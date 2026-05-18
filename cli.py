#!/usr/bin/env python3
"""
CLI wrapper for github-pages-qa skill.
Allows standalone usage: `python cli.py init --repo "MyProject"`
"""

import argparse
import sys
from main import init_site, sync_qa, start_qa_session, create_github_issue_for_suggestion


def main():
    parser = argparse.ArgumentParser(description="github-pages-qa - GitHub Pages + 2-way Q&A skill")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = subparsers.add_parser("init", help="Initialize GitHub Pages site")
    p_init.add_argument("--repo", default="Repository", help="Repository name")

    # sync
    p_sync = subparsers.add_parser("sync", help="Sync new Q&A pairs")
    p_sync.add_argument("--pairs", required=True, help="JSON array of {q, a} objects")

    # suggest
    p_suggest = subparsers.add_parser("suggest", help="Create GitHub issue from suggestion")
    p_suggest.add_argument("question", help="Suggested question")

    # start-session
    subparsers.add_parser("start-qa-session", help="Start dedicated Q&A Hermes session")

    args = parser.parse_args()

    if args.command == "init":
        init_site(args.repo)
    elif args.command == "sync":
        import json
        pairs = json.loads(args.pairs)
        sync_qa(pairs)
    elif args.command == "suggest":
        create_github_issue_for_suggestion(args.question)
    elif args.command == "start-qa-session":
        start_qa_session()


if __name__ == "__main__":
    main()