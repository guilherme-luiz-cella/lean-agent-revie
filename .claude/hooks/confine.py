"""Keep Claude Code (and every board agent) inside this repository. PreToolUse hook, stdlib only.
Blocks (exit code 2, reason on stderr):
- file tools (Read, Edit, Write, Glob, Grep, NotebookEdit) on any path outside the project folder;
- shell commands that mention another drive (D: to Z:), a network share (\\\\server), the Git Bash
  form of a drive (//p/) or AppData.
Copy it with .claude/settings.json into any repo that holds or sits near personal data.
Bash and PowerShell commands get the same check.
Tested by tests/confine_test.py. A guard rail, not a sandbox: obfuscated commands are not caught.
"""
import json, os, re, sys

SHELL_BLOCK = re.compile(r"(?<![A-Za-z])[d-zD-Z]:[\\/]?|\\\\[^\\\s]|//[d-z]/|appdata", re.I)

def block(why):
    print(f"Blocked by the repo's confinement rule (CLAUDE.md): {why}", file=sys.stderr)
    sys.exit(2)

def main():
    d = json.load(sys.stdin)
    root = os.path.normcase(os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or d.get("cwd") or "."))
    tool, ti = d.get("tool_name", ""), d.get("tool_input") or {}
    if tool in ("Bash", "PowerShell"):
        if SHELL_BLOCK.search(ti.get("command", "")):
            block("the command mentions another drive, a network share or AppData.")
        return
    for key in ("file_path", "path", "notebook_path"):
        p = ti.get(key)
        if not p:
            continue
        if os.name != "nt" and re.match(r"^([A-Za-z]:|\\\\|//)", p):
            block(f"{p} is a drive or share outside this repository.")
        full = os.path.normcase(os.path.realpath(os.path.join(root, p)))
        try:
            inside = os.path.commonpath([full, root]) == root
        except ValueError:                            # another drive
            inside = False
        if not inside:
            block(f"{p} is outside this repository.")

if __name__ == "__main__":
    main()
