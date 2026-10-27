import subprocess
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent / "git_demo_repo"

def run(*args, check=True):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    print("$", " ".join(args))
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip())
    if check and result.returncode:
        raise SystemExit(result.returncode)
    return result

if ROOT.exists():
    shutil.rmtree(ROOT)
ROOT.mkdir(parents=True)
subprocess.run(["git", "init", "-b", "main"], cwd=ROOT, check=True, capture_output=True)
subprocess.run(["git", "config", "user.name", "Nitya Parmar"], cwd=ROOT, check=True)
subprocess.run(["git", "config", "user.email", "nitya@example.com"], cwd=ROOT, check=True)

(ROOT / "README.md").write_text("# University Document Sharing Platform\n")
(ROOT / "login.html").write_text("<h1>University Document Sharing Platform</h1>\n")
run("git", "add", ".")
run("git", "commit", "-m", "Initial project files")

run("git", "checkout", "-b", "feature/login-page")
(ROOT / "login.html").write_text("<h1>University Document Sharing Platform</h1>\n<p>Login page skeleton</p>\n")
run("git", "add", "login.html")
run("git", "commit", "-m", "Add login page skeleton")
run("git", "checkout", "main")

run("git", "checkout", "-b", "feature/login-validation")
(ROOT / "login.html").write_text("<h1>University Student Portal — Secure Login</h1>\n")
run("git", "add", "login.html")
run("git", "commit", "-m", "Update login heading for validation branch")
run("git", "checkout", "main")

# Merge the first feature branch, as if PR 1 had been accepted locally.
run("git", "merge", "--no-ff", "feature/login-page", "-m", "Merge feature/login-page")
# Merging the second branch causes a real conflict in the shared heading line.
conflict = run("git", "merge", "--no-ff", "feature/login-validation", "-m", "Merge feature/login-validation", check=False)
if conflict.returncode == 0:
    print("Unexpected: conflict did not occur.")
    raise SystemExit(1)
print("\\n--- CONFLICT MARKERS (expected during the demo) ---")
print((ROOT / "login.html").read_text().rstrip())

(ROOT / "login.html").write_text("<h1>University Document Sharing Platform — Secure Login</h1>\n<p>Login page skeleton</p>\n")
run("git", "add", "login.html")
run("git", "commit", "-m", "Resolve login heading merge conflict")
print("\\n--- FINAL COMMIT GRAPH ---")
run("git", "log", "--graph", "--oneline", "--all", "--decorate")
print("\\nDemo complete. This is local Git evidence only; no GitHub PRs were created.")
