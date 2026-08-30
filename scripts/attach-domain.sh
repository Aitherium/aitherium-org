#!/usr/bin/env bash
# Attach the aitherium.org domain to this Pages site — run AFTER the zone
# exists in Cloudflare (owner adds it in the dashboard, or a token with
# zone.create does). Steps:
#   1. wait for the aitherium.org zone to answer (NS REFUSED -> gone)
#   2. create DNS CNAMEs via the monorepo tunnel-sync workflow (pages-cnames.yaml
#      already carries aitherium.org + www with per-entry zone overrides)
#   3. set the Pages custom domain (cname=aitherium.org)
#   4. poll GitHub's cert issuance (PPC002)
#
# Usage: scripts/attach-domain.sh
set -euo pipefail

NS1="${NS1:-molly.ns.cloudflare.com}"

echo "1/4  waiting for aitherium.org zone to serve…"
zone_ready=0
for i in $(seq 1 40); do
  if nslookup -type=SOA aitherium.org "$NS1" >/dev/null 2>&1; then
    zone_ready=1
    echo "     zone is live (attempt $i)"
    break
  fi
  sleep 15
done
if [ "$zone_ready" != "1" ]; then
  echo "FAIL: aitherium.org zone still not serving after 10 min" >&2
  echo "      Add the zone in the Cloudflare dashboard (Add site → aitherium.org → Free)." >&2
  exit 1
fi

echo "2/4  dispatching monorepo tunnel-sync to create the DNS CNAMEs…"
gh workflow run cloudflare-tunnel-sync.yml --repo Aitherium/AitherOS --ref develop
echo "     dispatched — CNAMEs land when the runner picks it up (idempotent)."

echo "3/4  setting the Pages custom domain…"
gh api -X PUT "repos/Aitherium/aitherium-org/pages" -f "cname=aitherium.org" \
  --jq '{cname, status, html_url}' 2>&1 | head -3

echo "4/4  polling GitHub cert issuance (PPC002 — live SAN probe)…"
for i in $(seq 1 60); do
  san=$(echo | openssl s_client -connect 185.199.108.153:443 \
        -servername aitherium.org 2>/dev/null \
        | openssl x509 -noout -text 2>/dev/null \
        | grep -A1 "Subject Alternative Name" | tail -1)
  if echo "$san" | grep -q "aitherium.org"; then
    echo "     cert live: $san"
    echo "DONE — https://aitherium.org serves its own cert."
    exit 0
  fi
  sleep 20
done
echo "WARN: cert not yet issued after 20 min — GitHub usually takes ~10-30 min."
echo "      Re-run this script; it skips completed steps."
exit 2
