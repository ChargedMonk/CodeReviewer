import os
import shutil
import sys
from pathlib import Path
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from code_reviewer.reviewer import run_diff_review


def init_global_hook():
    print("🔧 Setting up global Git hook...")

    os.system("git config --global core.hooksPath ~/.git-hooks")

    hooks_dir = Path.home() / ".git-hooks"
    hooks_dir.mkdir(exist_ok=True)

    script_src = Path(__file__).parent.parent / "hooks" / "pre-commit"
    script_dst = hooks_dir / "pre-commit"

    print(f"Copying pre-commit hook from {script_src} to {script_dst}")
    shutil.copy(script_src, script_dst)
    script_dst.chmod(0o755)

    print(f"✅ Global pre-commit hook installed at {script_dst}")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            init_global_hook()
        elif sys.argv[1] == "--diff" and len(sys.argv) > 3:
            run_diff_review(Path(sys.argv[2]), Path(sys.argv[3]))
        else:
            print("❌ Unknown command. Use:\n  code-reviewer init\n  code-reviewer --diff <patch_file>")
    else:
        print("ℹ️  Usage:\n  code-reviewer init\n  code-reviewer --diff <patch_file>")
