# aitherium.org — Aitherium Foundation

The foundation's site, and the home of the thesis: **no hyperscale**. The compute to
run frontier AI already exists, idle, on hardware people own; the missing layer is the
operating system that turns it into working agents and a safe way for an ordinary
machine to join. The site argues that with receipts, renders the public stack as a
periodic table, and links to the record instead of asserting credibility in prose.

## Pages

| Page | Purpose |
|---|---|
| `index.html` | The thesis in six sections: no hyperscale, the stack, doctrine, the operator, receipts, start |
| `about.html` | The thesis, long form |
| `programs.html` | The four programs: the stack, weights & the commons, the operator doctrine, the commons infrastructure |
| `transparency.html` | The record: what is inspectable, the licence map as it actually is, deployed versus specified |
| `get-involved.html` | Run a brain, run a node, contribute, the rooms, support |
| `news.html` | Points to blog.aitherium.com (one record, not two) plus selected posts |

## Design

Tokens come from the brand's content design system (`.ELEMENT/DESIGN.md` in the
platform monorepo): the void `#000103`, one cyan `#2AD7D7`, forge orange `#FF8950`
used once per page, Inter at thin display weights, JetBrains Mono for anything
measured. The periodic-table motif is the brand's own — Aitherium is element 0, "Ai",
The Element of Creation. No glass, no gradient text, no feature grids.

## Stack

Plain HTML + CSS + one small JS file (mobile nav, and the periodic table's detail
panel). Every page is complete with JavaScript off. **There is no build step at deploy
time.** `scripts/gen_pages.py` exists so the shared chrome cannot drift across six
files and so the brick table is rendered from a dated snapshot of the ecosystem
registry (`scripts/bricks.json`) rather than typed by hand; run it, commit the output.

## Deploy

```
scripts/publish.sh "message"
```

Syncs `main`'s tree onto `gh-pages`; GitHub's own builder publishes it at
`aitherium.org` (custom domain via `CNAME`, DNS from the monorepo's
`pages-cnames.yaml` lane). No Actions workflow, no runner dependency.

## Content rules

- Every external link points at a surface that answered 200 when it was added. The
  monorepo gate `check_org_site_links.py` re-probes the live site and denies hosts
  that serve the wrong thing (`docs.`, `status.`, `demo.`, `irc.`).
- Every number carries its date and its source. Re-measure; never edit a figure by hand.
- Nothing on this site claims what the record does not show. Where the record does not
  exist yet (financials, governance), the transparency page says so.
- The brand line "The Element of Creation" appears on every page; the monorepo gate
  `check_public_surface_brand.py` asserts it against the served site.
- Revenue figures never appear in public content (owner ruling).
