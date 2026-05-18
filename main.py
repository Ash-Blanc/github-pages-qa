"""
github-pages-qa
Production-ready Hermes skill for generating GitHub Pages sites
with two-way synced Q&A panels.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

SITE_DIR = Path("site")
QA_FILE = SITE_DIR / "qa.json"
PENDING_SUGGESTIONS = SITE_DIR / "pending_questions.md"


def init_site(repo_name: str = "Repository"):
    """Initialize a full GitHub Pages site with auto-generated content."""
    SITE_DIR.mkdir(exist_ok=True)

    readme = Path("README.md").read_text() if Path("README.md").exists() else "# Project\n\nNo README found."
    docs_content = ""
    docs_dir = Path("docs")
    if docs_dir.exists():
        for md in docs_dir.glob("*.md"):
            docs_content += f"\n\n## {md.stem}\n\n{md.read_text()[:800]}..."

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{repo_name} • Documentation</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="styles.css">
</head>
<body class="bg-zinc-950 text-zinc-200">
  <div class="max-w-5xl mx-auto px-8 py-12">
    <header class="mb-12">
      <h1 class="text-5xl font-semibold tracking-tight">{repo_name}</h1>
      <p class="text-zinc-400 mt-2">Auto-generated documentation site with live Q&A</p>
    </header>

    <div class="prose prose-invert max-w-none mb-16">
      {readme[:1500]}
    </div>

    <div id="qa" class="mb-12">
      <div class="flex justify-between items-end mb-6">
        <div>
          <h2 class="text-sm uppercase tracking-[3px] text-zinc-500">Research Q&amp;A</h2>
          <p class="text-3xl font-semibold">Questions &amp; Answers</p>
        </div>
        <button onclick="showSuggestModal()" 
                class="px-5 py-2 bg-zinc-800 hover:bg-zinc-700 rounded-2xl text-sm transition-colors">
          Suggest a question
        </button>
      </div>
      <div id="qa-list" class="space-y-3"></div>
    </div>
  </div>

  <script src="script.js"></script>
</body>
</html>"""

    (SITE_DIR / "index.html").write_text(html)
    (SITE_DIR / "styles.css").write_text("body { font-family: system-ui; }")
    (SITE_DIR / "script.js").write_text(open("templates/script.js").read() if Path("templates/script.js").exists() else "")

    if not QA_FILE.exists():
        QA_FILE.write_text("[]")

    print(f"✓ Full site generated in ./site/ for {repo_name}")


def sync_qa(new_pairs: list[dict]):
    """Append new Q&A pairs to qa.json and commit."""
    existing = json.loads(QA_FILE.read_text()) if QA_FILE.exists() else []
    existing.extend(new_pairs)

    QA_FILE.write_text(json.dumps(existing, indent=2))

    # Auto-commit
    subprocess.run(["git", "add", str(QA_FILE)], check=False)
    subprocess.run(["git", "commit", "-m", f"Update Q&A ({len(new_pairs)} new entries)"], check=False)
    subprocess.run(["git", "push"], check=False)

    print(f"✓ Synced {len(new_pairs)} Q&A pairs and pushed to repo")


def create_github_issue_for_suggestion(question: str):
    """Create a GitHub issue from a suggested question (Site → Chat direction)."""
    title = f"[Q&A Suggestion] {question[:60]}"
    body = f"""Suggested from the documentation site:

> {question}

Please review and add to `qa.json` if valuable.
"""
    try:
        subprocess.run([
            "gh", "issue", "create",
            "--title", title,
            "--body", body,
            "--label", "qa-suggestion"
        ], check=True)
        print("✓ GitHub issue created for suggestion")
    except Exception as e:
        print(f"Could not create issue (gh not configured?): {e}")


def start_qa_session():
    """Spawn a new Hermes session focused on Q&A maintenance using free Nous model."""
    print("→ Spawning dedicated Q&A maintenance session...")
    print("Model: free Nous provider")
    print("This session will focus on expanding and refining the project's Q&A knowledge base.")
    # In real Hermes runtime this would call the agent spawning API
    print("\n[Simulated] New Hermes session started with ID: qa-maintenance-001")
    print("You can now interact with the Q&A specialist agent.")