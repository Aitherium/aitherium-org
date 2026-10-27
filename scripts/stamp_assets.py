"""Stamp every page's CSS/JS links with a content hash (?v=...).

aitherium.org sits behind Cloudflare, which caches theme.css/styles.css/app.js for
hours. Without a version in the URL a visitor gets the NEW page with the OLD assets
(measured 2026-10-01: dead theme switch, black element card, dark-mode colours on a
light page). Idempotent: re-running with unchanged assets changes nothing.
Exit 1 with --check when any page carries a stale stamp.
"""
import hashlib, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ("theme.css", "styles.css", "app.js")


def stamps():
    return {a: hashlib.sha256((ROOT / a).read_bytes()).hexdigest()[:10] for a in ASSETS if (ROOT / a).exists()}


def stamp_text(text, st):
    for name, h in st.items():
        text = re.sub(r'((?:href|src)=")' + re.escape(name) + r'(?:\?v=[0-9a-f]+)?(")', r'\g<1>' + name + '?v=' + h + r'\g<2>', text)
    return text


def main():
    check = "--check" in sys.argv
    st = stamps(); stale = []
    for page in sorted(ROOT.glob("*.html")):
        old = page.read_text(encoding="utf-8"); new = stamp_text(old, st)
        if new != old:
            stale.append(page.name)
            if not check:
                page.write_text(new, encoding="utf-8")
    if check and stale:
        print("stale asset stamps:", ", ".join(stale)); return 1
    print(("checked" if check else "stamped"), len(list(ROOT.glob("*.html"))), "pages", st)
    return 0


if __name__ == "__main__":
    sys.exit(main())
