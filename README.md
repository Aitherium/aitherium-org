# aitherium.org — Aitherium Foundation

The non-profit site for the Aitherium Foundation. A deliberately **traditional
web page**: light paper, serif display type, one dignified accent — not the
dark Living-OS chrome of aitherium.com. A foundation site reads as a
document, not an operating system.

## Pages

| Page | Purpose |
|---|---|
| `index.html` | Mission, programs, principles, news |
| `about.html` | Mission & operating principles |
| `programs.html` | The four programs |
| `transparency.html` | The public record — what anyone can inspect |
| `get-involved.html` | Contribute, community, hardware, support |
| `news.html` | Points to blog.aitherium.com (one record, not two) |

## Stack

Plain HTML + CSS + a few lines of JS (mobile nav only). No build step, no
framework — a static site stays deployable from any machine, forever.

## Deploy

`push` to `main` → `.github/workflows/pages-deploy.yml` → GitHub Pages at
`aitherium.org` (custom domain via the Pages settings; DNS CNAME is managed
from the monorepo's `pages-cnames.yaml` lane).

## Content rules

- Nothing on this site claims what the record does not show. The
  transparency page links to the actual surfaces (status, repos, docs,
  blog) rather than asserting the foundation's credibility in prose.
- The blog at blog.aitherium.com is the record; this site links to it
  rather than duplicating it.
- The Aitherium mark is the delta-and-core glyph, in the foundation's
  dignified blue (#1f4fd8) on paper (#faf9f7).
