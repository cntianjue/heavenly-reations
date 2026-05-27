# D:\work\project\Pipeline\heavenly-reations

本项目由 `setup_local_agents.py` 自动生成。

## 运行方式

```powershell
cd D:\work\project\Pipeline\heavenly-reations
.\.venv\Scripts\Activate.ps1
python orchestrator\main.py
```

## 当前最小闭环

GitHub Issue → Product Agent → Architecture Agent → 人工确认 → PM Agent → 人工确认。

## 人工确认指令

在 GitHub Issue 评论：

```text
/approve architecture
```

然后本地运行：

```powershell
python orchestrator\main.py
```

之后等 PM Agent 输出计划，再评论：

```text
/approve plan
```
