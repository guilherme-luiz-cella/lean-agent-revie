"""Checks .claude/hooks/confine.py: outside the repo is blocked, normal work passes.
    py tests/confine_test.py
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(ROOT, ".claude", "hooks", "confine.py")
CASES = [
    ("Read", {"file_path": "README.md"}, False),
    ("Read", {"file_path": ".claude/agents/scout.md"}, False),
    ("Edit", {"file_path": os.path.join(ROOT, "protocol.md")}, False),
    ("Grep", {"path": "personas"}, False),
    ("Bash", {"command": "git status"}, False),
    ("Bash", {"command": "python tests/confine_test.py"}, False),
    ("Read", {"file_path": "../folder-graph/app.py"}, True),
    ("Read", {"file_path": "/etc/passwd"}, True),
    ("Read", {"file_path": "P:\\Projetos\\x.prw"}, True),
    ("Glob", {"path": "\\\\servidor\\share"}, True),
    ("Bash", {"command": "dir P:\\"}, True),
    ("Bash", {"command": "type \\\\servidor\\share\\a.txt"}, True),
    ("Bash", {"command": "ls //p/Projetos"}, True),
    ("Bash", {"command": "Get-Content $env:APPDATA\\x"}, True),
    ("PowerShell", {"command": "git status"}, False),
    ("PowerShell", {"command": "Get-ChildItem P:\\"}, True),
    ("PowerShell", {"command": "Get-Content $env:APPDATA\\x"}, True),
]
fails = []
for tool, ti, want in CASES:
    r = subprocess.run([sys.executable, HOOK], input=json.dumps({"tool_name": tool, "tool_input": ti, "cwd": ROOT}),
                       capture_output=True, text=True, env=dict(os.environ, CLAUDE_PROJECT_DIR=ROOT))
    if (r.returncode == 2) != want:
        fails.append(f"{'should block' if want else 'should allow'}: {tool} {ti}")

# The hook must work from any folder (a relative path broke it after a cd) and cover PowerShell.
with open(os.path.join(ROOT, ".claude", "settings.json"), encoding="utf-8") as f:
    hook = json.load(f)["hooks"]["PreToolUse"][0]
if "$CLAUDE_PROJECT_DIR" not in hook["hooks"][0]["command"]:
    fails.append("settings.json: hook path must start with $CLAUDE_PROJECT_DIR")
if "PowerShell" not in hook["matcher"].split("|"):
    fails.append("settings.json: matcher must include PowerShell")
print("\n".join(fails) if fails else f"OK: {len(CASES)} cases + settings")
sys.exit(1 if fails else 0)
