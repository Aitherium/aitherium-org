# Contributing to aitherium.org

This repository is the Aitherium Foundation site (https://aitherium.org): plain HTML,
CSS and one small JavaScript file, with no build step at deploy time.

## How to contribute

1. **Report a problem or suggest a change** by opening an issue:
   https://github.com/Aitherium/aitherium-org/issues. Broken links, wrong figures and
   accessibility problems are all welcome. English is the working language.
2. **Propose a fix** by forking the repository and opening a pull request against
   `main`. Small, focused pull requests are reviewed fastest.
3. A maintainer reviews every pull request. Discussion happens on the pull request,
   in public, addressable by URL.
4. Security problems go through [SECURITY.md](SECURITY.md), never a public issue.

## Requirements for an acceptable contribution

- **Shared chrome is generated.** Edit `scripts/gen_pages.py` (or `scripts/bricks.json`
  for the stack table), run `python scripts/gen_pages.py`, and commit the regenerated
  HTML with your change. Do not hand-edit the generated header, menubar or footer.
- **Works with JavaScript off.** Every page must stay complete without `app.js`.
- **Colours come from tokens.** Both palettes live in `theme.css`; no colour literal
  belongs anywhere else. `kit/` is vendored verbatim and is never edited.
- **Every external link answers 200** when you add it.
- **Every number carries its date and its source.** Re-measure; never edit a figure
  by hand. Nothing on the site may claim what the public record does not show.
- **Licence.** Contributions are accepted under the repository's
  [Apache-2.0 licence](LICENSE).
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Previewing locally

Open `index.html` in a browser, or serve the folder:

```
python -m http.server 8000
```

## Releasing

Maintainers publish with `scripts/publish.sh "message"`, which syncs `main` onto the
`gh-pages` branch that GitHub Pages serves.
