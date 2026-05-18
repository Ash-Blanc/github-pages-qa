# Two-Way Sync Pattern

## Core Principle

The Q&A panel uses the repository itself as the database. `site/qa.json` is the single source of truth.

## Flow

### Chat → Site (Primary direction during research)
1. Valuable exchange occurs in Hermes session
2. Skill extracts clean Q/A pair
3. Appends to `site/qa.json`
4. Commits with clear message
5. GitHub Pages automatically reflects the change (or user triggers manual deploy)

### Site → Chat (Reverse direction)
1. Visitor uses "Suggest question" form on the live site
2. Form either:
   - Creates a GitHub Issue, or
   - Appends to a `pending-suggestions.json` file
3. Next time the skill runs `sync`, it can surface these suggestions in the current Hermes session for review

## Why This Works Well

- Zero external services required
- Full version history of every Q&A entry
- Works offline and in air-gapped environments
- Extremely simple to implement and debug
- Naturally fits into existing git-based workflows

## Implementation Notes

- Keep `qa.json` as a flat array of objects: `{ "q": string, "a": string }`
- Frontend should be pure client-side (no build step)
- Use Tailwind via CDN for zero-dependency deployment
- Make the panel collapsible/searchable for good UX
