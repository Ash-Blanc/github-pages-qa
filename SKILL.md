---
name: github-pages-qa
description: Generate and maintain GitHub Pages sites with two-way synced Q&A panels for any repository. Supports auto site generation, GitHub issue creation, and dedicated Hermes Q&A sessions.
version: 0.2.0
author: Ashwin (hermey)
tags: [github-pages, qa, documentation, hermes-skill, hackathon]
---

# github-pages-qa

Production-grade Hermes skill that turns any GitHub repository into a living documentation site with a **two-way synced Q&A panel**.

## Features

- Auto-generates a clean GitHub Pages site from `README.md` + `docs/`
- Maintains `qa.json` as the single source of truth for Q&A
- **Chat → Site**: Syncs valuable exchanges from Hermes sessions into the live site
- **Site → Chat**: Suggestions from the site create GitHub issues for review
- Can spawn dedicated Q&A maintenance sessions using the free Nous model

## Commands

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

1. During research, good questions/answers are collected.
2. `sync` command updates `qa.json` and auto-commits + pushes.
3. Visitors can suggest questions from the live site.
4. Suggestions are turned into GitHub issues (or queued in `pending_questions.md`).
5. The skill can later pull suggestions into the current Hermes session.

## Hackathon Context

Submitted to the Hermes Agent Challenge (dev.to). Demonstrates:
- Protocol-driven modular documentation
- Persistent, version-controlled knowledge (via `qa.json`)
- Seamless integration between chat sessions and static sites
- Easy spawning of specialized agents

## Future Work

- Richer content extraction from docs
- Better GitHub integration (PRs instead of issues)
- Full multi-model support in Q&A sessions

## Files

- `SKILL.md`
- `main.py`
- `templates/`
- `README.md`