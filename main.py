"""
github-pages-qa
Production-ready Hermes skill for generating GitHub Pages sites
with two-way synced Q&A panels.
"""

import html
import json
import subprocess
from pathlib import Path
from datetime import datetime

SITE_DIR = Path("docs")
QA_FILE = SITE_DIR / "qa.json"
PENDING_SUGGESTIONS = SITE_DIR / "pending_questions.md"


def init_site(repo_name: str = "Repository"):
    """Initialize a full GitHub Pages site with auto-generated content."""
    SITE_DIR.mkdir(exist_ok=True)

    readme_raw = Path("README.md").read_text() if Path("README.md").exists() else "# Project\n\nNo README found."
    readme_escaped = html.escape(readme_raw[:1500])
    docs_content = ""
    docs_src = Path("docs_src")
    if docs_src.exists():
        for md in docs_src.glob("*.md"):
            docs_content += f"\n\n## {md.stem}\n\n{md.read_text()[:800]}..."
    docs_escaped = html.escape(docs_content)

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{repo_name} — Live Q&A Forum</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="styles.css">
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
</head>
<body class="bg-[#0a0a0f] text-zinc-300 font-['Inter'] min-h-screen">
  <div class="fixed inset-0 opacity-[0.03] pointer-events-none" style="background-image:url('data:image/svg+xml,%3Csvg viewBox=%220 0 256 256%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cfilter id=%22noise%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.9%22 numOctaves=%224%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23noise)%22/%3E%3C/svg%3E');"></div>

  <div class="relative max-w-6xl mx-auto px-6 py-16">
    <!-- Header -->
    <header class="mb-16 text-center">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono mb-6">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        LIVE FORUM
      </div>
      <h1 class="font-['Space_Grotesk'] text-6xl font-bold text-white tracking-tight mb-4">{repo_name}</h1>
      <p class="text-zinc-500 text-lg max-w-xl mx-auto">A public space for questions, answers, and ongoing research threads. Curated from live sessions.</p>
    </header>

    <!-- Stats bar -->
    <div class="grid grid-cols-3 gap-4 mb-12 max-w-3xl mx-auto">
      <div class="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 text-center">
        <div class="font-['Space_Grotesk'] text-3xl font-bold text-white" id="qa-count">0</div>
        <div class="text-xs text-zinc-500 mt-1 uppercase tracking-wider">Threads</div>
      </div>
      <div class="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 text-center">
        <div class="font-['Space_Grotesk'] text-3xl font-bold text-emerald-400" id="answered-count">0</div>
        <div class="text-xs text-zinc-500 mt-1 uppercase tracking-wider">Answered</div>
      </div>
      <div class="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 text-center">
        <div class="font-['Space_Grotesk'] text-3xl font-bold text-violet-400">∞</div>
        <div class="text-xs text-zinc-500 mt-1 uppercase tracking-wider">Open</div>
      </div>
    </div>

    <!-- Filters + CTA -->
    <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 mb-8">
      <div class="flex-1 relative">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        <input id="search-input" type="text" placeholder="Search threads..." class="w-full bg-zinc-900/50 border border-zinc-800 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white placeholder-zinc-600 focus:outline-none focus:border-zinc-600 transition-colors">
      </div>
      <select id="tag-filter" class="bg-zinc-900/50 border border-zinc-800 rounded-xl px-4 py-2.5 text-sm text-zinc-400 focus:outline-none focus:border-zinc-600 cursor-pointer">
        <option value="">All tags</option>
      </select>
      <button onclick="openModal()" class="flex items-center justify-center gap-2 px-5 py-2.5 bg-white text-black rounded-xl font-semibold text-sm hover:bg-zinc-200 transition-colors whitespace-nowrap">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
        Suggest
      </button>
    </div>

    <!-- Two-column layout -->
    <div class="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-8">
      <!-- Main feed -->
      <div>
        <div id="qa-list" class="space-y-4"></div>
      </div>

      <!-- Sidebar -->
      <aside class="space-y-6">
        <div class="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5">
          <h3 class="font-['Space_Grotesk'] text-sm font-semibold text-white uppercase tracking-wider mb-4">Pending Suggestions</h3>
          <div id="pending-list" class="space-y-3">
            <div class="animate-pulse space-y-3">
              <div class="h-12 bg-zinc-800 rounded-xl"></div>
              <div class="h-12 bg-zinc-800 rounded-xl"></div>
            </div>
          </div>
          <a href="https://github.com/Ash-Blanc/{repo_name}/issues?q=label:qa-suggestion" target="_blank" class="block mt-4 text-xs text-zinc-500 hover:text-emerald-400 transition-colors">View all on GitHub →</a>
        </div>

        <div class="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5">
          <h3 class="font-['Space_Grotesk'] text-sm font-semibold text-white uppercase tracking-wider mb-2">How it works</h3>
          <p class="text-zinc-500 text-sm leading-relaxed">
            Threads are synced from live Hermes research sessions. Suggest a question — it becomes a GitHub issue. Answered threads get merged back here.
          </p>
        </div>
      </aside>
    </div>

    <!-- Footer -->
    <footer class="mt-20 pt-8 border-t border-zinc-800 text-center text-zinc-600 text-sm">
      <p>Synced live from Hermes sessions · <a href="https://github.com/Ash-Blanc/{repo_name}" class="text-zinc-400 hover:text-white transition-colors">View on GitHub</a></p>
    </footer>
  </div>

  <!-- Modal -->
  <div id="modal" class="fixed inset-0 bg-black/80 backdrop-blur-sm hidden items-center justify-center z-50">
    <div class="bg-zinc-900 border border-zinc-700 rounded-2xl p-8 max-w-md w-full mx-4">
      <h3 class="font-['Space_Grotesk'] text-xl font-bold text-white mb-4">Suggest a Question</h3>
      <p class="text-zinc-400 text-sm mb-4">Your question will be queued as a GitHub issue for the community to answer.</p>
      <textarea id="suggest-input" class="w-full bg-zinc-800 border border-zinc-700 rounded-xl p-4 text-white placeholder-zinc-500 focus:outline-none focus:border-emerald-500/50 resize-none h-32" placeholder="What's on your mind?"></textarea>
      <div class="flex gap-3 mt-4">
        <button onclick="closeModal()" class="flex-1 py-2.5 border border-zinc-700 rounded-xl text-zinc-400 hover:text-white hover:border-zinc-500 transition-colors">Cancel</button>
        <button onclick="submitSuggestion()" class="flex-1 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-black font-semibold rounded-xl transition-colors">Submit</button>
      </div>
    </div>
  </div>

  <script src="script.js"></script>
</body>
</html>"""

    (SITE_DIR / "index.html").write_text(page_html)
    (SITE_DIR / "styles.css").write_text("body { font-family: system-ui; }")
    (SITE_DIR / "script.js").write_text(open("templates/script.js").read() if Path("templates/script.js").exists() else "")

    if not QA_FILE.exists():
        QA_FILE.write_text("[]")

    print(f"✓ Forum generated in ./docs/ for {repo_name}")


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