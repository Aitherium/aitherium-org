#!/usr/bin/env bash
# Publish the aitherium.org site: sync main's tree onto the gh-pages branch
# and push. Pages is build_type: legacy, source: gh-pages — GitHub's own
# builder publishes it (no self-hosted runner needed).
#
# Git-only on purpose: rsync is not on Windows git-bash, and the site has no
# build step, so gh-pages is simply main's tree. The publish branch is
# rewritten from main every time (deploy-branch pattern).
#
# Usage: scripts/publish.sh [message]
set -euo pipefail

cd "$(dirname "$0")/.."
MSG="${1:-Publish aitherium.org}"

# A failed run (e.g. mid-script network error) can leave .publish-tmp behind.
# Without this sweep the next publish fails with "cannot force update the
# branch 'gh-pages' used by worktree" — a confusing error that names neither
# the stale directory nor the fix. Measured 2026-08-29, live.
if [ -d .publish-tmp ]; then
  git worktree remove .publish-tmp --force 2>/dev/null || rm -rf .publish-tmp
  echo "note: removed stale .publish-tmp from a previous failed publish"
fi
git worktree prune

git fetch origin gh-pages 2>/dev/null || true
if ! git worktree add .publish-tmp gh-pages 2>/dev/null; then
  # gh-pages does not exist yet — point it at main and done.
  git branch -f gh-pages main
  git push origin gh-pages
  echo "published (first) → https://aitherium.github.io/aitherium-org/"
  exit 0
fi

(cd .publish-tmp \
  && git rm -q -rf . \
  && git checkout main -- . \
  && git add -A \
  && git -c user.name="wizzense" -c user.email="wizzense@users.noreply.github.com" \
     commit -m "$MSG" --quiet \
  && git push origin gh-pages --quiet)

# ── Verification (this used to scan NOTHING) ─────────────────────────────
# The pre-publish fetch above only fills FETCH_HEAD, so `origin/gh-pages` does
# not resolve on a fresh clone, `git ls-tree` printed "Not a valid object
# name", grep -c on EMPTY input printed 0, and every publish reported
# "(tree verified == main)" having verified nothing. Measured live
# 2026-08-30 — the "gate that scanned nothing" class. Re-fetch into a real
# ref after the push so the check reads the state that was actually pushed.
git fetch origin gh-pages:refs/remotes/origin/gh-pages 2>/dev/null || {
  echo "cannot re-fetch gh-pages after publish — DEAD, not verified" >&2
  exit 2
}

# 1) The published tree must be EXACTLY main's tree. Measured 2026-08-29:
#    a foreign Veil static export (.next/, AGENTS.md, CNAME) appeared on
#    gh-pages mid-session; the wholesale rewrite above swept it, and this
#    re-asserts the invariant after every publish so a repeat cannot be silent.
MAIN_TREE=$(git rev-parse "main^{tree}")
PAGE_TREE=$(git rev-parse "refs/remotes/origin/gh-pages^{tree}")
if [ "$MAIN_TREE" != "$PAGE_TREE" ]; then
  echo "TREE MISMATCH: gh-pages tree $PAGE_TREE != main tree $MAIN_TREE — publish did not land main's site" >&2
  exit 1
fi

# 2) No foreign artifacts on top of the exact tree.
FOREIGN=$(git ls-tree --name-only refs/remotes/origin/gh-pages | grep -cE '__next|\.next|node_modules|^dist' || true)
if [ "$FOREIGN" != "0" ]; then
  echo "FOREIGN ARTIFACTS on gh-pages ($FOREIGN) — publish did not sweep clean" >&2
  exit 1
fi
git worktree remove .publish-tmp
echo "published → https://aitherium.github.io/aitherium-org/ (tree verified == main)"
