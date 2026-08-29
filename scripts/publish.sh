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

git worktree remove .publish-tmp
echo "published → https://aitherium.github.io/aitherium-org/"
