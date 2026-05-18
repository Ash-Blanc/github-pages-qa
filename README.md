# github-pages-qa

A reusable **Hermes Skill** that turns any GitHub repository into a clean, living documentation site with a **two-way synced Q&A panel**.

## What it does

- Auto-generates a modern GitHub Pages site from your `README.md` + `docs/` folder
- Maintains a version-controlled `qa.json` as the single source of truth for research Q&A
- Enables **two-way sync**:
  - Chat → Site: New valuable exchanges from Hermes sessions are synced to the live site
  - Site → Chat: Visitors can suggest questions that become GitHub issues for review
- Can spawn dedicated Q&A maintenance Hermes sessions using the free Nous model

## Installation

```bash
# Clone the skill
git clone https://github.com/Ash-Blanc/github-pages-qa.git ~/.hermes/skills/github-pages-qa
```

## Usage

### Via Hermes
```bash
hermes skill run github-pages-qa init --repo "My Project"
hermes skill run github-pages-qa sync --pairs '[{"q": "...", "a": "..."}]'
hermes skill run github-pages-qa start-qa-session
```

### Standalone CLI
```bash
python cli.py init --repo "My Project"
python cli.py sync --pairs '[{"q":"...","a":"..."}]'
python cli.py suggest "How does the IR work?"
python cli.py start-qa-session
```

## Two-Way Sync Flow

1. During research sessions, important Q&A is collected
2. `sync` command updates `qa.json` and auto-commits + pushes
3. The live site displays the Q&A panel (powered by `qa.json`)
4. Visitors can suggest new questions via the site
5. Suggestions are converted into GitHub issues for easy review

## Hackathon Submission

This skill was built for the **Hermes Agent Challenge** on dev.to.

It demonstrates:
- Protocol-driven modular documentation
- Persistent, version-controlled knowledge via `qa.json`
- Seamless integration between Hermes chat sessions and static sites
- Easy spawning of specialized agents for ongoing maintenance

## License

MIT License

## Author

Ashwin (hermey) — Agentra Labs

## Related Projects

- [program-benchmaxxing](https://github.com/Ash-Blanc/program-benchmaxxing) — Original research project that inspired this skill
