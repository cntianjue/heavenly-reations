import os
import json
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5-coder:7b")

TARGET_REPO_PATH = Path(os.getenv("TARGET_REPO_PATH", ""))
AGENT_DATA_DIR = Path(os.getenv("AGENT_DATA_DIR", "./data"))

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts"

client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
)


def check_config():
    required = {
        "GITHUB_OWNER": GITHUB_OWNER,
        "GITHUB_REPO": GITHUB_REPO,
        "TARGET_REPO_PATH": str(TARGET_REPO_PATH),
        "AGENT_DATA_DIR": str(AGENT_DATA_DIR),
    }

    missing = [k for k, v in required.items() if not v]
    if missing:
        raise RuntimeError(f".env 缺少配置: {', '.join(missing)}")

    if not TARGET_REPO_PATH.exists():
        raise RuntimeError(f"目标项目目录不存在: {TARGET_REPO_PATH}")

    if not PROMPTS_DIR.exists():
        raise RuntimeError(f"prompts 目录不存在: {PROMPTS_DIR}")


def run_cmd(cmd: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "命令执行失败:\n"
            f"命令: {' '.join(cmd)}\n"
            f"错误: {result.stderr}"
        )

    return result.stdout.strip()


def gh_json(args: list[str]):
    output = run_cmd(["gh", *args])
    if not output:
        return None
    return json.loads(output)


def list_issues_by_label(label: str):
    return gh_json([
        "issue",
        "list",
        "--repo",
        f"{GITHUB_OWNER}/{GITHUB_REPO}",
        "--label",
        label,
        "--state",
        "open",
        "--json",
        "number,title,body,labels",
    ]) or []


def get_issue_comments(issue_number: int):
    return gh_json([
        "api",
        f"repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues/{issue_number}/comments",
    ]) or []


def comment_issue(issue_number: int, body: str):
    temp = AGENT_DATA_DIR / "temp_comment.md"
    temp.parent.mkdir(parents=True, exist_ok=True)
    temp.write_text(body, encoding="utf-8")

    run_cmd([
        "gh",
        "issue",
        "comment",
        str(issue_number),
        "--repo",
        f"{GITHUB_OWNER}/{GITHUB_REPO}",
        "--body-file",
        str(temp),
    ])


def add_label(issue_number: int, label: str):
    run_cmd([
        "gh",
        "issue",
        "edit",
        str(issue_number),
        "--repo",
        f"{GITHUB_OWNER}/{GITHUB_REPO}",
        "--add-label",
        label,
    ])


def remove_label(issue_number: int, label: str):
    run_cmd([
        "gh",
        "issue",
        "edit",
        str(issue_number),
        "--repo",
        f"{GITHUB_OWNER}/{GITHUB_REPO}",
        "--remove-label",
        label,
    ])


def has_comment_command(issue_number: int, command: str) -> bool:
    comments = get_issue_comments(issue_number)

    for comment in comments:
        body = comment.get("body") or ""
        if command in body:
            return True

    return False


def call_llm(system_prompt: str, user_input: str) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content or ""


def read_prompt(name: str) -> str:
    prompt_path = PROMPTS_DIR / name

    if not prompt_path.exists():
        raise RuntimeError(f"Prompt 文件不存在: {prompt_path}")

    return prompt_path.read_text(encoding="utf-8")


def issue_dir(issue_number: int) -> Path:
    path = TARGET_REPO_PATH / "docs" / "issues" / str(issue_number)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_issue_doc(issue_number: int, filename: str, content: str) -> Path:
    path = issue_dir(issue_number) / filename
    path.write_text(content, encoding="utf-8")
    return path


def scan_project_tree(max_lines: int = 120) -> str:
    ignore_dirs = {
        ".git",
        ".venv",
        "node_modules",
        "dist",
        "build",
        "__pycache__",
    }

    lines = []

    for path in TARGET_REPO_PATH.rglob("*"):
        rel = path.relative_to(TARGET_REPO_PATH)

        if any(part in ignore_dirs for part in rel.parts):
            continue

        lines.append(str(rel))

        if len(lines) >= max_lines:
            break

    return "\n".join(lines)


def commit_docs(issue_number: int, message: str):
    run_cmd(["git", "add", "docs"], cwd=TARGET_REPO_PATH)

    status = run_cmd(["git", "status", "--porcelain"], cwd=TARGET_REPO_PATH)

    if status:
        run_cmd(["git", "commit", "-m", message], cwd=TARGET_REPO_PATH)
        run_cmd(["git", "push"], cwd=TARGET_REPO_PATH)


def handle_intake():
    issues = list_issues_by_label("stage:intake")

    for issue in issues:
        number = issue["number"]
        title = issue["title"]
        body = issue.get("body") or ""

        prompt = read_prompt("product.md")

        user_input = f"""
Issue 标题：
{title}

Issue 内容：
{body}
"""

        print(f"[Product Agent] 开始处理 Issue #{number}: {title}")

        prd = call_llm(prompt, user_input)

        save_issue_doc(number, "original_issue.md", user_input)
        save_issue_doc(number, "prd.md", prd)

        commit_docs(number, f"docs: add PRD for issue #{number}")

        comment_issue(
            number,
            f"""## Product Agent 已完成需求拆解

产物：

- `docs/issues/{number}/prd.md`

下一步进入架构设计阶段。
""",
        )

        remove_label(number, "stage:intake")
        add_label(number, "stage:architecture")
        add_label(number, "agent:product")

        print(f"[Product Agent] Issue #{number} 处理完成")


def handle_architecture():
    issues = list_issues_by_label("stage:architecture")

    for issue in issues:
        number = issue["number"]
        title = issue["title"]

        prd_path = issue_dir(number) / "prd.md"

        if not prd_path.exists():
            comment_issue(number, "未找到 PRD 文件，无法进行架构设计。")
            add_label(number, "stage:blocked")
            continue

        prd = prd_path.read_text(encoding="utf-8")
        tree = scan_project_tree()

        prompt = read_prompt("architecture.md")

        user_input = f"""
Issue 标题：
{title}

PRD：
{prd}

当前项目结构：
{tree}
"""

        print(f"[Architecture Agent] 开始处理 Issue #{number}: {title}")

        architecture = call_llm(prompt, user_input)

        save_issue_doc(number, "architecture.md", architecture)

        commit_docs(number, f"docs: add architecture for issue #{number}")

        comment_issue(
            number,
            f"""## Architecture Agent 已完成架构设计

产物：

- `docs/issues/{number}/architecture.md`

请确认是否进入项目计划阶段。

确认方式：

`/approve architecture`

如需驳回，请评论：

`/reject architecture 你的原因`
""",
        )

        remove_label(number, "stage:architecture")
        add_label(number, "stage:waiting-architecture-approval")
        add_label(number, "agent:architecture")

        print(f"[Architecture Agent] Issue #{number} 处理完成")


def handle_architecture_approval():
    issues = list_issues_by_label("stage:waiting-architecture-approval")

    for issue in issues:
        number = issue["number"]

        if has_comment_command(number, "/approve architecture"):
            remove_label(number, "stage:waiting-architecture-approval")
            add_label(number, "stage:pm-planning")

            comment_issue(
                number,
                "已收到架构确认，进入项目管理 Agent 拆分开发计划。",
            )

            print(f"[Approval] Issue #{number} 架构已确认")


def handle_pm_planning():
    issues = list_issues_by_label("stage:pm-planning")

    for issue in issues:
        number = issue["number"]
        title = issue["title"]

        prd_path = issue_dir(number) / "prd.md"
        architecture_path = issue_dir(number) / "architecture.md"

        if not prd_path.exists() or not architecture_path.exists():
            comment_issue(number, "缺少 PRD 或架构文档，无法生成开发计划。")
            add_label(number, "stage:blocked")
            continue

        prd = prd_path.read_text(encoding="utf-8")
        architecture = architecture_path.read_text(encoding="utf-8")

        prompt = read_prompt("pm.md")

        user_input = f"""
Issue 标题：
{title}

PRD：
{prd}

架构设计：
{architecture}
"""

        print(f"[PM Agent] 开始处理 Issue #{number}: {title}")

        plan = call_llm(prompt, user_input)

        save_issue_doc(number, "plan.md", plan)

        commit_docs(number, f"docs: add development plan for issue #{number}")

        comment_issue(
            number,
            f"""## 项目管理 Agent 已完成开发计划

产物：

- `docs/issues/{number}/plan.md`

请确认是否进入开发执行阶段。

确认方式：

`/approve plan`

如需驳回，请评论：

`/reject plan 你的原因`
""",
        )

        remove_label(number, "stage:pm-planning")
        add_label(number, "stage:waiting-plan-approval")
        add_label(number, "agent:pm")

        print(f"[PM Agent] Issue #{number} 处理完成")


def handle_plan_approval():
    issues = list_issues_by_label("stage:waiting-plan-approval")

    for issue in issues:
        number = issue["number"]

        if has_comment_command(number, "/approve plan"):
            remove_label(number, "stage:waiting-plan-approval")
            add_label(number, "stage:ready-for-dev")

            comment_issue(
                number,
                "已收到开发计划确认。下一阶段可以接入 Coding / Testing / Review / DevOps Agent。",
            )

            print(f"[Approval] Issue #{number} 开发计划已确认")


def main():
    check_config()

    handle_intake()
    handle_architecture()
    handle_architecture_approval()
    handle_pm_planning()
    handle_plan_approval()


if __name__ == "__main__":
    main()
