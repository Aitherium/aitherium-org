#!/usr/bin/env bash
# Publish the aitherium.org site: sync the working tree onto the gh-pages
# branch and push. Pages is build_type: legacy, source: gh-pages — GitHub's
# own builder publishes it (no self-hosted runner needed).
#
# Usage: scripts/publish.sh [message]
set -euo pipefail

cd "$(dirname "$0")/.."
MSG="${1:-Publish aitherium.org}"

# Fresh orphan-like tree: start from main's content, not the old branch.
git fetch origin gh-pages 2>/dev/null || true
git worktree add .publish-tmp gh-pages 2>/dev/null || {
  git branch -f gh-pages main
  git push origin gh-pages
  exit 0
}

rsync -a --delete \
  --exclude '.git' --exclude '.publish-tmp' --exclude 'scripts' --exclude 'README.md' \
  ./ .publish-tmp/

(cd .publish-tmp \
  && git add -A \
  && git -c user.name="wizzense" -c user.email="wizzense@users.noreply.github.com" \
     commit -m "$MSG" --quiet \
  && git push origin gh-pages --quiet)

git worktree remove .publish-tmp
echo "published → https://aitherium.github.io/aitherium-org/"
