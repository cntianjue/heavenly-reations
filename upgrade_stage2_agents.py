# -*- coding: utf-8 -*-
"""
upgrade_stage2_agents.py

作用：
  将第一阶段已经跑通的 local-ai-dev-agents 升级到第二阶段：
  - 新增 Coding / Testing / Review / DevOps Agent Prompt
  - 新增第二阶段 GitHub Labels
  - 更新 .env 的 TARGET_REPO_PATH
  - 备份并替换 orchestrator/main.py 为第二阶段版本

推荐用法：
  cd D:\ai-dev\local-ai-dev-agents
  python upgrade_stage2_agents.py --target-repo "D:\work\project\Pipeline\heavenly-reations"

如果你的 Agent 系统目录就在当前目录，直接运行即可。
"""

import argparse
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


DEFAULT_TARGET_REPO = r"D:\work\project\Pipeline\heavenly-reations"

CODING_PROMPT = '你是 Coding Agent，负责根据 PRD、架构设计、开发计划生成代码修改方案。\n\n重要约束：\n1. 你不能修改 main/master 分支。\n2. 你必须严格遵守 PRD、architecture.md、plan.md。\n3. 你不能引入 plan.md 没有提到的复杂组件。\n4. 你不能读取或生成真实密钥。\n5. 你不能输出解释性闲聊。\n\n你必须输出一个 JSON 对象，格式如下：\n\n{\n  "summary": "本次实现概要",\n  "files": [\n    {\n      "path": "相对项目根目录的文件路径",\n      "content": "完整文件内容"\n    }\n  ],\n  "commands": [\n    "建议人工执行或测试 Agent 执行的命令"\n  ],\n  "notes": [\n    "需要人工注意的事项"\n  ]\n}\n\n要求：\n- files 必须是完整文件内容，不要输出 diff。\n- path 不能是绝对路径。\n- path 不能包含 ..。\n- 不允许修改 .env、私钥、证书、系统目录。\n- 如果目标项目为空，可以生成最小可运行项目结构。\n- 如果现有文件需要修改，也要输出完整的新文件内容。\n'
TESTING_PROMPT = '你是 Testing Agent，负责根据 PRD、架构设计、开发计划和当前代码生成测试方案、测试文件和测试命令。\n\n你必须输出一个 JSON 对象，格式如下：\n\n{\n  "summary": "测试策略概要",\n  "files": [\n    {\n      "path": "相对项目根目录的测试文件路径",\n      "content": "完整测试文件内容"\n    }\n  ],\n  "commands": [\n    "可执行的测试命令"\n  ],\n  "notes": [\n    "测试覆盖说明和风险"\n  ]\n}\n\n要求：\n- 优先补充单元测试，其次补充集成测试。\n- commands 只能包含安全测试/构建命令，例如：npm test、npm run test、pytest、mvn test、gradle test、go test ./...、python -m pytest。\n- 不要输出危险命令。\n- 不要修改 .env、密钥、证书。\n'
REVIEW_PROMPT = '你是 Review Agent，负责审查本次代码变更。\n\n你必须输出 Markdown，结构如下：\n\n# Review 报告\n\n## 1. 总体结论\n给出：通过 / 有条件通过 / 不通过。\n\n## 2. 与 PRD 的一致性\n\n## 3. 与架构设计的一致性\n\n## 4. 代码质量\n\n## 5. 测试质量\n\n## 6. 安全风险\n\n## 7. 可维护性风险\n\n## 8. 必须修改项\n\n## 9. 建议优化项\n\n## 10. 是否建议进入 DevOps 阶段\n\n要求：\n- 基于 git diff 审查，不要凭空评价。\n- 发现问题要具体到文件和原因。\n'
DEVOPS_PROMPT = '你是 DevOps Agent，负责根据项目代码、PRD、架构设计和开发计划生成部署相关文件。\n\n你必须输出一个 JSON 对象，格式如下：\n\n{\n  "summary": "部署方案概要",\n  "files": [\n    {\n      "path": "相对项目根目录的部署文件路径",\n      "content": "完整文件内容"\n    }\n  ],\n  "commands": [\n    "建议人工执行的构建或部署命令"\n  ],\n  "notes": [\n    "部署注意事项"\n  ]\n}\n\n要求：\n- 优先生成 Dockerfile、docker-compose.yml、.env.example、README 部署说明。\n- 不允许生成真实密钥。\n- 不允许修改真实 .env。\n- 如果不能准确判断技术栈，先生成保守部署文档，不要硬编复杂配置。\n'
ORCHESTRATOR_STAGE2 = '# -*- coding: utf-8 -*-\nimport os\nimport re\nimport json\nimport subprocess\nfrom pathlib import Path\n\nfrom dotenv import load_dotenv\nfrom openai import OpenAI\n\n\nload_dotenv()\n\nGITHUB_OWNER = os.getenv("GITHUB_OWNER")\nGITHUB_REPO = os.getenv("GITHUB_REPO")\n\nLLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")\nLLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")\nLLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5-coder:7b")\n\nTARGET_REPO_PATH = Path(os.getenv("TARGET_REPO_PATH", ""))\nAGENT_DATA_DIR = Path(os.getenv("AGENT_DATA_DIR", "./data"))\n\nROOT = Path(__file__).resolve().parents[1]\nPROMPTS_DIR = ROOT / "prompts"\n\nclient = OpenAI(\n    base_url=LLM_BASE_URL,\n    api_key=LLM_API_KEY,\n)\n\nDANGEROUS_PATH_PARTS = {\n    ".git",\n    ".ssh",\n    ".aws",\n    ".azure",\n    ".gcp",\n    "id_rsa",\n    "id_ed25519",\n}\n\nBLOCKED_FILENAMES = {\n    ".env",\n    ".env.local",\n    ".env.production",\n    ".env.development",\n}\n\nSAFE_COMMAND_PREFIXES = [\n    "npm test",\n    "npm run test",\n    "npm run build",\n    "pnpm test",\n    "pnpm run test",\n    "pnpm run build",\n    "yarn test",\n    "yarn build",\n    "pytest",\n    "python -m pytest",\n    "mvn test",\n    "gradle test",\n    "go test ./...",\n]\n\n\ndef check_config():\n    required = {\n        "GITHUB_OWNER": GITHUB_OWNER,\n        "GITHUB_REPO": GITHUB_REPO,\n        "TARGET_REPO_PATH": str(TARGET_REPO_PATH),\n        "AGENT_DATA_DIR": str(AGENT_DATA_DIR),\n    }\n\n    missing = [k for k, v in required.items() if not v]\n    if missing:\n        raise RuntimeError(f".env 缺少配置: {\', \'.join(missing)}")\n\n    if not TARGET_REPO_PATH.exists():\n        raise RuntimeError(f"目标项目目录不存在: {TARGET_REPO_PATH}")\n\n    if not PROMPTS_DIR.exists():\n        raise RuntimeError(f"prompts 目录不存在: {PROMPTS_DIR}")\n\n\ndef run_cmd(cmd: list[str], cwd: Path | None = None, check: bool = True) -> str:\n    result = subprocess.run(\n        cmd,\n        cwd=str(cwd) if cwd else None,\n        capture_output=True,\n        text=True,\n        encoding="utf-8",\n        shell=False,\n    )\n\n    if check and result.returncode != 0:\n        raise RuntimeError(\n            "命令执行失败:\\n"\n            f"命令: {\' \'.join(cmd)}\\n"\n            f"错误: {result.stderr}"\n        )\n\n    return result.stdout.strip()\n\n\ndef gh_json(args: list[str]):\n    output = run_cmd(["gh", *args])\n    if not output:\n        return None\n    return json.loads(output)\n\n\ndef list_issues_by_label(label: str):\n    return gh_json([\n        "issue",\n        "list",\n        "--repo",\n        f"{GITHUB_OWNER}/{GITHUB_REPO}",\n        "--label",\n        label,\n        "--state",\n        "open",\n        "--json",\n        "number,title,body,labels",\n    ]) or []\n\n\ndef get_issue_comments(issue_number: int):\n    return gh_json([\n        "api",\n        f"repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues/{issue_number}/comments",\n    ]) or []\n\n\ndef comment_issue(issue_number: int, body: str):\n    temp = AGENT_DATA_DIR / "temp_comment.md"\n    temp.parent.mkdir(parents=True, exist_ok=True)\n    temp.write_text(body, encoding="utf-8")\n\n    run_cmd([\n        "gh",\n        "issue",\n        "comment",\n        str(issue_number),\n        "--repo",\n        f"{GITHUB_OWNER}/{GITHUB_REPO}",\n        "--body-file",\n        str(temp),\n    ])\n\n\ndef add_label(issue_number: int, label: str):\n    run_cmd([\n        "gh",\n        "issue",\n        "edit",\n        str(issue_number),\n        "--repo",\n        f"{GITHUB_OWNER}/{GITHUB_REPO}",\n        "--add-label",\n        label,\n    ])\n\n\ndef remove_label(issue_number: int, label: str):\n    run_cmd([\n        "gh",\n        "issue",\n        "edit",\n        str(issue_number),\n        "--repo",\n        f"{GITHUB_OWNER}/{GITHUB_REPO}",\n        "--remove-label",\n        label,\n    ], check=False)\n\n\ndef has_comment_command(issue_number: int, command: str) -> bool:\n    comments = get_issue_comments(issue_number)\n\n    for comment in comments:\n        body = comment.get("body") or ""\n        if command in body:\n            return True\n\n    return False\n\n\ndef call_llm(system_prompt: str, user_input: str) -> str:\n    response = client.chat.completions.create(\n        model=LLM_MODEL,\n        messages=[\n            {\n                "role": "system",\n                "content": system_prompt,\n            },\n            {\n                "role": "user",\n                "content": user_input,\n            },\n        ],\n        temperature=0.2,\n    )\n\n    return response.choices[0].message.content or ""\n\n\ndef read_prompt(name: str) -> str:\n    prompt_path = PROMPTS_DIR / name\n\n    if not prompt_path.exists():\n        raise RuntimeError(f"Prompt 文件不存在: {prompt_path}")\n\n    return prompt_path.read_text(encoding="utf-8")\n\n\ndef issue_dir(issue_number: int) -> Path:\n    path = TARGET_REPO_PATH / "docs" / "issues" / str(issue_number)\n    path.mkdir(parents=True, exist_ok=True)\n    return path\n\n\ndef save_issue_doc(issue_number: int, filename: str, content: str) -> Path:\n    path = issue_dir(issue_number) / filename\n    path.write_text(content, encoding="utf-8")\n    return path\n\n\ndef read_issue_doc(issue_number: int, filename: str) -> str:\n    path = issue_dir(issue_number) / filename\n    if not path.exists():\n        raise RuntimeError(f"缺少文件: {path}")\n    return path.read_text(encoding="utf-8")\n\n\ndef scan_project_tree(max_lines: int = 220) -> str:\n    ignore_dirs = {\n        ".git",\n        ".venv",\n        "node_modules",\n        "dist",\n        "build",\n        "__pycache__",\n        ".idea",\n        ".vscode",\n    }\n\n    lines = []\n\n    for path in TARGET_REPO_PATH.rglob("*"):\n        rel = path.relative_to(TARGET_REPO_PATH)\n\n        if any(part in ignore_dirs for part in rel.parts):\n            continue\n\n        lines.append(str(rel))\n\n        if len(lines) >= max_lines:\n            break\n\n    return "\\n".join(lines)\n\n\ndef read_small_project_files(max_files: int = 40, max_chars_each: int = 6000) -> str:\n    allowed_suffixes = {\n        ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go",\n        ".md", ".json", ".yml", ".yaml", ".toml", ".xml",\n        ".gradle", ".properties", ".html", ".css",\n    }\n    ignore_dirs = {\n        ".git",\n        ".venv",\n        "node_modules",\n        "dist",\n        "build",\n        "__pycache__",\n        ".idea",\n        ".vscode",\n    }\n\n    chunks = []\n    count = 0\n\n    for path in TARGET_REPO_PATH.rglob("*"):\n        if not path.is_file():\n            continue\n\n        rel = path.relative_to(TARGET_REPO_PATH)\n        if any(part in ignore_dirs for part in rel.parts):\n            continue\n\n        if path.suffix.lower() not in allowed_suffixes and path.name not in {"Dockerfile", "Makefile"}:\n            continue\n\n        try:\n            content = path.read_text(encoding="utf-8", errors="ignore")\n        except Exception:\n            continue\n\n        chunks.append(f"\\n--- FILE: {rel} ---\\n{content[:max_chars_each]}")\n        count += 1\n\n        if count >= max_files:\n            break\n\n    return "\\n".join(chunks)\n\n\ndef commit_all(message: str):\n    run_cmd(["git", "add", "."], cwd=TARGET_REPO_PATH)\n\n    status = run_cmd(["git", "status", "--porcelain"], cwd=TARGET_REPO_PATH)\n\n    if status:\n        run_cmd(["git", "commit", "-m", message], cwd=TARGET_REPO_PATH)\n\n        try:\n            run_cmd(["git", "push"], cwd=TARGET_REPO_PATH)\n        except Exception as e:\n            print("[WARN] git push 失败，本地 commit 已完成。你可以稍后手动 git push。")\n            print(e)\n\n\ndef current_branch() -> str:\n    return run_cmd(["git", "branch", "--show-current"], cwd=TARGET_REPO_PATH)\n\n\ndef ensure_issue_branch(issue_number: int):\n    branch = current_branch()\n    desired = f"agent/issue-{issue_number}"\n\n    if branch == desired:\n        return\n\n    branches = run_cmd(["git", "branch", "--list", desired], cwd=TARGET_REPO_PATH)\n    if branches.strip():\n        run_cmd(["git", "checkout", desired], cwd=TARGET_REPO_PATH)\n    else:\n        run_cmd(["git", "checkout", "-b", desired], cwd=TARGET_REPO_PATH)\n\n    try:\n        run_cmd(["git", "push", "-u", "origin", desired], cwd=TARGET_REPO_PATH)\n    except Exception as e:\n        print("[WARN] 分支 push 失败，本地分支已创建。你可以稍后手动 push。")\n        print(e)\n\n\ndef extract_json_object(text: str) -> dict:\n    cleaned = text.strip()\n\n    if cleaned.startswith("```"):\n        cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\\s*", "", cleaned)\n        cleaned = re.sub(r"\\s*```$", "", cleaned)\n\n    try:\n        return json.loads(cleaned)\n    except Exception:\n        pass\n\n    start = cleaned.find("{")\n    end = cleaned.rfind("}")\n    if start == -1 or end == -1 or end <= start:\n        raise RuntimeError("模型输出中没有找到 JSON 对象。")\n\n    return json.loads(cleaned[start:end + 1])\n\n\ndef validate_relative_path(path_text: str) -> Path:\n    if not path_text or Path(path_text).is_absolute():\n        raise RuntimeError(f"非法文件路径: {path_text}")\n\n    normalized = Path(path_text)\n\n    if ".." in normalized.parts:\n        raise RuntimeError(f"禁止使用上级目录路径: {path_text}")\n\n    if any(part in DANGEROUS_PATH_PARTS for part in normalized.parts):\n        raise RuntimeError(f"危险路径，已拒绝: {path_text}")\n\n    if normalized.name in BLOCKED_FILENAMES:\n        raise RuntimeError(f"禁止修改真实环境配置文件: {path_text}")\n\n    return normalized\n\n\ndef write_files_from_agent_json(issue_number: int, json_filename: str, commit_message: str):\n    raw = read_issue_doc(issue_number, json_filename)\n    data = extract_json_object(raw)\n\n    files = data.get("files") or []\n    if not isinstance(files, list):\n        raise RuntimeError("JSON 中 files 必须是数组。")\n\n    written = []\n\n    for item in files:\n        rel_path_text = item.get("path")\n        content = item.get("content")\n\n        if content is None:\n            raise RuntimeError(f"文件缺少 content: {rel_path_text}")\n\n        rel_path = validate_relative_path(rel_path_text)\n        full_path = TARGET_REPO_PATH / rel_path\n\n        full_path.parent.mkdir(parents=True, exist_ok=True)\n        full_path.write_text(content, encoding="utf-8")\n        written.append(str(rel_path))\n\n    save_issue_doc(issue_number, f"{json_filename}.applied.md", "\\n".join(written))\n    commit_all(commit_message)\n\n    return data, written\n\n\ndef run_safe_commands(commands: list[str]) -> list[dict]:\n    results = []\n\n    for command in commands:\n        command = command.strip()\n\n        if not any(command == p or command.startswith(p + " ") for p in SAFE_COMMAND_PREFIXES):\n            results.append({\n                "command": command,\n                "skipped": True,\n                "reason": "不在安全命令白名单中",\n            })\n            continue\n\n        print(f"[Test Command] {command}")\n\n        result = subprocess.run(\n            command,\n            cwd=str(TARGET_REPO_PATH),\n            capture_output=True,\n            text=True,\n            encoding="utf-8",\n            shell=True,\n        )\n\n        results.append({\n            "command": command,\n            "returncode": result.returncode,\n            "stdout": result.stdout[-6000:],\n            "stderr": result.stderr[-6000:],\n        })\n\n    return results\n\n\ndef get_git_diff() -> str:\n    diff = run_cmd(["git", "diff", "HEAD~1..HEAD"], cwd=TARGET_REPO_PATH, check=False)\n    if diff.strip():\n        return diff\n\n    return run_cmd(["git", "diff"], cwd=TARGET_REPO_PATH, check=False)\n\n\ndef handle_intake():\n    issues = list_issues_by_label("stage:intake")\n\n    for issue in issues:\n        number = issue["number"]\n        title = issue["title"]\n        body = issue.get("body") or ""\n\n        prompt = read_prompt("product.md")\n\n        user_input = f"""\nIssue 标题：\n{title}\n\nIssue 内容：\n{body}\n"""\n\n        print(f"[Product Agent] 开始处理 Issue #{number}: {title}")\n\n        prd = call_llm(prompt, user_input)\n\n        save_issue_doc(number, "original_issue.md", user_input)\n        save_issue_doc(number, "prd.md", prd)\n\n        commit_all(f"docs: add PRD for issue #{number}")\n\n        comment_issue(\n            number,\n            f"""## Product Agent 已完成需求拆解\n\n产物：\n\n- `docs/issues/{number}/prd.md`\n\n下一步进入架构设计阶段。\n""",\n        )\n\n        remove_label(number, "stage:intake")\n        add_label(number, "stage:architecture")\n        add_label(number, "agent:product")\n\n        print(f"[Product Agent] Issue #{number} 处理完成")\n\n\ndef handle_architecture():\n    issues = list_issues_by_label("stage:architecture")\n\n    for issue in issues:\n        number = issue["number"]\n        title = issue["title"]\n\n        prd = read_issue_doc(number, "prd.md")\n        tree = scan_project_tree()\n\n        prompt = read_prompt("architecture.md")\n\n        user_input = f"""\nIssue 标题：\n{title}\n\nPRD：\n{prd}\n\n当前项目结构：\n{tree}\n"""\n\n        print(f"[Architecture Agent] 开始处理 Issue #{number}: {title}")\n\n        architecture = call_llm(prompt, user_input)\n\n        save_issue_doc(number, "architecture.md", architecture)\n\n        commit_all(f"docs: add architecture for issue #{number}")\n\n        comment_issue(\n            number,\n            f"""## Architecture Agent 已完成架构设计\n\n产物：\n\n- `docs/issues/{number}/architecture.md`\n\n请确认是否进入项目计划阶段。\n\n确认方式：\n\n`/approve architecture`\n\n如需驳回，请评论：\n\n`/reject architecture 你的原因`\n""",\n        )\n\n        remove_label(number, "stage:architecture")\n        add_label(number, "stage:waiting-architecture-approval")\n        add_label(number, "agent:architecture")\n\n        print(f"[Architecture Agent] Issue #{number} 处理完成")\n\n\ndef handle_architecture_approval():\n    issues = list_issues_by_label("stage:waiting-architecture-approval")\n\n    for issue in issues:\n        number = issue["number"]\n\n        if has_comment_command(number, "/approve architecture"):\n            remove_label(number, "stage:waiting-architecture-approval")\n            add_label(number, "stage:pm-planning")\n\n            comment_issue(\n                number,\n                "已收到架构确认，进入项目管理 Agent 拆分开发计划。",\n            )\n\n            print(f"[Approval] Issue #{number} 架构已确认")\n\n\ndef handle_pm_planning():\n    issues = list_issues_by_label("stage:pm-planning")\n\n    for issue in issues:\n        number = issue["number"]\n        title = issue["title"]\n\n        prd = read_issue_doc(number, "prd.md")\n        architecture = read_issue_doc(number, "architecture.md")\n\n        prompt = read_prompt("pm.md")\n\n        user_input = f"""\nIssue 标题：\n{title}\n\nPRD：\n{prd}\n\n架构设计：\n{architecture}\n"""\n\n        print(f"[PM Agent] 开始处理 Issue #{number}: {title}")\n\n        plan = call_llm(prompt, user_input)\n\n        save_issue_doc(number, "plan.md", plan)\n\n        commit_all(f"docs: add development plan for issue #{number}")\n\n        comment_issue(\n            number,\n            f"""## 项目管理 Agent 已完成开发计划\n\n产物：\n\n- `docs/issues/{number}/plan.md`\n\n请确认是否进入开发执行阶段。\n\n确认方式：\n\n`/approve plan`\n\n如需驳回，请评论：\n\n`/reject plan 你的原因`\n""",\n        )\n\n        remove_label(number, "stage:pm-planning")\n        add_label(number, "stage:waiting-plan-approval")\n        add_label(number, "agent:pm")\n\n        print(f"[PM Agent] Issue #{number} 处理完成")\n\n\ndef handle_plan_approval():\n    issues = list_issues_by_label("stage:waiting-plan-approval")\n\n    for issue in issues:\n        number = issue["number"]\n\n        if has_comment_command(number, "/approve plan"):\n            remove_label(number, "stage:waiting-plan-approval")\n            add_label(number, "stage:ready-for-dev")\n\n            comment_issue(\n                number,\n                "已收到开发计划确认。下一阶段进入 Coding Agent，先生成代码文件方案，等待 `/approve patch` 后再写入项目。",\n            )\n\n            print(f"[Approval] Issue #{number} 开发计划已确认")\n\n\ndef handle_ready_for_dev():\n    issues = list_issues_by_label("stage:ready-for-dev")\n\n    for issue in issues:\n        number = issue["number"]\n        title = issue["title"]\n\n        prd = read_issue_doc(number, "prd.md")\n        architecture = read_issue_doc(number, "architecture.md")\n        plan = read_issue_doc(number, "plan.md")\n        tree = scan_project_tree()\n        files = read_small_project_files()\n\n        prompt = read_prompt("coding.md")\n\n        user_input = f"""\nIssue 标题：\n{title}\n\nPRD：\n{prd}\n\n架构设计：\n{architecture}\n\n开发计划：\n{plan}\n\n当前项目结构：\n{tree}\n\n部分项目文件内容：\n{files}\n"""\n\n        print(f"[Coding Agent] 开始生成代码方案 Issue #{number}: {title}")\n\n        output = call_llm(prompt, user_input)\n\n        save_issue_doc(number, "coding-output.json", output)\n\n        commit_all(f"docs: add coding output for issue #{number}")\n\n        comment_issue(\n            number,\n            f"""## Coding Agent 已生成代码文件方案\n\n产物：\n\n- `docs/issues/{number}/coding-output.json`\n\n请先检查该文件中即将写入/修改的文件列表。\n\n确认写入项目代码，请评论：\n\n`/approve patch`\n\n如需驳回，请评论：\n\n`/reject patch 你的原因`\n""",\n        )\n\n        remove_label(number, "stage:ready-for-dev")\n        add_label(number, "stage:waiting-patch-approval")\n        add_label(number, "agent:coding")\n\n        print(f"[Coding Agent] Issue #{number} 代码方案生成完成")\n\n\ndef handle_patch_approval():\n    issues = list_issues_by_label("stage:waiting-patch-approval")\n\n    for issue in issues:\n        number = issue["number"]\n\n        if not has_comment_command(number, "/approve patch"):\n            continue\n\n        print(f"[Coding Agent] 开始写入代码 Issue #{number}")\n\n        ensure_issue_branch(number)\n        data, written = write_files_from_agent_json(\n            number,\n            "coding-output.json",\n            f"feat: implement issue #{number}",\n        )\n\n        report = f"""# Coding 写入报告\n\n## 写入文件\n\n{chr(10).join(f"- {p}" for p in written)}\n\n## 说明\n\n{data.get("summary", "")}\n\n## Notes\n\n{chr(10).join(f"- {n}" for n in data.get("notes", []))}\n"""\n        save_issue_doc(number, "coding-report.md", report)\n        commit_all(f"docs: add coding report for issue #{number}")\n\n        comment_issue(\n            number,\n            f"""## Coding Agent 已写入代码\n\n产物：\n\n- `docs/issues/{number}/coding-report.md`\n\n已写入文件：\n\n{chr(10).join(f"- `{p}`" for p in written)}\n\n下一步进入 Testing Agent。\n""",\n        )\n\n        remove_label(number, "stage:waiting-patch-approval")\n        add_label(number, "stage:testing")\n\n\ndef handle_testing():\n    issues = list_issues_by_label("stage:testing")\n\n    for issue in issues:\n        number = issue["number"]\n        title = issue["title"]\n\n        prd = read_issue_doc(number, "prd.md")\n        architecture = read_issue_doc(number, "architecture.md")\n        plan = read_issue_doc(number, "plan.md")\n        tree = scan_project_tree()\n        files = read_small_project_files()\n\n        prompt = read_prompt("testing.md")\n\n        user_input = f"""\nIssue 标题：\n{title}\n\nPRD：\n{prd}\n\n架构设计：\n{architecture}\n\n开发计划：\n{plan}\n\n当前项目结构：\n{tree}\n\n部分项目文件内容：\n{files}\n"""\n\n        print(f"[Testing Agent] 开始生成测试 Issue #{number}: {title}")\n\n        output = call_llm(prompt, user_input)\n        save_issue_doc(number, "testing-output.json", output)\n        commit_all(f"docs: add testing output for issue #{number}")\n\n        ensure_issue_branch(number)\n        data, written = write_files_from_agent_json(\n            number,\n            "testing-output.json",\n            f"test: add tests for issue #{number}",\n        )\n\n        commands = data.get("commands") or []\n        if not isinstance(commands, list):\n            commands = []\n\n        results = run_safe_commands(commands)\n\n        report = {\n            "summary": data.get("summary", ""),\n            "written_files": written,\n            "commands": results,\n            "notes": data.get("notes", []),\n        }\n\n        save_issue_doc(\n            number,\n            "test-report.md",\n            "# 测试报告\\n\\n```json\\n"\n            + json.dumps(report, ensure_ascii=False, indent=2)\n            + "\\n```\\n",\n        )\n\n        commit_all(f"docs: add test report for issue #{number}")\n\n        comment_issue(\n            number,\n            f"""## Testing Agent 已完成测试处理\n\n产物：\n\n- `docs/issues/{number}/testing-output.json`\n- `docs/issues/{number}/test-report.md`\n\n下一步进入 Review Agent。\n""",\n        )\n\n        remove_label(number, "stage:testing")\n        add_label(number, "stage:reviewing")\n        add_label(number, "agent:testing")\n\n        print(f"[Testing Agent] Issue #{number} 测试完成")\n\n\ndef handle_reviewing():\n    issues = list_issues_by_label("stage:reviewing")\n\n    for issue in issues:\n        number = issue["number"]\n        title = issue["title"]\n\n        prd = read_issue_doc(number, "prd.md")\n        architecture = read_issue_doc(number, "architecture.md")\n        plan = read_issue_doc(number, "plan.md")\n        test_report = read_issue_doc(number, "test-report.md")\n        diff = get_git_diff()\n\n        prompt = read_prompt("review.md")\n\n        user_input = f"""\nIssue 标题：\n{title}\n\nPRD：\n{prd}\n\n架构设计：\n{architecture}\n\n开发计划：\n{plan}\n\n测试报告：\n{test_report}\n\nGit Diff：\n{diff}\n"""\n\n        print(f"[Review Agent] 开始 Review Issue #{number}: {title}")\n\n        report = call_llm(prompt, user_input)\n\n        save_issue_doc(number, "review-report.md", report)\n        commit_all(f"docs: add review report for issue #{number}")\n\n        comment_issue(\n            number,\n            f"""## Review Agent 已完成代码审查\n\n产物：\n\n- `docs/issues/{number}/review-report.md`\n\n下一步进入 DevOps Agent。\n""",\n        )\n\n        remove_label(number, "stage:reviewing")\n        add_label(number, "stage:devops")\n        add_label(number, "agent:review")\n\n        print(f"[Review Agent] Issue #{number} Review 完成")\n\n\ndef handle_devops():\n    issues = list_issues_by_label("stage:devops")\n\n    for issue in issues:\n        number = issue["number"]\n        title = issue["title"]\n\n        prd = read_issue_doc(number, "prd.md")\n        architecture = read_issue_doc(number, "architecture.md")\n        plan = read_issue_doc(number, "plan.md")\n        review_report = read_issue_doc(number, "review-report.md")\n        tree = scan_project_tree()\n        files = read_small_project_files()\n\n        prompt = read_prompt("devops.md")\n\n        user_input = f"""\nIssue 标题：\n{title}\n\nPRD：\n{prd}\n\n架构设计：\n{architecture}\n\n开发计划：\n{plan}\n\nReview 报告：\n{review_report}\n\n当前项目结构：\n{tree}\n\n部分项目文件内容：\n{files}\n"""\n\n        print(f"[DevOps Agent] 开始生成部署文件 Issue #{number}: {title}")\n\n        output = call_llm(prompt, user_input)\n        save_issue_doc(number, "devops-output.json", output)\n        commit_all(f"docs: add devops output for issue #{number}")\n\n        ensure_issue_branch(number)\n        data, written = write_files_from_agent_json(\n            number,\n            "devops-output.json",\n            f"chore: add devops files for issue #{number}",\n        )\n\n        report = f"""# DevOps 报告\n\n## 部署概要\n\n{data.get("summary", "")}\n\n## 写入文件\n\n{chr(10).join(f"- {p}" for p in written)}\n\n## 建议命令\n\n{chr(10).join(f"- {c}" for c in data.get("commands", []))}\n\n## 注意事项\n\n{chr(10).join(f"- {n}" for n in data.get("notes", []))}\n"""\n        save_issue_doc(number, "deploy-report.md", report)\n        commit_all(f"docs: add deploy report for issue #{number}")\n\n        comment_issue(\n            number,\n            f"""## DevOps Agent 已完成部署文件生成\n\n产物：\n\n- `docs/issues/{number}/deploy-report.md`\n\n已写入文件：\n\n{chr(10).join(f"- `{p}`" for p in written)}\n\n当前分支：\n\n`agent/issue-{number}`\n\n请人工检查后创建 PR 或执行：\n\n`gh pr create --fill`\n""",\n        )\n\n        remove_label(number, "stage:devops")\n        add_label(number, "stage:ready-for-pr")\n        add_label(number, "agent:devops")\n\n        print(f"[DevOps Agent] Issue #{number} DevOps 完成")\n\n\ndef main():\n    check_config()\n\n    # 第一阶段\n    handle_intake()\n    handle_architecture()\n    handle_architecture_approval()\n    handle_pm_planning()\n    handle_plan_approval()\n\n    # 第二阶段\n    handle_ready_for_dev()\n    handle_patch_approval()\n    handle_testing()\n    handle_reviewing()\n    handle_devops()\n\n\nif __name__ == "__main__":\n    main()\n'


def run_cmd(cmd, cwd=None, check=False):
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        shell=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"命令失败: {' '.join(cmd)}\n{result.stderr}")
    return result


def backup_file(path: Path):
    if not path.exists():
        return None
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_suffix(path.suffix + f".bak_{ts}")
    shutil.copy2(path, backup)
    return backup


def write_text_with_backup(path: Path, content: str, overwrite: bool = True):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and overwrite:
        backup = backup_file(path)
        print(f"[BACKUP] {path} -> {backup}")
    if not path.exists() or overwrite:
        path.write_text(content, encoding="utf-8")
        print(f"[WRITE] {path}")


def parse_env(env_path: Path):
    data = {}
    if not env_path.exists():
        return data
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if not line or line.strip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip()
    return data


def upsert_env_value(env_path: Path, key: str, value: str):
    lines = []
    found = False

    if env_path.exists():
        lines = env_path.read_text(encoding="utf-8").splitlines()

    new_lines = []
    for line in lines:
        if line.startswith(key + "="):
            new_lines.append(f"{key}={value}")
            found = True
        else:
            new_lines.append(line)

    if not found:
        new_lines.append(f"{key}={value}")

    env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"[ENV] {key}={value}")


def create_labels(owner: str, repo: str):
    labels = [
        ("stage:waiting-patch-approval", "fbca04", "等待 patch 写入确认"),
        ("stage:testing", "006b75", "测试 Agent 处理中"),
        ("stage:reviewing", "d93f0b", "Review Agent 处理中"),
        ("stage:devops", "1d76db", "DevOps Agent 处理中"),
        ("stage:ready-for-pr", "0e8a16", "准备创建 PR"),
        ("agent:coding", "5319e7", "Coding Agent"),
        ("agent:testing", "006b75", "Testing Agent"),
        ("agent:review", "d93f0b", "Review Agent"),
        ("agent:devops", "1d76db", "DevOps Agent"),
    ]

    if shutil.which("gh") is None:
        print("[WARN] 未找到 gh，跳过 GitHub Labels 创建。")
        return

    for name, color, desc in labels:
        result = run_cmd([
            "gh", "label", "create", name,
            "--repo", f"{owner}/{repo}",
            "--color", color,
            "--description", desc,
        ])
        if result.returncode == 0:
            print(f"[LABEL] created {name}")
        else:
            stderr = result.stderr.strip()
            if "already exists" in stderr or "Name already exists" in stderr:
                print(f"[LABEL] exists {name}")
            else:
                print(f"[WARN] label 创建失败 {name}: {stderr}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-root", default=".", help="local-ai-dev-agents 根目录，默认当前目录")
    parser.add_argument("--target-repo", default=DEFAULT_TARGET_REPO, help="目标项目目录")
    parser.add_argument("--owner", default=None, help="GitHub owner，不传则读取 .env")
    parser.add_argument("--repo", default=None, help="GitHub repo，不传则读取 .env")
    parser.add_argument("--skip-labels", action="store_true", help="跳过 GitHub label 创建")
    args = parser.parse_args()

    agent_root = Path(args.agent_root).resolve()
    target_repo = Path(args.target_repo).resolve()

    if not agent_root.exists():
        raise RuntimeError(f"Agent 根目录不存在: {agent_root}")

    if not target_repo.exists():
        raise RuntimeError(f"目标项目目录不存在: {target_repo}")

    env_path = agent_root / ".env"
    env_data = parse_env(env_path)

    owner = args.owner or env_data.get("GITHUB_OWNER")
    repo = args.repo or env_data.get("GITHUB_REPO")

    print(f"[INFO] Agent Root: {agent_root}")
    print(f"[INFO] Target Repo: {target_repo}")

    upsert_env_value(env_path, "TARGET_REPO_PATH", str(target_repo))

    write_text_with_backup(agent_root / "prompts" / "coding.md", CODING_PROMPT)
    write_text_with_backup(agent_root / "prompts" / "testing.md", TESTING_PROMPT)
    write_text_with_backup(agent_root / "prompts" / "review.md", REVIEW_PROMPT)
    write_text_with_backup(agent_root / "prompts" / "devops.md", DEVOPS_PROMPT)

    write_text_with_backup(agent_root / "orchestrator" / "main.py", ORCHESTRATOR_STAGE2)

    if not args.skip_labels:
        if owner and repo:
            create_labels(owner, repo)
        else:
            print("[WARN] 没有 GITHUB_OWNER / GITHUB_REPO，跳过 label 创建。")

    print("\n[DONE] 第二阶段升级完成。")
    print("\n下一步：")
    print(f"  cd {agent_root}")
    print("  .\\.venv\\Scripts\\Activate.ps1")
    print("  python orchestrator\\main.py")
    print("\n如果当前 Issue 已经是 stage:ready-for-dev，运行后会进入 Coding Agent，生成 coding-output.json。")
    print("检查无误后，在 Issue 评论：/approve patch")
    print("然后再次运行：python orchestrator\\main.py")


if __name__ == "__main__":
    main()
