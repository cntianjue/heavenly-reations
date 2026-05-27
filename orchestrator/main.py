# -*- coding: utf-8 -*-
import os
import re
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

DANGEROUS_PATH_PARTS = {
    ".git",
    ".ssh",
    ".aws",
    ".azure",
    ".gcp",
    "id_rsa",
    "id_ed25519",
}

BLOCKED_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
}

SAFE_COMMAND_PREFIXES = [
    "npm test",
    "npm run test",
    "npm run build",
    "pnpm test",
    "pnpm run test",
    "pnpm run build",
    "yarn test",
    "yarn build",
    "pytest",
    "python -m pytest",
    "mvn test",
    "gradle test",
    "go test ./...",
]


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


def run_cmd(cmd: list[str], cwd: Path | None = None, check: bool = True) -> str:
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        shell=False,
    )

    if check and result.returncode != 0:
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
    ], check=False)


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
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_input,
            },
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


def read_issue_doc(issue_number: int, filename: str) -> str:
    path = issue_dir(issue_number) / filename
    if not path.exists():
        raise RuntimeError(f"缺少文件: {path}")
    return path.read_text(encoding="utf-8")


def scan_project_tree(max_lines: int = 220) -> str:
    ignore_dirs = {
        ".git",
        ".venv",
        "node_modules",
        "dist",
        "build",
        "__pycache__",
        ".idea",
        ".vscode",
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


def read_small_project_files(max_files: int = 40, max_chars_each: int = 6000) -> str:
    allowed_suffixes = {
        ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go",
        ".md", ".json", ".yml", ".yaml", ".toml", ".xml",
        ".gradle", ".properties", ".html", ".css",
    }
    ignore_dirs = {
        ".git",
        ".venv",
        "node_modules",
        "dist",
        "build",
        "__pycache__",
        ".idea",
        ".vscode",
    }

    chunks = []
    count = 0

    for path in TARGET_REPO_PATH.rglob("*"):
        if not path.is_file():
            continue

        rel = path.relative_to(TARGET_REPO_PATH)
        if any(part in ignore_dirs for part in rel.parts):
            continue

        if path.suffix.lower() not in allowed_suffixes and path.name not in {"Dockerfile", "Makefile"}:
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        chunks.append(f"\n--- FILE: {rel} ---\n{content[:max_chars_each]}")
        count += 1

        if count >= max_files:
            break

    return "\n".join(chunks)


def commit_all(message: str):
    run_cmd(["git", "add", "."], cwd=TARGET_REPO_PATH)

    status = run_cmd(["git", "status", "--porcelain"], cwd=TARGET_REPO_PATH)

    if status:
        run_cmd(["git", "commit", "-m", message], cwd=TARGET_REPO_PATH)

        try:
            run_cmd(["git", "push"], cwd=TARGET_REPO_PATH)
        except Exception as e:
            print("[WARN] git push 失败，本地 commit 已完成。你可以稍后手动 git push。")
            print(e)


def current_branch() -> str:
    return run_cmd(["git", "branch", "--show-current"], cwd=TARGET_REPO_PATH)


def ensure_issue_branch(issue_number: int):
    branch = current_branch()
    desired = f"agent/issue-{issue_number}"

    if branch == desired:
        return

    branches = run_cmd(["git", "branch", "--list", desired], cwd=TARGET_REPO_PATH)
    if branches.strip():
        run_cmd(["git", "checkout", desired], cwd=TARGET_REPO_PATH)
    else:
        run_cmd(["git", "checkout", "-b", desired], cwd=TARGET_REPO_PATH)

    try:
        run_cmd(["git", "push", "-u", "origin", desired], cwd=TARGET_REPO_PATH)
    except Exception as e:
        print("[WARN] 分支 push 失败，本地分支已创建。你可以稍后手动 push。")
        print(e)


def extract_json_object(text: str) -> dict:
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except Exception:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise RuntimeError("模型输出中没有找到 JSON 对象。")

    return json.loads(cleaned[start:end + 1])


def validate_relative_path(path_text: str) -> Path:
    if not path_text or Path(path_text).is_absolute():
        raise RuntimeError(f"非法文件路径: {path_text}")

    normalized = Path(path_text)

    if ".." in normalized.parts:
        raise RuntimeError(f"禁止使用上级目录路径: {path_text}")

    if any(part in DANGEROUS_PATH_PARTS for part in normalized.parts):
        raise RuntimeError(f"危险路径，已拒绝: {path_text}")

    if normalized.name in BLOCKED_FILENAMES:
        raise RuntimeError(f"禁止修改真实环境配置文件: {path_text}")

    return normalized


def write_files_from_agent_json(issue_number: int, json_filename: str, commit_message: str):
    raw = read_issue_doc(issue_number, json_filename)
    data = extract_json_object(raw)

    files = data.get("files") or []
    if not isinstance(files, list):
        raise RuntimeError("JSON 中 files 必须是数组。")

    written = []

    for item in files:
        rel_path_text = item.get("path")
        content = item.get("content")

        if content is None:
            raise RuntimeError(f"文件缺少 content: {rel_path_text}")

        rel_path = validate_relative_path(rel_path_text)
        full_path = TARGET_REPO_PATH / rel_path

        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        written.append(str(rel_path))

    save_issue_doc(issue_number, f"{json_filename}.applied.md", "\n".join(written))
    commit_all(commit_message)

    return data, written


def run_safe_commands(commands: list[str]) -> list[dict]:
    results = []

    for command in commands:
        command = command.strip()

        if not any(command == p or command.startswith(p + " ") for p in SAFE_COMMAND_PREFIXES):
            results.append({
                "command": command,
                "skipped": True,
                "reason": "不在安全命令白名单中",
            })
            continue

        print(f"[Test Command] {command}")

        result = subprocess.run(
            command,
            cwd=str(TARGET_REPO_PATH),
            capture_output=True,
            text=True,
            encoding="utf-8",
            shell=True,
        )

        results.append({
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout[-6000:],
            "stderr": result.stderr[-6000:],
        })

    return results


def get_git_diff() -> str:
    diff = run_cmd(["git", "diff", "HEAD~1..HEAD"], cwd=TARGET_REPO_PATH, check=False)
    if diff.strip():
        return diff

    return run_cmd(["git", "diff"], cwd=TARGET_REPO_PATH, check=False)


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

        commit_all(f"docs: add PRD for issue #{number}")

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

        prd = read_issue_doc(number, "prd.md")
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

        commit_all(f"docs: add architecture for issue #{number}")

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

        prd = read_issue_doc(number, "prd.md")
        architecture = read_issue_doc(number, "architecture.md")

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

        commit_all(f"docs: add development plan for issue #{number}")

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
                "已收到开发计划确认。下一阶段进入 Coding Agent，先生成代码文件方案，等待 `/approve patch` 后再写入项目。",
            )

            print(f"[Approval] Issue #{number} 开发计划已确认")


def handle_ready_for_dev():
    issues = list_issues_by_label("stage:ready-for-dev")

    for issue in issues:
        number = issue["number"]
        title = issue["title"]

        prd = read_issue_doc(number, "prd.md")
        architecture = read_issue_doc(number, "architecture.md")
        plan = read_issue_doc(number, "plan.md")
        tree = scan_project_tree()
        files = read_small_project_files()

        prompt = read_prompt("coding.md")

        user_input = f"""
Issue 标题：
{title}

PRD：
{prd}

架构设计：
{architecture}

开发计划：
{plan}

当前项目结构：
{tree}

部分项目文件内容：
{files}
"""

        print(f"[Coding Agent] 开始生成代码方案 Issue #{number}: {title}")

        output = call_llm(prompt, user_input)

        save_issue_doc(number, "coding-output.json", output)

        commit_all(f"docs: add coding output for issue #{number}")

        comment_issue(
            number,
            f"""## Coding Agent 已生成代码文件方案

产物：

- `docs/issues/{number}/coding-output.json`

请先检查该文件中即将写入/修改的文件列表。

确认写入项目代码，请评论：

`/approve patch`

如需驳回，请评论：

`/reject patch 你的原因`
""",
        )

        remove_label(number, "stage:ready-for-dev")
        add_label(number, "stage:waiting-patch-approval")
        add_label(number, "agent:coding")

        print(f"[Coding Agent] Issue #{number} 代码方案生成完成")


def handle_patch_approval():
    issues = list_issues_by_label("stage:waiting-patch-approval")

    for issue in issues:
        number = issue["number"]

        if not has_comment_command(number, "/approve patch"):
            continue

        print(f"[Coding Agent] 开始写入代码 Issue #{number}")

        ensure_issue_branch(number)
        data, written = write_files_from_agent_json(
            number,
            "coding-output.json",
            f"feat: implement issue #{number}",
        )

        report = f"""# Coding 写入报告

## 写入文件

{chr(10).join(f"- {p}" for p in written)}

## 说明

{data.get("summary", "")}

## Notes

{chr(10).join(f"- {n}" for n in data.get("notes", []))}
"""
        save_issue_doc(number, "coding-report.md", report)
        commit_all(f"docs: add coding report for issue #{number}")

        comment_issue(
            number,
            f"""## Coding Agent 已写入代码

产物：

- `docs/issues/{number}/coding-report.md`

已写入文件：

{chr(10).join(f"- `{p}`" for p in written)}

下一步进入 Testing Agent。
""",
        )

        remove_label(number, "stage:waiting-patch-approval")
        add_label(number, "stage:testing")


def handle_testing():
    issues = list_issues_by_label("stage:testing")

    for issue in issues:
        number = issue["number"]
        title = issue["title"]

        prd = read_issue_doc(number, "prd.md")
        architecture = read_issue_doc(number, "architecture.md")
        plan = read_issue_doc(number, "plan.md")
        tree = scan_project_tree()
        files = read_small_project_files()

        prompt = read_prompt("testing.md")

        user_input = f"""
Issue 标题：
{title}

PRD：
{prd}

架构设计：
{architecture}

开发计划：
{plan}

当前项目结构：
{tree}

部分项目文件内容：
{files}
"""

        print(f"[Testing Agent] 开始生成测试 Issue #{number}: {title}")

        output = call_llm(prompt, user_input)
        save_issue_doc(number, "testing-output.json", output)
        commit_all(f"docs: add testing output for issue #{number}")

        ensure_issue_branch(number)
        data, written = write_files_from_agent_json(
            number,
            "testing-output.json",
            f"test: add tests for issue #{number}",
        )

        commands = data.get("commands") or []
        if not isinstance(commands, list):
            commands = []

        results = run_safe_commands(commands)

        report = {
            "summary": data.get("summary", ""),
            "written_files": written,
            "commands": results,
            "notes": data.get("notes", []),
        }

        save_issue_doc(
            number,
            "test-report.md",
            "# 测试报告\n\n```json\n"
            + json.dumps(report, ensure_ascii=False, indent=2)
            + "\n```\n",
        )

        commit_all(f"docs: add test report for issue #{number}")

        comment_issue(
            number,
            f"""## Testing Agent 已完成测试处理

产物：

- `docs/issues/{number}/testing-output.json`
- `docs/issues/{number}/test-report.md`

下一步进入 Review Agent。
""",
        )

        remove_label(number, "stage:testing")
        add_label(number, "stage:reviewing")
        add_label(number, "agent:testing")

        print(f"[Testing Agent] Issue #{number} 测试完成")


def handle_reviewing():
    issues = list_issues_by_label("stage:reviewing")

    for issue in issues:
        number = issue["number"]
        title = issue["title"]

        prd = read_issue_doc(number, "prd.md")
        architecture = read_issue_doc(number, "architecture.md")
        plan = read_issue_doc(number, "plan.md")
        test_report = read_issue_doc(number, "test-report.md")
        diff = get_git_diff()

        prompt = read_prompt("review.md")

        user_input = f"""
Issue 标题：
{title}

PRD：
{prd}

架构设计：
{architecture}

开发计划：
{plan}

测试报告：
{test_report}

Git Diff：
{diff}
"""

        print(f"[Review Agent] 开始 Review Issue #{number}: {title}")

        report = call_llm(prompt, user_input)

        save_issue_doc(number, "review-report.md", report)
        commit_all(f"docs: add review report for issue #{number}")

        comment_issue(
            number,
            f"""## Review Agent 已完成代码审查

产物：

- `docs/issues/{number}/review-report.md`

下一步进入 DevOps Agent。
""",
        )

        remove_label(number, "stage:reviewing")
        add_label(number, "stage:devops")
        add_label(number, "agent:review")

        print(f"[Review Agent] Issue #{number} Review 完成")


def handle_devops():
    issues = list_issues_by_label("stage:devops")

    for issue in issues:
        number = issue["number"]
        title = issue["title"]

        prd = read_issue_doc(number, "prd.md")
        architecture = read_issue_doc(number, "architecture.md")
        plan = read_issue_doc(number, "plan.md")
        review_report = read_issue_doc(number, "review-report.md")
        tree = scan_project_tree()
        files = read_small_project_files()

        prompt = read_prompt("devops.md")

        user_input = f"""
Issue 标题：
{title}

PRD：
{prd}

架构设计：
{architecture}

开发计划：
{plan}

Review 报告：
{review_report}

当前项目结构：
{tree}

部分项目文件内容：
{files}
"""

        print(f"[DevOps Agent] 开始生成部署文件 Issue #{number}: {title}")

        output = call_llm(prompt, user_input)
        save_issue_doc(number, "devops-output.json", output)
        commit_all(f"docs: add devops output for issue #{number}")

        ensure_issue_branch(number)
        data, written = write_files_from_agent_json(
            number,
            "devops-output.json",
            f"chore: add devops files for issue #{number}",
        )

        report = f"""# DevOps 报告

## 部署概要

{data.get("summary", "")}

## 写入文件

{chr(10).join(f"- {p}" for p in written)}

## 建议命令

{chr(10).join(f"- {c}" for c in data.get("commands", []))}

## 注意事项

{chr(10).join(f"- {n}" for n in data.get("notes", []))}
"""
        save_issue_doc(number, "deploy-report.md", report)
        commit_all(f"docs: add deploy report for issue #{number}")

        comment_issue(
            number,
            f"""## DevOps Agent 已完成部署文件生成

产物：

- `docs/issues/{number}/deploy-report.md`

已写入文件：

{chr(10).join(f"- `{p}`" for p in written)}

当前分支：

`agent/issue-{number}`

请人工检查后创建 PR 或执行：

`gh pr create --fill`
""",
        )

        remove_label(number, "stage:devops")
        add_label(number, "stage:ready-for-pr")
        add_label(number, "agent:devops")

        print(f"[DevOps Agent] Issue #{number} DevOps 完成")


def main():
    check_config()

    # 第一阶段
    handle_intake()
    handle_architecture()
    handle_architecture_approval()
    handle_pm_planning()
    handle_plan_approval()

    # 第二阶段
    handle_ready_for_dev()
    handle_patch_approval()
    handle_testing()
    handle_reviewing()
    handle_devops()


if __name__ == "__main__":
    main()
