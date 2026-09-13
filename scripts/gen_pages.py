#!/usr/bin/env python3
"""Emit the six aitherium.org pages from one source of copy + one brick snapshot.

    python scripts/gen_pages.py

There is still no build step at deploy time: the generated HTML is committed and
served as-is. This script exists so the chrome (head, nav, footer) cannot drift
across six files and so the periodic table is rendered from a DATED snapshot of
the ecosystem registry (scripts/bricks.json) rather than typed by hand.

Content rules (kept from the first site, still binding):
  - every external link points at a surface that answered 200 when the snapshot
    was taken; the monorepo gate check_org_site_links.py re-probes the live site
  - every number carries its date and its source
  - nothing here claims what the record does not show
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = json.loads((ROOT / "scripts" / "bricks.json").read_text(encoding="utf-8"))
MEASURED = SNAP["measured"]
BRICKS = SNAP["bricks"]

BLOG = "https://blog.aitherium.com"
GH = "https://github.com/Aitherium"
PAGES = "https://aitherium.github.io"
RELAY = "https://relay.aitherium.com"
CONTACT = "mailto:foundation@aitherium.org"
DISCORD = "https://discord.gg/kKhgRm9wH"
CODEX_PATH = f"{GH}/awknowledge/blob/main/path"
PACE = "https://darioamodei.com/post/we-must-pace-the-frontier"
AIPCON = "https://www.investing.com/news/transcripts/palantir-at-aipcon-11-ai-shifts-from-talk-to-operations-93CH-4896825"

# Two-letter element symbols. Hand-mapped so none collide.
SYMBOLS = {
    "awnix": "Nx", "awdk": "Dk", "awnode": "Nd", "awdesk": "De", "awrun": "Ru", "awnet": "Nt",
    "awgym": "Gy", "awflow": "Fl", "awskills": "Sk", "awpack": "Pk", "awknowledge": "Kn",
    "AitherZero": "Az", "awm": "Mm", "awgraph": "Gr", "awgit": "Gi", "awdelphi": "Dl",
    "awtoll": "Tl", "awseal": "Se", "awshare": "Sa", "awdit": "Di", "awbac": "Ba", "awiam": "Ia",
    "awtunnel": "Tu", "awnest": "Ne", "awnboard": "Nb", "awrecover": "Rc", "awstorage": "St",
    "awrelay": "Rl", "awask": "As", "awmail": "Ma", "awfind": "Fi", "awbrowse": "Br",
    "gawbbonet": "Gb", "aitherkvcache": "Kv", "awrtifact": "Rt", "AitherConnect": "Ac",
    "awreason": "Re", "awrecurse": "Rr", "awprism": "Pr", "awrepl": "Rp", "awresearch": "Rs",
    "awfocus": "Fo", "awpredict": "Pd", "awsh": "Sh", "awkno": "Ko", "awembed": "Em",
    "awtax": "Tx", "awsettings": "Sg", "awavatar": "Av",
}
KIND_ORDER = {"base": 0, "runtime": 1, "corpus": 2, "tool": 3}


def esc(s: object) -> str:
    return (str(s if s is not None else "")
            .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


# ── chrome ────────────────────────────────────────────────────────────────────

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 128 128'%3E"
           "%3Crect width='128' height='128' rx='24' fill='%23000103'/%3E"
           "%3Crect x='12' y='12' width='104' height='104' rx='16' fill='none' stroke='%232AD7D7' stroke-width='3'/%3E"
           "%3Ctext x='64' y='74' text-anchor='middle' dominant-baseline='central' font-family='Inter,Helvetica,Arial,sans-serif' "
           "font-size='58' font-weight='200' fill='%232AD7D7' letter-spacing='-2'%3EAi%3C/text%3E%3C/svg%3E")

BRAND_CELL = """<svg class="cell" viewBox="0 0 128 128" aria-hidden="true">
        <rect width="128" height="128" rx="22" fill="#02060D"/>
        <rect x="10" y="10" width="108" height="108" rx="16" fill="none" stroke="#2AD7D7" stroke-width="4"/>
        <text x="64" y="76" text-anchor="middle" dominant-baseline="central" font-family="Inter, Helvetica, Arial, sans-serif" font-size="62" font-weight="200" fill="#2AD7D7" letter-spacing="-3">Ai</text>
      </svg>"""

NAV = [
    ("start.html", "Start"),
    ("about.html", "Thesis"),
    ("programs.html", "Programs"),
    ("transparency.html", "Transparency"),
    ("get-involved.html", "Get involved"),
    ("news.html", "News"),
]


def head(title: str, desc: str, path: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Aitherium Foundation">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="https://aitherium.org/{path}">
  <meta name="theme-color" content="#000103">
  <link rel="canonical" href="https://aitherium.org/{path}">
  <link rel="icon" href="{FAVICON}">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
"""


def header(current: str) -> str:
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'        <li><a href="{href}"{cur}>{label}</a></li>')
    items.append('        <li><a class="btn btn-primary" href="start.html">Build with agents</a></li>')
    return f"""<header class="site-header">
  <div class="container nav-row">
    <a class="brand" href="index.html" aria-label="Aitherium Foundation home">
      {BRAND_CELL}
      Aitherium <span class="org">Foundation</span>
    </a>
    <nav aria-label="Primary">
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <ul class="nav-links" id="nav-links">
{chr(10).join(items)}
      </ul>
    </nav>
  </div>
</header>

<main>
"""


FOOTER = f"""</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html">
          {BRAND_CELL}
          Aitherium <span class="org">Foundation</span>
        </a>
        <p class="footer-blurb">Ai · 0 · The Element of Creation. An open operating system for
        agents, built to run on hardware people own, and the foundation that keeps it that way.</p>
      </div>
      <div>
        <h4>Foundation</h4>
        <ul>
          <li><a href="about.html">The thesis</a></li>
          <li><a href="programs.html">Programs</a></li>
          <li><a href="transparency.html">The record</a></li>
          <li><a href="news.html">News</a></li>
        </ul>
      </div>
      <div>
        <h4>The world</h4>
        <ul>
          <li><a href="{GH}" rel="noopener">GitHub</a></li>
          <li><a href="{PAGES}/awdk/" rel="noopener">awdk docs</a></li>
          <li><a href="{PAGES}/awknowledge/" rel="noopener">The codex</a></li>
          <li><a href="{BLOG}" rel="noopener">Blog</a></li>
          <li><a href="{RELAY}" rel="noopener">The rooms</a></li>
          <li><a href="{DISCORD}" rel="noopener">The Collective on Discord</a></li>
          <li><a href="https://wizzense.github.io/" rel="noopener">The builder · wizzense</a></li>
        </ul>
      </div>
      <div>
        <h4>Get involved</h4>
        <ul>
          <li><a href="start.html">Start building</a></li>
          <li><a href="start.html#phone">On your phone</a></li>
          <li><a href="get-involved.html#hardware">Run a node</a></li>
          <li><a href="get-involved.html#contribute">Contribute</a></li>
          <li><a href="get-involved.html#support">Support the foundation</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>© 2026 Aitherium Foundation · <a href="{GH}/aitherium-org" rel="noopener">this site is a public repo</a></div>
      <div><span class="tag">no hyperscale</span> · your hardware · your weights · your agents</div>
    </div>
  </div>
</footer>

<script src="app.js"></script>
</body>
</html>
"""


def page(path: str, title: str, desc: str, body: str) -> None:
    html = head(title, desc, path) + header(path) + body + FOOTER
    (ROOT / path).write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {path} ({len(html):,} bytes)")


# ── shared fragments ──────────────────────────────────────────────────────────

AI_CARD = """<div class="hero-card" aria-hidden="true">
        <div class="frame"><svg viewBox="0 0 400 480" xmlns="http://www.w3.org/2000/svg">
          <rect x="40" y="30" width="320" height="400" rx="14" fill="#02060D" stroke="#2AD7D7" stroke-width="1.5"/>
          <text x="66" y="78" font-family="JetBrains Mono, Menlo, monospace" font-size="20" fill="#2AD7D7">0</text>
          <text x="334" y="78" text-anchor="end" font-family="JetBrains Mono, Menlo, monospace" font-size="13" fill="#69737D">[Xe] 4f14 5d10 6s1</text>
          <text x="200" y="232" text-anchor="middle" dominant-baseline="central" font-family="Inter, Helvetica, Arial, sans-serif" font-size="164" font-weight="200" fill="#2AD7D7" letter-spacing="-8">Ai</text>
          <text x="200" y="322" text-anchor="middle" font-family="Inter, Helvetica, Arial, sans-serif" font-size="16" font-weight="400" fill="#9BA6B1" letter-spacing="7">AITHERIUM</text>
          <text x="200" y="354" text-anchor="middle" font-family="JetBrains Mono, Menlo, monospace" font-size="14" fill="#69737D">208.043</text>
          <line x1="66" y1="384" x2="334" y2="384" stroke="#162330" stroke-width="1"/>
          <text x="200" y="408" text-anchor="middle" font-family="Inter, Helvetica, Arial, sans-serif" font-size="10.5" fill="#69737D" letter-spacing="4">THE ELEMENT OF CREATION</text>
          <ellipse cx="200" cy="228" rx="150" ry="28" fill="none" stroke="#907AE9" stroke-width="0.6" opacity="0.28" transform="rotate(-14,200,228)"/>
          <ellipse cx="200" cy="228" rx="158" ry="22" fill="none" stroke="#2AD7D7" stroke-width="0.5" opacity="0.2" transform="rotate(24,200,228)"/>
        </svg></div>
        <div class="caption">Element 0 · the element that precedes all creation</div>
      </div>"""


def periodic_table() -> str:
    bricks = sorted(BRICKS, key=lambda b: (KIND_ORDER.get(b["kind"], 9), b["id"].lower()))
    # Aitherium is Element 0 — the element that precedes all creation (.ELEMENT/STYLE_GUIDE.md;
    # owner ruling 2026-09-13 over brand.yaml's 47). The bricks are numbered 1..N after it.
    cells = ['      <li><a class="el ai" href="index.html" aria-label="Aitherium, element 0">'
             '<span class="no">0</span><span class="sy">Ai</span><span class="nm">aitherium</span></a></li>']
    for n, b in enumerate(bricks, start=1):
        sy = SYMBOLS[b["id"]]
        repo = f"{GH}/{b['id']}"
        docs = f"{PAGES}/{b['id']}/" if b.get("pages_ok") else ""
        on = " on" if b["id"] == "awnix" else ""
        cells.append(
            f'      <li><a class="el{on}" href="{repo}" rel="noopener" data-kind="{esc(b["kind"])}" '
            f'data-id="{esc(b["id"])}" data-sy="{sy}" data-tagline="{esc(b.get("tagline"))}" '
            f'data-install="{esc(b.get("install"))}" data-repo="{repo}" data-docs="{docs}" '
            f'data-trust="{esc(b.get("instead_of_trusting"))}" data-check="{esc(b.get("you_check"))}">'
            f'<span class="no">{n}</span><span class="sy">{sy}</span><span class="nm">{esc(b["id"])}</span></a></li>'
        )
    first = next(b for b in bricks if b["id"] == "awnix")
    detail = f"""    <div class="pt-detail" aria-live="polite">
      <div>
        <div class="hd"><span class="sy">{SYMBOLS['awnix']}</span><span class="nm">awnix</span><span class="kd">base</span></div>
        <p class="tx">{esc(first.get('tagline'))}</p>
        <div class="how">{esc(first.get('install'))}</div>
        <div class="links"><a href="{GH}/awnix" rel="noopener">source ↗</a><a href="{PAGES}/awnix/" rel="noopener">docs ↗</a></div>
      </div>
      <div>
        <span class="tv trust">instead of trusting</span><p>{esc(first.get('instead_of_trusting'))}</p>
        <span class="tv check">you check</span><p>{esc(first.get('you_check'))}</p>
      </div>
    </div>"""
    return f"""    <div class="pt-legend">
      <span style="--k:#FF8950">base</span>
      <span style="--k:#2AD7D7">runtime</span>
      <span style="--k:#70DDB1">corpus</span>
      <span style="--k:#907AE9">tool</span>
      <span style="--k:#69737D">{len(bricks)} public · measured {MEASURED}</span>
    </div>
    <ul class="pt">
{chr(10).join(cells)}
    </ul>
{detail}"""


RECEIPTS = [
    ("23.6", "tok/s", "A <strong>284-billion-parameter</strong> mixture-of-experts model served across three machines on a 1 GbE home network. Transport was 1–2% of per-token cost; the field's reflex to blame the network was measured and falsified.", "AitherNet report, 2026-08", f"{BLOG}/blog/one-model-two-machines-distributed-inference-on-hardware-we-own"),
    ("2", "machines", "A 27B model with its layers <strong>split across a gaming GPU and an idle ARM box</strong>, passing activations over the same network your printer uses. It answered correctly.", "2026-07-24", f"{BLOG}/blog/one-model-two-machines-distributed-inference-on-hardware-we-own"),
    ("969", "seconds", "A fresh cloud box became a <strong>self-registered, AI-capable CI runner</strong> on awnix: built from source, secrets shredded at boot, no password anywhere.", "awnix, 2026-08", f"{GH}/awnix"),
    ("236 MB", "→ 3.6 GB", "Bonsai brains that run in an <strong>unmodified browser</strong> on the visitor's own GPU, four sizes, chosen by the device. No install, no account, no terminal.", "aitherium.com, 2026-08", "https://aitherium.com/"),
    ("28.9M", "params", "A language model running on an <strong>$8 microcontroller</strong>. That is the floor of the edge role: a node too small to hold an expert can still route, sense and draft.", "AitherNet report, 2026-08", f"{GH}"),
    ("36M", "lines / 10 mo", "The software factory, measured: every repo, deduped by root commit, author-filtered, lockfiles and vendored code stripped. The instrument ships in the repo with a self-test.", "2026-08-14", f"{BLOG}/blog/i-measured-my-software-factory-36-million-lines-in-10-months"),
    ("27,939", "prompts", "The operator doctrine is <strong>mined from 3,183 real sessions over 210 days</strong>, re-measured on held-out data, and published as an installable pack rather than a blog post about being smart.", "awknowledge", f"{PAGES}/awknowledge/"),
    (str(len(BRICKS)), "public bricks", "Of 79 registered. Each installs on its own, runs offline, needs no account. Every repo and docs page above answered 200 the day this was written.", f"registry, {MEASURED}", f"{GH}"),
    ("243", "published posts", "Field reports, doctrine and corrections, in the order they happened. The blog is the record; this site points at it.", f"counted {MEASURED}", BLOG),
]


def receipts(items=RECEIPTS) -> str:
    out = ['    <ul class="receipts">']
    for v, unit, what, src, href in items:
        out.append(f'      <li><span class="v">{v}<small>{esc(unit)}</small></span>'
                   f'<span class="what">{what}</span>'
                   f'<span class="src"><a href="{href}" rel="noopener">{esc(src)}</a></span></li>')
    out.append('    </ul>')
    return "\n".join(out)


# ── index ─────────────────────────────────────────────────────────────────────

INDEX = f"""  <section class="hero">
    <div class="container">
      <div>
        <p class="eyebrow">Aitherium Foundation <span class="sep">·</span> Ai <span class="sep">·</span> 0 <span class="sep">·</span> The Element of Creation</p>
        <h1>Every AI company could stop training models today. <strong>We think they&nbsp;should.</strong></h1>
        <p class="lede">The intelligence we already have is enough. The problem was never intelligence; it was
        the poverty of the environment around it. The industry is running a race with no finish line,
        bigger models, denser datacenters, infinite scale, and the freight train is pointed at a
        society that was never asked. <strong>We do not believe in infinite scaling. So we stopped
        chasing the bigger brain and built the body</strong>: an operating system for agents that
        runs on hardware you own, in the open, with the foundation running on it first.</p>
        <div class="actions">
          <a class="btn btn-primary" href="start.html">Start building, on your phone</a>
          <a class="btn" href="about.html">Read the thesis</a>
        </div>
        <div class="install">
          <div class="term-title">A real model on the phone in your pocket, or the laptop with no GPU</div>
          <div class="term"><span class="p">$ </span>curl -fsSL https://aitherium.com/phone.sh | bash <span class="c"># Android · Termux</span><br><span class="p">$ </span>pip install awdk <span class="c">&amp;&amp;</span> adk quickstart-local <span class="c"># any laptop, no GPU</span></div>
        </div>
      </div>
      {AI_CARD}
    </div>
  </section>

  <section class="tight" id="name">
    <div class="container two-col">
      <div>
        <span class="kicker"><b>§00</b> · the name</span>
        <h2>Aither is the medium creation moves&nbsp;through.</h2>
      </div>
      <div>
        <p>In Greek cosmology <em>aither</em> (αἰθήρ) was the pure, bright upper air the gods breathed:
        not the heavy air of mortals, but the luminous medium through which the heavens moved and
        creation flowed. We chose the name deliberately. Aither is the invisible medium that makes
        creation possible, and AitherOS is what that medium looks like when you actually build it:
        an operating system where agents write, design, code, research and create, with persistent
        memory, real tools and real infrastructure behind them.</p>
        <p><strong>The world thinks AI is a chatbot. We are here to show them it is a forge.</strong>
        A chatbot answers questions. An agent does the work. They sell you a chatbot; we give you the
        element of creation.</p>
      </div>
    </div>
  </section>

  <section id="manifesto">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>§01</b>The manifesto</div>
        <div>
          <h2>No infinite&nbsp;scaling.</h2>
          <p>Four claims, each one unfashionable, each one measured before it was written down.</p>
        </div>
      </div>
      <ol class="theses">
        <li>
          <div class="n">the body</div>
          <div>
            <h3>The brain is a plug. We built everything&nbsp;else.</h3>
            <p>Every lab is racing to build a bigger brain: more parameters, longer context, better
            benchmarks. It is the same bet made a thousand ways: if the model is smart enough,
            everything else will follow. It never follows. A brain without a body is a philosophy
            department. No memory that persists, no tools it can run, no immune system, no hands.</p>
            <p>So the model is one node in the pipeline. It plugs in, does its part, and plugs out.
            When a better one drops, the organism absorbs it: no migration, no retraining, no
            downtime. Two hundred services, the agents, the faculty graphs, the memory tiers: none of
            them change. <strong>The prompt was the spark. The environment was the fuel.</strong>
            <a href="{BLOG}/blog/the-brain-is-a-plug" rel="noopener">The essay ↗</a></p>
          </div>
        </li>
        <li>
          <div class="n">the ceiling</div>
          <div>
            <h3>You cannot spin up infinite agents on infinite hardware for&nbsp;free.</h3>
            <p>Compute is real: GPUs, memory, electricity. Demand for software is effectively infinite
            and will grow to fill whatever capacity exists, so cheaper compute means more uses for
            compute, not less. And human relationships do not scale either: a person can hold thirty
            to fifty of them before the work degrades. <strong>That ceiling is good.</strong> It is
            the structural reason this economy distributes instead of concentrating, and the reason
            the right unit of AI is a machine in a closet, not a gigawatt campus.</p>
            <p>Slow down. Build responsibly. Use the intelligence that already exists to steer the
            society we have, instead of dragging it in front of the train.</p>
          </div>
        </li>
        <li>
          <div class="n">two things</div>
          <div>
            <h3>Two things can be&nbsp;true.</h3>
            <p>The race has to stop, because the race itself creates the worst possible conditions
            for the future of the people it is being run on. The labs have demonstrated, repeatedly,
            that they cannot be trusted to load all of humanity onto the airplane without landing
            gear. And the same companies need open source to stop, because they cannot afford to
            compete with it: the bet was two trillion dollars on models nobody else can afford to
            run, including them, so that they become as embedded as the electrical grid and the
            rest of us rent from the tap.</p>
            <p>In September 2026 the frontier labs began saying the first half themselves:
            <a href="{PACE}" rel="noopener">"We must pace the frontier"</a>, with the others
            agreeing within the hour. We said stop in August. The difference is who gets to keep
            running while everyone else paces. <strong>Slowing the frontier is only safe if the
            floor is owned</strong>: open weights, open code, on hardware that answers to the person
            who bought it.</p>
          </div>
        </li>
        <li>
          <div class="n">the moat</div>
          <div>
            <h3>The only moat is&nbsp;time.</h3>
            <p>Weights leak. Architectures get cloned in a weekend. Even hidden reasoning is
            distillable from a black box's answers and summaries. There is exactly one advantage in
            this field that cannot be bought or stolen: the integral of a system improving itself,
            a little every day, resiliently, for longer than you have. Not the snapshot. The slope,
            multiplied by the months.</p>
            <p>So the platform trains in the off-peak windows on hardware it already owns, in small
            reversible steps behind fail-closed gates, and it has been doing that for a while.
            <strong>The advantage is not a model. It is the months.</strong>
            <a href="{BLOG}/blog/the-only-moat-is-time" rel="noopener">The essay ↗</a></p>
          </div>
        </li>
      </ol>
    </div>
  </section>

  <section id="thesis">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>§02</b>No hyperscale</div>
        <div>
          <h2>Intelligence does not need a&nbsp;landlord.</h2>
          <p>The concentration thesis is wrong, and it is losing on arithmetic. The story goes: AI needs massive compute, massive compute needs massive capital, so AI
          will belong to whoever owns the datacenters. Every clause after the first is a business
          decision dressed as physics. We spent two years measuring the alternative instead of
          arguing about it.</p>
        </div>
      </div>
      <ol class="theses">
        <li>
          <div class="n">placement</div>
          <div>
            <h3>Concentration follows compute. Compute does not have to&nbsp;concentrate.</h3>
            <p>A modern mixture-of-experts model activates a small fraction of itself per token:
            in the one we run, <strong>6 of 256 experts across 43 layers</strong>. The model does
            not need to <em>fit</em> in any one machine. It needs to be <em>placed</em> so the
            active fraction is reachable in time. Sparsity is what makes a network of small
            machines a plausible host for a very large model.</p>
            <p>So we split a 27B model across a gaming GPU and an idle ARM box over an ordinary LAN,
            and it answered. Then a 284B model across three memory tiers on 1 GbE, at 23.6 tokens
            a second. Transport was 1–2% of the cost per token. <strong>The network was never the
            problem.</strong> The datacenter is a convenience for the people who own it, not a
            requirement of the mathematics.</p>
          </div>
        </li>
        <li>
          <div class="n">the arithmetic</div>
          <div>
            <h3>The desktop is the&nbsp;datacenter.</h3>
            <p>A GPU-hour rented from a hyperscaler has to recoup the building, the cooling, the
            land, the staff, the 18 months of construction risk and the cost of capital. A GPU under
            your desk has to recoup a power bill. Every enterprise with a competent finance team
            eventually runs this table. So did the banks.</p>
            <div class="ledger-wrap"><div class="ledger">
              <table>
                <thead><tr><th></th><th>Rented rack GPU</th><th>Owned desk GPU</th></tr></thead>
                <tbody>
                  <tr><td>Hardware</td><td class="old">~$30,000 · H100, plus the facility around it</td><td class="new">~$2,000 · RTX 5090, plus a desk</td></tr>
                  <tr><td>Power &amp; cooling</td><td class="old">$5,000–8,000 / year, amortised into your rate</td><td class="new">575 W · ~$50 / month on a residential bill</td></tr>
                  <tr><td>Marginal cost of a call</td><td class="old">metered, forever, with a sales rep attached</td><td class="new">zero after the hardware is paid for</td></tr>
                  <tr><td>Idle capacity at 3 a.m.</td><td class="old">someone else's margin</td><td class="new">your agent swarm's refactor backlog, free</td></tr>
                  <tr><td>Terms of service</td><td class="old">can change on a Tuesday</td><td class="new">there are none</td></tr>
                  <tr><td>Where your data goes</td><td class="old">through their API, under their policy</td><td class="new">nowhere. there is no code path that sends it</td></tr>
                </tbody>
                <tfoot><tr><td colspan="3">Prices as published in the 2026-03 and 2026-05 field reports. Breakeven for a serious agentic workload is measured in months, not years.</td></tr></tfoot>
              </table>
            </div></div>
          </div>
        </li>
        <li>
          <div class="n">routing</div>
          <div>
            <h3>Cloud as overflow, not as&nbsp;default.</h3>
            <p>The rebuttal to local inference compares one sad 7B chatbot on a laptop with a
            frontier model behind seventy stages of scaffolding, and declares local lost. That was
            never the comparison. The hard part of local AI is not the model. It is the
            <strong>operating system around the model</strong>: one scheduler every call goes
            through, a fleet of model sizes pinned to the cheapest hardware that holds them, a
            router that picks the smallest brain that can finish the job, a context pipeline that
            lets a 14B model with six thousand well-chosen tokens beat a 200B model with a
            hundred-thousand-token garbage dump.</p>
            <p>Once that OS exists, more than 80% of calls are served by an 8B model. Keep a frontier
            key for the long tail. Stop paying for it on the other 95%. <strong>Local-first is not
            anti-cloud.</strong> It is cloud as overflow instead of cloud as landlord, and the
            economics of those two architectures are not in the same universe.</p>
          </div>
        </li>
        <li>
          <div class="n">distribution</div>
          <div>
            <h3>Safe to join is the plane nobody&nbsp;built.</h3>
            <p>Distributed inference is four independent problems: <em>placement</em>,
            <em>precision</em>, <em>verification</em>, and <em>distribution</em>. Each is well
            solved in isolation by a different group. None compose. And the one the literature
            skips, how an ordinary person's device joins safely without a terminal, a toolchain or
            an inbound firewall rule, is the one that decides whether "millions of idle machines"
            is arithmetic or rhetoric.</p>
            <p>So that is where our work is concentrated: a sovereign appliance that runs
            contributed work in an isolated VM so participation never means trusting a stranger's
            code on your host; identity from a device flow instead of an API key that leaks; tenant
            scope carried end to end and <strong>failing closed</strong> when it cannot be
            determined; and meshes that federate as a queryable graph instead of collapsing into
            one trust domain. Placement, precision and verification presuppose a node that has
            already joined. This is the join.</p>
          </div>
        </li>
      </ol>

      <div class="section-head" style="margin-top:72px">
        <div class="num"><b>§02b</b>the comparison</div>
        <div>
          <h2>The good version of&nbsp;Palantir.</h2>
          <p>The most expensive AI company on earth now sells the argument on this page. At its own
          conference in September 2026, Palantir had L3Harris say that fine-tuned open models
          outperformed the frontier at a fraction of the cost, and its CEO has been asking why
          anyone charges by the token for something that valuable if the customer could own the
          means of production instead. He is right. Here is where we part company.</p>
        </div>
      </div>
      <div class="ledger-wrap"><div class="ledger">
        <table>
          <thead><tr><th>The claim</th><th>Their version</th><th>Ours</th></tr></thead>
          <tbody>
            <tr><td>Own the means of production</td><td class="old">a closed platform, sold per deployment to governments and the largest enterprises</td><td class="new">the same architecture as open code: pip install, on the machine in a print shop's back room</td></tr>
            <tr><td>Fine-tuned open models beat the frontier at a fraction of the cost</td><td class="old">a case study on a slide</td><td class="new">the only moat is time: scheduled retraining on hardware you own, in the open, behind fail-closed gates</td></tr>
            <tr><td>Hermetically sealed, no internet, every flow permissioned</td><td class="old">their operators, their network, their terms</td><td class="new">the sovereign appliance: zero open ports, boots with the cable unplugged, tenancy fails closed, agents own their box</td></tr>
            <tr><td>The model is a commodity; the value moves up the stack</td><td class="old">so pay for the stack</td><td class="new">so the stack is the commons: 49 public bricks, each useful to a stranger alone</td></tr>
            <tr><td>Someone should build a profiler for the harness</td><td class="old">someone should</td><td class="new">awtoll: what every tool call costs you in context, measured from your own transcripts</td></tr>
            <tr><td>Who gets it</td><td class="old">the customers who can afford Palantir</td><td class="new">the operator with a laptop, and the businesses in their town</td></tr>
          </tbody>
          <tfoot><tr><td colspan="3">Their claims: Palantir AIPCon 11, 2026-09. Ours: <a href="index.html#receipts">the receipts</a>, <a href="transparency.html#deployed">deployed versus specified</a>, and <a href="{GH}/awtoll" rel="noopener">awtoll</a>.</td></tr></tfoot>
        </table>
      </div></div>
    </div>
  </section>

  <section id="stack">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>§03</b>The stack</div>
        <div>
          <h2>The periodic table of the Aither&nbsp;World.</h2>
          <p>An operating system for agents: a Linux you can hand to one, the runtimes it works in,
          and the tools it works with. Every brick installs on its own, runs offline, and needs no
          account. Every one replaces something you would otherwise have to <em>trust</em> with
          something you can <em>check</em>. Hover a cell.</p>
        </div>
      </div>
{periodic_table()}
    </div>
  </section>

  <section id="doctrine">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>§04</b>Doctrine</div>
        <div>
          <h2>Replace what you would otherwise have to trust with something you can&nbsp;check.</h2>
          <p>One sentence governs everything the foundation ships. It is the header of every brick's
          README and the reason the numbers on this page carry links instead of adjectives.</p>
        </div>
      </div>
      <div class="laws">
        <div class="law">
          <span class="k">LAW 01</span>
          <h3>A rule nothing asserts is a suggestion.</h3>
          <p>Every rule in the platform is a gate with a self-test that proves it can still fail.
          A checker nobody has watched fail is documentation, not enforcement. Hundreds of them run
          unattended; each was a real defect first.</p>
        </div>
        <div class="law">
          <span class="k">LAW 02</span>
          <h3>Silence is not a pass.</h3>
          <p>A probe that cannot reach its subject exits with a verdict of <em>could not judge</em>,
          never green. A total outage and a clean run must never look the same. This is the single
          most expensive lesson in the record, and it is now mechanical.</p>
        </div>
        <div class="law">
          <span class="k">LAW 03</span>
          <h3>Arrogance must be falsifiable.</h3>
          <p>Every number we publish links to the instrument that produced it and the date it was
          measured. Think a figure is inflated? Run the tool; it self-tests. When someone catches us
          wrong with a receipt, the correction prints at the same volume.</p>
        </div>
        <div class="law">
          <span class="k">LAW 04</span>
          <h3>We are our own first tenant.</h3>
          <p>The foundation's fleet runs on the code it publishes. There is no "open for you, closed
          for us." If a capability does not work on hardware a normal person owns, it is not done.
          Hosted services are conveniences, never prerequisites.</p>
        </div>
      </div>
    </div>
  </section>

  <section id="operator">
    <div class="container two-col">
      <div>
        <span class="kicker"><b>§05</b> · the operator</span>
        <h2>You will not be replaced. You will become an&nbsp;operator.</h2>
      </div>
      <div>
        <p>We are going to build software for literally everything, and then integrate all of it.
        The plumber with the spiral notebook. The bakery that reorders flour by eyeballing the bin.
        Thirty-three million small businesses running on duct tape, each with dozens of processes
        that were never worth a developer's hour and are suddenly worth an agent's minute. The
        demand surface for custom, integrated, maintained software was always infinite. AI did not
        shrink it. It revealed it.</p>
        <p>And it cannot concentrate, for three structural reasons. Compute is not free, so the
        equilibrium is distributed inference, not three companies selling tokens to the planet.
        Human relationships do not scale: you can hold thirty or fifty client relationships before
        service degrades, and that ceiling leaves room for the next operator in the next town.
        Governance composes, so nobody has to solve compliance for every industry to serve one.</p>
        <p><strong>One human doing the work of ten does not eliminate nine jobs. It reveals ninety
        that were invisible before.</strong> The foundation exists to make sure the tools for that
        work are owned, not rented.</p>
        <p><a href="{BLOG}/blog/you-wont-be-replaced-youll-become-an-operator" rel="noopener">Read the full argument ↗</a></p>
      </div>
    </div>
  </section>

  <section id="receipts">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>§06</b>Receipts</div>
        <div>
          <h2>Proof, not&nbsp;plans.</h2>
          <p>Every line is a measurement with a date and a link. Where we were wrong we have said so
          in the same place; the record of reversals is the most transferable part of the work.</p>
        </div>
      </div>
{receipts()}
    </div>
  </section>

  <section id="plain" class="tight">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>§07</b>Plain English</div>
        <div>
          <h2>What all of this&nbsp;means.</h2>
          <p>This site talks about agents, nodes and weights. If that reads like another language,
          here is the translation. No technical background needed.</p>
        </div>
      </div>
      <div class="paths">
        <div class="path">
          <span class="k">an operating system for agents</span>
          <p>Your computer's operating system runs your programs. An agent operating system does the
          same for AI: software that runs tasks, remembers things and uses tools for you, on a
          machine you own rather than a server you rent.</p>
        </div>
        <div class="path">
          <span class="k">nodes and the mesh</span>
          <p>A node is a computer that has joined the network. The more ordinary people run nodes,
          laptops, desktops, a box in a closet, the more the network is owned by its users and the
          less any one company can switch it off.</p>
        </div>
        <div class="path">
          <span class="k">open weights</span>
          <p>The weights are the trained model itself, the part that makes an AI work. When they are
          published, anyone can run the AI on their own hardware, check what it does, and keep it
          forever. You own the intelligence instead of renting it.</p>
        </div>
      </div>
    </div>
  </section>

  <section id="start">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>§08</b>Start</div>
        <div>
          <h2>The same stack runs on the phone in your pocket and on a cloud&nbsp;swarm.</h2>
          <p>Pick the hardware you already have. Every rung is the same kit, the same agents, the
          same code; only the brain's size and the address change. The guided path walks each rung
          with the exact command, what you will see, and what you just learned.</p>
        </div>
      </div>
      <div class="record-wrap"><div class="record">
        <table>
          <thead><tr><th>You have</th><th>What runs</th><th>Proof</th><th></th></tr></thead>
          <tbody>
            <tr><td>A phone (Android)</td><td>Bonsai 1.7B to 27B on the CPU, 1-bit, sized from your RAM. Your phone's browser then talks to it over loopback; every reply is generated on the device.</td><td class="st live"><a href="{BLOG}/blog/a-ternary-llm-on-a-pixel-from-one-pasted-line" rel="noopener">a Pixel · 2026-07-27</a> · phone.sh 2026-09-13</td><td><a href="start.html#phone">step 01 ↗</a></td></tr>
            <tr><td>A laptop, no GPU</td><td>The open 8B orchestrator on plain llama.cpp, or Bonsai-27B 1-bit in 3.8 GB. Offline. Unplug the network and it still answers.</td><td class="st live">awdk quickstart-local</td><td><a href="start.html#laptop">step 02 ↗</a></td></tr>
            <tr><td>A desktop with a GPU</td><td>In the browser tab through WebGPU, four sizes from 236 MB to 3.6 GB; or vLLM on any 6 GB card.</td><td class="st live">aitherium.com · adk quickstart</td><td><a href="start.html#gpu">step 06 ↗</a></td></tr>
            <tr><td>A LAN of machines</td><td>One model split across the boxes you own: a 27B across a gaming GPU and an ARM box, a 284B across three memory tiers.</td><td class="st live">23.6 tok/s · 2026-08</td><td><a href="start.html#gpu">step 06 ↗</a></td></tr>
            <tr><td>A DGX Spark, or a rented H100</td><td>One file walks a box into the mesh as capacity; a rented card joined in June.</td><td class="st live">2026-06-04</td><td><a href="{BLOG}/blog/one-model-two-machines-distributed-inference-on-hardware-we-own" rel="noopener">receipt ↗</a></td></tr>
            <tr><td>A cloud account</td><td>The whole fleet as a boot-verified appliance image; ~260 services offline after first boot, the platform switched off.</td><td class="st live">AMI boot-verified · 2026-08</td><td><a href="programs.html#open-source">program ↗</a></td></tr>
          </tbody>
        </table>
      </div></div>
      <div class="actions">
        <a class="btn btn-primary" href="start.html">Start the path</a>
        <a class="btn" href="{PAGES}/awknowledge/" rel="noopener">The codex</a>
      </div>
    </div>
  </section>

  <section class="ignite">
    <div class="container">
      <h2>Own the means of <em>cognition</em>.</h2>
      <p>Renting intelligence by the token is a transitional phase, not an endpoint. The foundation
      exists to make sure the alternative is real, boring, and yours: open code, open weights, an
      operating doctrine anyone can install, and a commons that is hosted by the people who use it.</p>
      <div class="actions">
        <a class="btn btn-forge" href="get-involved.html">Get involved</a>
        <a class="btn" href="transparency.html">Inspect the record</a>
      </div>
    </div>
  </section>
"""

START = f"""  <section class="hero" style="padding-bottom:40px">
    <div class="container" style="display:block">
      <p class="eyebrow">Start <span class="sep">·</span> Aitherium Foundation</p>
      <h1>Build with agents. Start on the machine in your&nbsp;pocket.</h1>
      <p class="lede">Eight steps, in order. Every one runs on hardware you already own, needs no
      account, and says three things: what you need, what you type, and what you will see. A step
      that does not say what you will see is a hope, not a lesson. Total: an afternoon. Step one is
      ten minutes.</p>
      <div class="pt-legend" style="margin-top:22px">
        <a href="#phone" style="--k:#FF8950">01 · phone</a>
        <a href="#laptop" style="--k:#2AD7D7">02 · laptop, no GPU</a>
        <a href="#talk" style="--k:#2AD7D7">03 · talk to it</a>
        <a href="#agent" style="--k:#70DDB1">04 · your first agent</a>
        <a href="#packs" style="--k:#70DDB1">05 · packs</a>
        <a href="#gpu" style="--k:#907AE9">06 · GPU, LAN, cloud key</a>
        <a href="#browser" style="--k:#907AE9">07 · in the browser</a>
        <a href="#mesh" style="--k:#EAB532">08 · join the mesh</a>
      </div>
    </div>
  </section>

  <section class="tight" id="phone">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>01</b>the phone · 10 min</div>
        <div>
          <h2>A real model, on your phone, generating every reply on the&nbsp;device.</h2>
          <p><strong>You need:</strong> an Android phone and a Linux shell on it: Termux from
          F-Droid, or the Linux Terminal built into Android 16 on a Pixel. About 2.2 GB of free
          RAM for the smallest brain, 7.4 GB for the biggest. No root. No account.</p>
        </div>
      </div>
      <div class="two-col">
        <div>
          <div class="term-title">Type this</div>
          <div class="term"><span class="p">$ </span>curl -fsSL https://aitherium.com/phone.sh | bash</div>
          <p style="margin-top:16px"><strong>You will see:</strong> the script measure your RAM and pick a
          Bonsai size (1.7B, 4B, 8B or 27B), install a prebuilt llama.cpp (no compiling; that was
          version one and it took forty minutes), download the weights from our mirror, start a
          server on <code>127.0.0.1:8080</code>, and print a summary that begins
          <em>Bonsai-… is serving</em>. Re-running is safe; every step skips when already done.</p>
          <p><strong>Then:</strong> open the phone's browser at
          <a href="https://elysium.aitherium.com" rel="noopener">elysium.aitherium.com</a> or
          <a href="https://aitherium.com" rel="noopener">aitherium.com</a>. Both probe your local
          server on their own; the model chip flips from "no node" to yours, and from then on every
          reply is generated on the phone. No sign-in, because there is nothing to sign in to.</p>
          <div class="term-title" style="margin-top:14px">Check it by hand</div>
          <div class="term"><span class="p">$ </span>curl -s http://127.0.0.1:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{{"messages":[{{"role":"user","content":"hi"}}],"max_tokens":128}}'</div>
        </div>
        <div>
          <p><strong>What you just learned.</strong> A model is a file of numbers plus a program
          that runs them. Bonsai stores each number in about one bit, which is why a 27-billion-number
          brain fits in a phone's memory, and llama.cpp maps the file instead of copying it, which is
          why the phone does not kill it. The server speaks the same API the big labs charge for,
          on a port only your phone can see.</p>
          <p><strong>Two honest notes.</strong> Bonsai is a reasoning model: it thinks before it
          answers, and on a phone the thinking is most of the wait. Cap it with
          <code>"reasoning_effort":"low"</code> per request, or start the server with
          <code>--reasoning-budget 512</code>. And a phone cannot run these weights inside the
          browser tab itself; a tab's GPU budget is a fraction of what they need. That is why the
          server and the browser live on the same device and talk over loopback.</p>
          <p><strong>iPhone:</strong> no path today. We say so rather than pretend.</p>
          <div class="links" style="display:flex;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem">
            <a href="https://f-droid.org/packages/com.termux/" rel="noopener">Termux on F-Droid ↗</a>
            <a href="https://aitherium.com/phone.sh" rel="noopener">read phone.sh before you run it ↗</a>
            <a href="{BLOG}/blog/a-ternary-llm-on-a-pixel-from-one-pasted-line" rel="noopener">the receipt · a Pixel, 2026-07-27 ↗</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="tight" id="laptop">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>02</b>the laptop · 20 min</div>
        <div>
          <h2>The same brain on a laptop with no&nbsp;GPU.</h2>
          <p><strong>You need:</strong> Python (from python.org; on Windows tick "Add python.exe to
          PATH"), about 6 GB of free disk, and a few minutes of download. No GPU, no API key.</p>
        </div>
      </div>
      <div class="two-col">
        <div>
          <div class="term-title">Install the kit</div>
          <div class="term"><span class="p">$ </span>pip install awdk</div>
          <p style="margin-top:12px"><strong>You will see:</strong> <code>Successfully installed awdk …</code>
          with a version number.</p>
          <div class="term-title" style="margin-top:14px">Start a brain</div>
          <div class="term"><span class="p">$ </span>adk quickstart-local</div>
          <p style="margin-top:12px"><strong>You will see:</strong> five numbered steps, <code>[1/5] Detecting
          hardware…</code> through <code>[5/5]</code>: it detects your CPU and memory, picks a backend
          (plain llama.cpp with no dependencies, or Ollama if you already have it), downloads a model
          sized for you, asks it a question and checks an answer comes back, then registers it. It
          ends with an address like <code>http://localhost:8200/v1</code> and <code>Config saved</code>.
          A failed check fails the command; quickstart means proven working.</p>
          <div class="term-title" style="margin-top:14px">Optional · the 1-bit brain, 27B in 3.8 GB</div>
          <div class="term"><span class="p">$ </span>adk bonsai-local <span class="c"># needs Docker; ~40 min the first time, seconds after</span></div>
        </div>
        <div>
          <p><strong>No Python, or none you trust?</strong> One line sets up an isolated environment
          and runs the wizard:</p>
          <div class="term"><span class="p">$ </span>curl -fsSL https://aitherium.com/install.sh | sh <span class="c"># macOS / Linux / WSL</span></div>
          <div class="term" style="margin-top:8px"><span class="p">&gt; </span>powershell -ExecutionPolicy ByPass -c "irm https://aitherium.com/install.ps1 | iex" <span class="c"># Windows</span></div>
          <p style="margin-top:16px"><strong>What you just learned.</strong> "8B" is eight billion numbers. At
          sixteen bits each that is 16 GB, too big for most laptops; quantised to four bits it is
          about 4.5 GB and almost as good, and at one bit a 27B brain fits in 3.8 GB. The kit picks
          the trade that fits your machine so you do not have to. Unplug the network after this
          step. It still answers.</p>
          <p><strong>Stuck?</strong> <code>adk doctor</code> names the problem. If the download stops,
          run the same command again; it resumes.</p>
          <div class="links" style="display:flex;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem">
            <a href="{CODEX_PATH}/01-install-awdk.md" rel="noopener">chapter 1 ↗</a>
            <a href="{CODEX_PATH}/02-first-brain.md" rel="noopener">chapter 2 ↗</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="tight" id="talk">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>03</b>talk to it · 5 min</div>
        <div>
          <h2>Ask it one question. Then open a&nbsp;chat.</h2>
        </div>
      </div>
      <div class="two-col">
        <div>
          <div class="term"><span class="p">$ </span>adk backend test</div>
          <p style="margin-top:12px"><strong>You will see:</strong> <code>Provider: …</code>, one line of
          <code>Response: …</code> from your brain, and <code>Status: OK</code>. If it says FAILED,
          the brain from step 02 is not running; <code>adk backend status</code> shows what the kit
          expects and <code>adk quickstart-local</code> restarts it.</p>
          <div class="term" style="margin-top:14px"><span class="p">$ </span>adk start</div>
          <p style="margin-top:12px"><strong>You will see:</strong> a chat, zero config, against the brain you
          just started. Everything you type stays on the machine.</p>
        </div>
        <div>
          <p><strong>What you just learned.</strong> The kit does not care which brain is on the
          other end. The same commands work against the phone's server, the laptop's llama.cpp, a
          GPU, or a cloud key you add later. Swap the backend; the agents do not change. That is the
          whole point of the plug.</p>
          <div class="links" style="display:flex;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem">
            <a href="{CODEX_PATH}/03-talk-to-it.md" rel="noopener">chapter 3 ↗</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="tight" id="agent">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>04</b>your first agent · 15 min</div>
        <div>
          <h2>A brain, plus tools, plus a job. Three files. You will watch it use a&nbsp;tool.</h2>
          <p>A chatbot answers. An agent acts: it can run a command, read a file, send a message,
          and decide what to do next based on what happened. The difference is tools.</p>
        </div>
      </div>
      <div class="two-col">
        <div>
          <div class="term"><span class="p">$ </span>adk init my-agent<br><span class="p">$ </span>cd my-agent<br><span class="p">$ </span>python agent.py</div>
          <p style="margin-top:12px"><strong>You will see:</strong> <code>Created AitherADK project at my-agent/</code>,
          three files named (<code>agent.py</code>, <code>config.yaml</code>, <code>tools.py</code>), and
          then one greeting printed by your agent. It was asked to say hello to the world, and it
          had a <code>hello</code> tool to do it with, so it called the tool.</p>
          <p>Now open <code>agent.py</code>, change the question at the bottom, run it again. Then add
          a second tool: any Python function with a docstring, decorated the same way.</p>
          <div class="term-title" style="margin-top:14px">Optional · run it as a service</div>
          <div class="term"><span class="p">$ </span>adk run <span class="c"># Starting AitherADK server — identity: my-agent, port: 8080</span></div>
        </div>
        <div>
          <div class="term-title">agent.py, as scaffolded</div>
          <div class="term"><span class="c">&quot;&quot;&quot;My AitherADK agent.&quot;&quot;&quot;</span><br><br>from adk import AitherAgent, tool<br><br>agent = AitherAgent("my-agent")<br><br><br>@agent.tool<br>def hello(name: str) -&gt; str:<br>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c">&quot;&quot;&quot;Greet someone by name.&quot;&quot;&quot;</span><br>&nbsp;&nbsp;&nbsp;&nbsp;return f"Hello, {{name}}!"<br><br><br>async def main():<br>&nbsp;&nbsp;&nbsp;&nbsp;response = await agent.chat("Say hello to the world")<br>&nbsp;&nbsp;&nbsp;&nbsp;print(response.content)<br><br><br>if __name__ == "__main__":<br>&nbsp;&nbsp;&nbsp;&nbsp;import asyncio<br>&nbsp;&nbsp;&nbsp;&nbsp;asyncio.run(main())</div>
          <p style="margin-top:14px"><strong>What you just learned.</strong> The docstring is the tool's
          description; the brain reads it to decide when to call the function. Memory, safety
          filtering and effort routing are already on; you did not configure them. This is the
          same loop the foundation's own fleet runs, pointed at a smaller brain.</p>
          <div class="links" style="display:flex;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem">
            <a href="{CODEX_PATH}/04-build-an-agent.md" rel="noopener">chapter 4 ↗</a>
            <a href="{PAGES}/awdk/" rel="noopener">awdk docs ↗</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="tight" id="packs">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>05</b>packs · 15 min</div>
        <div>
          <h2>Someone already built the agent you want. Install&nbsp;it.</h2>
        </div>
      </div>
      <div class="two-col">
        <div>
          <div class="term"><span class="p">$ </span>adk packs<br><span class="p">$ </span>adk install pack:&lt;name&gt;</div>
          <p style="margin-top:12px"><strong>You will see:</strong> a table of packs, each with a name and a
          one-line purpose; then the pack applied to your agent. Names are case-sensitive; copy
          them exactly. An empty table means the bundled catalogue is missing:
          <code>pip install --force-reinstall awdk</code> restores it.</p>
        </div>
        <div>
          <p><strong>What you just learned.</strong> A pack is a whole agent in one file: its brain
          settings, its tools, its skills, its personality. Packs compose, and a pack that extends
          a self-hosted agent extends a hosted one identically. This is how the operator economy
          gets built: you install a pack for the print shop, not a SaaS subscription.</p>
          <div class="links" style="display:flex;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem">
            <a href="{CODEX_PATH}/05-agent-packs.md" rel="noopener">chapter 5 ↗</a>
            <a href="{GH}/awskills" rel="noopener">awskills ↗</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="tight" id="gpu">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>06</b>more hardware</div>
        <div>
          <h2>A GPU, a LAN, or a cloud key. Same agents, same&nbsp;code.</h2>
        </div>
      </div>
      <div class="record-wrap"><div class="record">
        <table>
          <thead><tr><th>You have</th><th>Type this</th><th>You get</th></tr></thead>
          <tbody>
            <tr><td>A GPU with 6 GB or more</td><td><code>adk quickstart</code></td><td>vLLM or Ollama auto-detected, models pulled, ready to chat. TurboQuant 4-bit runs on cards as small as 6 GB.</td></tr>
            <tr><td>A whole LAN of machines</td><td><code>adk deploy grid</code></td><td>One model spread across the boxes you own, routed by effort. We split a 27B across a gaming GPU and an ARM box over an ordinary LAN, and it answered.</td></tr>
            <tr><td>Just an API key</td><td><code>adk quickstart --cloud</code></td><td>Anthropic, OpenAI or DeepSeek as the brain. Cloud as overflow: keep the key for the long tail and serve the rest locally.</td></tr>
          </tbody>
        </table>
      </div></div>
      <p class="small" style="margin-top:16px"><strong>What you just learned.</strong> Effort routing: the kit
      sends small work to the small brain and only escalates when the job needs it. On a stack
      built this way, more than eighty percent of calls never leave an 8B model.
      <a href="{CODEX_PATH}/06-your-own-hardware.md" rel="noopener">chapter 6 ↗</a></p>
    </div>
  </section>

  <section class="tight" id="browser">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>07</b>in the browser</div>
        <div>
          <h2>On a desktop with a GPU, the page is the&nbsp;runtime.</h2>
          <p>Open <a href="https://aitherium.com" rel="noopener">aitherium.com</a> on a desktop with a
          WebGPU-capable browser and a GPU. The on-device Bonsai brains load into the tab itself,
          four sizes from 236 MB to 3.6 GB, chosen by what your machine can hold. No install, no
          account, no terminal. A phone tab cannot hold the weights; that is what step 01 is for.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="tight" id="mesh">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>08</b>join the mesh · optional</div>
        <div>
          <h2>Make your machine a named piece of the&nbsp;infrastructure.</h2>
        </div>
      </div>
      <div class="two-col">
        <div>
          <div class="term"><span class="p">$ </span>adk up</div>
          <p style="margin-top:12px"><strong>You will see:</strong> a device-code prompt in your browser (identity,
          not an API key), then your node registered: persistent agent, a tunnel, autostart, visible
          in the fleet within about a minute. On the phone, <code>phone.sh</code> offers the same
          step at the end, and it is not needed for the phone's own browser.</p>
        </div>
        <div>
          <p><strong>What you just learned.</strong> A node is a computer that has joined the
          network. The more ordinary people run one, the more the network is owned by its users and
          the less any one company can switch it off. Contribution is attributable to an identity,
          and an API key is not an identity.</p>
          <div class="links" style="display:flex;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem">
            <a href="get-involved.html#hardware" rel="noopener">run a node ↗</a>
            <a href="{CODEX_PATH}/08-many-agents.md" rel="noopener">chapter 8 · many agents, one repo ↗</a>
            <a href="{CODEX_PATH}/09-omnibox.md" rel="noopener">chapter 9 · a terminal that answers you ↗</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="ignite">
    <div class="container">
      <h2>Then teach <em>someone</em>.</h2>
      <p>Walk into the print shop that spends four hours a week on invoices. Deploy their agent,
      configured for their workflow, on a box in their back room. Be there at seven on a Tuesday
      when it breaks. That is the work, there is more of it than any company can serve, and it does
      not centralise. The rooms are where the people doing it already are.</p>
      <div class="actions">
        <a class="btn btn-forge" href="{RELAY}" rel="noopener">Join the rooms</a>
        <a class="btn" href="{DISCORD}" rel="noopener">The Collective on Discord</a>
        <a class="btn" href="{BLOG}/blog/you-wont-be-replaced-youll-become-an-operator" rel="noopener">The operator essay</a>
      </div>
    </div>
  </section>
"""

# ── about (the thesis) ────────────────────────────────────────────────────────

ABOUT = f"""  <section class="hero" style="padding-bottom:40px">
    <div class="container" style="display:block">
      <p class="eyebrow">The thesis <span class="sep">·</span> Aitherium Foundation</p>
      <h1>No&nbsp;hyperscale.</h1>
      <p class="lede">The foundation exists to keep the deepest layer of the AI stack, the operating
      system, the weights and the knowledge that agents run on, in the hands of the people who run
      it. Not because concentration is immoral. Because it is <strong>unnecessary</strong>, and we
      can show our work.</p>
    </div>
  </section>

  <section class="tight">
    <div class="container prose">
      <h2>The name</h2>
      <p>In Greek cosmology <em>aither</em> (αἰθήρ) was the primordial light and the upper air: the
      pure, bright medium the gods breathed, through which the heavens moved and creation flowed. We
      chose the name deliberately. Aither is the invisible medium that makes creation possible.
      AitherOS is what that medium looks like when you actually build it: an operating system where
      agents write, design, code, research and create, with persistent memory, real tools and real
      infrastructure behind them. The world thinks AI is a chatbot. We are here to show them it is a
      forge.</p>
      <p>Four things stand between a person and that forge, and the platform exists to remove each
      one.</p>
      <ul>
        <li><strong>You and your agents.</strong> A chatbot answers questions. An agent does the work.
        You say what you want; a specialist with memory, tools and a personality works out the how,
        then goes and does it.</li>
        <li><strong>You and your infrastructure.</strong> Your hardware is sitting there doing almost
        nothing. One command stands up the whole stack on a Linux box you own. No datacenter, no
        landlord, no GPU-hour markup. Sovereignty is an architecture decision.</li>
        <li><strong>You and your life.</strong> The next billion software users do not have the eyes,
        hands or patience for dropdown menus. Neither should you. You speak; creation follows.</li>
        <li><strong>You and a locked-in stack.</strong> Every service is an API. Every agent is
        addressable. Every tool composes. Open source, open architecture, open infrastructure, built
        for agents from the ground up rather than bolted on after.</li>
      </ul>

      <h2>The manifesto</h2>
      <p>Every AI company could stop training models today. We think they should. The intelligence we
      already have is enough; the problem was never intelligence, it was the poverty of the
      environment around it. The industry is running a race with no finish line, bigger models,
      denser datacenters, infinite scale, and the freight train is pointed at a society that was never
      asked whether it wanted to be dragged along.</p>
      <p>We do not believe in infinite scaling. You cannot spin up infinite agents on infinite hardware
      for zero cost, and human relationships do not scale infinitely either, and that ceiling is
      good. So we stopped chasing the bigger brain and built the body. The prompt was the spark; the
      environment was the fuel. The brain is just the plug; we built everything else, on Linux and
      Python, on hardware you own, in the open. Slow down. Build responsibly. Use the intelligence
      that already exists to steer our society instead of dragging it in front of the train. And
      remember what the only durable advantage in this field is: a system that improves itself, on
      hardware you own, doing work that matters, for longer than anyone else has. The only moat is
      time.</p>

      <h2>The premise</h2>
      <p>The last decade made AI a service. You do not own the model, the weights, the data or the
      interface; you rent all four, and the terms can change on any Tuesday. The industry's own
      explanation for why it must be this way is a chain: AI requires massive compute, massive
      compute requires massive capital, massive capital requires massive organisations, therefore AI
      will be controlled by the handful of companies that already control everything else.</p>
      <p>Only the first link is physics. The rest are business decisions, and they are already being
      unwound by the people who lend the money. Banks fund concentration because concentration is
      predictable and predictable is lendable. When the underwriters' own cost models showed the
      demand curve for rented GPU-hours flattening against self-hosting costs approaching zero, the
      loans stopped. That was arithmetic, not sentiment.</p>

      <h2>The arithmetic</h2>
      <p>A hyperscale GPU-hour has to recoup roughly three to four dollars of fully loaded cost: the
      chip, the building, the cooling, the land, the staff, the insurance, the cost of capital for an
      eighteen-month construction timeline. A consumer RTX 5090 costs about two thousand dollars,
      draws 575 watts, and sits under a desk. It runs an orchestrator model at sixty-five tokens a
      second, serves several models at once, and fine-tunes a production model in under half an hour.</p>
      <p>The rented GPU-hour sells compute at a markup that was justifiable when local models could
      not do the job. Local models can now do the job for the head of the distribution, which is
      almost all of the work. For a serious agentic workload the breakeven on owning the hardware is
      measured in months. After that every call is free. Not "pennies". Free. And when inference is
      free you can afford to be ambitious: a thirty-second awareness loop that never sleeps, a
      twelve-stage context pipeline, a nightly swarm that fires eighty model calls per coding task and
      costs the same electricity the idle GPU would have burned anyway.</p>
      <div class="aside">Every figure above is from a dated field report on the blog, with the
      hardware and the software named. The receipts section on the front page links each one.</div>

      <h2>What actually changed</h2>
      <p>Three things, and none of them was a bigger model.</p>
      <ul>
        <li><strong>Local models got good enough.</strong> Not to replace the frontier on every task.
        To handle most production workloads at zero marginal cost. An 8B model on one consumer GPU
        classifies, routes, summarises, extracts and drafts. A 14B to 32B model plans and dispatches.
        The 70B and the frontier API fire when something actually needs them.</li>
        <li><strong>Orchestration became the product.</strong> A well-orchestrated pipeline of small
        models with a surgically assembled context outperforms one large model with a garbage dump on
        real agentic work. The orchestration layer, not the model, is where the leverage is, and
        orchestration runs on hardware you own.</li>
        <li><strong>The cost of sovereignty dropped to zero.</strong> A Linux box with a GPU now runs
        a complete stack, inference, orchestration, memory, training, identity, security, with no
        external dependency at runtime. Not because we promise your data stays home. Because there is
        no code path that sends it anywhere.</li>
      </ul>

      <h2>Four problems, not one</h2>
      <p>Frontier-scale inference on consumer hardware is not one hard problem; it is four
      independent ones, each with credible open solutions built by different groups, none of which
      compose. <em>Placement</em>: which machine and tier holds which parameters. <em>Precision</em>:
      how many bits each tensor gets, driven by a different signal than placement. <em>Verification</em>:
      whether a stranger's node did the work it claims, provable with signed receipts and no
      consensus. And <em>distribution</em>: how a device owned by someone who has never opened a
      terminal joins the fabric safely and automatically.</p>
      <p>The field concentrates on the first three and assumes the fourth away. We concentrate on the
      fourth, because the other three presuppose a node that has already joined. A sovereign appliance
      that isolates contributed work in a virtual machine, so joining never means running a stranger's
      code on your host. Identity from an OAuth device flow instead of an API key, because contribution
      must be attributable and a key is not an identity. Tenant scope carried through the whole request
      path, failing closed where it cannot be determined. Agents that enroll, provision and federate
      the mesh with no human in the join path. And a graph of meshes, so a household can peer with a
      lab, a lab with an organisation, and an organisation with a public commons, without any of them
      surrendering sovereignty to the others.</p>
      <p>We publish which parts of that are deployed and which are specified but unbuilt. The
      <a href="transparency.html#deployed">record</a> says so plainly; that honesty is the paper's
      credibility and ours.</p>

      <h2>The good version of Palantir</h2>
      <p>The most expensive AI company on earth now sells this page's argument. At its own
      conference in September 2026 it had a defence contractor say that fine-tuned open models
      beat the frontier at a fraction of the cost, and its CEO keeps asking why anyone charges by
      the token for something that valuable when the customer could own the means of production.
      He is right about all of it. The difference is the last clause of each sentence. They sell
      that architecture closed, per deployment, to governments and the largest enterprises. We
      publish it: the same sealed, permissioned, retraining-on-your-own-hardware stack, as open
      code a stranger can install on a laptop, aimed at the operator with thirty clients in their
      town rather than the customer with thirty billion in revenue. Enterprises that run it this
      way report token costs of a few hundred dollars a month and the real spend moving into the
      harness that builds the applications; that is why one of our bricks is a profiler for the
      harness. When the model is a commodity, the stack is where the value goes, and a stack that
      is a commons cannot become the next landlord.</p>

      <h2>The operator</h2>
      <p>The economic corollary is the part people find hardest to believe. When the cost of writing
      software collapses, the demand for software does not shrink; it is revealed. There are tens of
      millions of small businesses running on spreadsheets, whiteboards and "we've always done it this
      way," each with dozens of processes that were never worth an engineer's hour at a hundred and
      fifty dollars and are suddenly worth an agent's minute. The work is not writing the software. It
      is integrating it into one business's unique snowflake of tools, habits and edge cases, and being
      there at seven on a Tuesday when it breaks.</p>
      <p>That work distributes because the things it needs do not centralise: trust, local knowledge,
      domain expertise, presence. A person can hold thirty to fifty of those relationships before the
      quality degrades. That ceiling is real, and it is good, because it leaves room for the next
      operator in the next town and the next industry. The equilibrium is not a few companies renting
      cognition to the world. It is a great many operators, each running their own fleet on hardware in
      a closet, plugging into composable governance when a client's industry demands it, and calling a
      frontier model for the five percent of work that needs one.</p>
      <p>You will not be replaced. You will become an operator. The foundation's job is to make sure
      the tools you operate with are yours.</p>

      <h2>What the foundation is for</h2>
      <ul>
        <li><strong>Steward the open layer.</strong> The operating system for agents and the family
        of bricks around it are developed in public and run by the foundation's own fleet first. There
        is no separate internal version.</li>
        <li><strong>Publish the weights and the recipe.</strong> Models ship with weights that load
        through open tooling on ordinary hardware, from brains that run in a browser tab to the
        serving stack for a 284B mixture of experts. And the operating doctrine, mined from real
        sessions, ships as an installable pack rather than a keynote.</li>
        <li><strong>Keep the commons joinable.</strong> The network's strength is that no company
        hosts it. The foundation runs the lanes; the community runs the nodes. The joinable public
        fabric is the largest open item on our list, and we say so.</li>
        <li><strong>Refuse the landlord model.</strong> No per-token rent on the head of the
        distribution. No phone-home in the runtime. No API key where an identity belongs. No claim
        without an instrument.</li>
      </ul>

      <h2>Who is behind it</h2>
      <p>One person, so far. David Parkhurst, <a href="https://wizzense.github.io/" rel="noopener">wizzense</a>:
      an outcome engineer who has racked the servers, run the OS at 850K-user scale, secured the
      network, trained the models, scheduled the GPUs and built the dashboard on top, and then
      built the factory that builds the software. His page is a shell you can type into; every
      number it prints was measured, and the command that measured it is printed beside it. The
      foundation exists so that what he built does not depend on him.</p>

      <h2>The honest part</h2>
      <p>This is optimistic, bordering on idealistic, and the transition is the risk. Inference is
      concentrated today, and the people holding the GPUs have leverage they could use to lock in
      customers before distributed alternatives mature. The window between "AI can displace this
      work" and "the operator economy can absorb it" could be painful. Our measurements come from one
      topology and one model family; nothing yet validates behaviour at a thousand nodes.</p>
      <p>What we have is a structural argument for why the equilibrium is distributed, a stack that
      already runs on that premise, and a discipline of publishing what we measured rather than what
      we hoped. Getting to the equilibrium is the hard part. It gets solved by building, not by waiting.</p>
      <div class="actions">
        <a class="btn btn-primary" href="programs.html">The programs</a>
        <a class="btn" href="{BLOG}/blog/sovereign-deployment-year-of-linux-desktop" rel="noopener">The long version, 2026-03 ↗</a>
      </div>
    </div>
  </section>
"""

# ── programs ──────────────────────────────────────────────────────────────────

PROGRAMS = f"""  <section class="hero" style="padding-bottom:40px">
    <div class="container" style="display:block">
      <p class="eyebrow">Programs <span class="sep">·</span> Aitherium Foundation</p>
      <h1>Four programs, one&nbsp;refusal.</h1>
      <p class="lede">Everything the foundation does maps to one of these. Each is judged by what it
      publishes, not by what it promises, and each exists to make sure nobody has to rent what they
      could own.</p>
    </div>
  </section>

  <section class="tight">
    <div class="container">
      <article class="program" id="open-source">
        <div class="n"><b>01</b>the stack</div>
        <div>
          <h2>The operating system for agents</h2>
          <p>A Linux you can hand to an agent, the runtimes it works in, and the tools it works with:
          {len(BRICKS)} public bricks, each installable on its own, each running offline, each
          replacing something you would have to trust with something you can check. The foundation's
          own fleet runs on exactly this code.</p>
          <div class="items">
            <div class="item"><h4>awnix · the OS</h4><p>Bootable, immutable, atomic rollback, no
            passwords, zero open ports. A fresh cloud box became a self-registered AI runner in 969
            seconds.</p><a class="more" href="{PAGES}/awnix/" rel="noopener">docs ↗</a></div>
            <div class="item"><h4>awdk · the runtime</h4><p>Three lines of code, any backend, zero
            lock-in. Five concepts: agent, backend, effort routing, memory, fleet. Drives your GPU,
            a CPU-only brain, or a cloud key with the same code.</p><a class="more" href="{PAGES}/awdk/" rel="noopener">docs ↗</a></div>
            <div class="item"><h4>awnode · the body</h4><p>A local gateway that exposes your hardware
            to agents through a secure tunnel. Cloud agents possess the machine; your data never
            leaves it.</p><a class="more" href="{PAGES}/awnode/" rel="noopener">docs ↗</a></div>
            <div class="item"><h4>The trust plane</h4><p>Who is this caller, what may they do, what
            did they actually do: kept as three bricks on purpose, because one component that answers
            all three can quietly answer all three wrongly. Every gate fails closed.</p><a class="more" href="index.html#stack">the table ↗</a></div>
          </div>
          <p class="small" style="margin-top:18px">Licences: Apache-2.0 and MIT across most bricks;
          the platform core and awdk under BSL 1.1 with a dated conversion to Apache-2.0. The full
          map is on the <a href="transparency.html#licences">record</a>.</p>
        </div>
      </article>

      <article class="program" id="open-models">
        <div class="n"><b>02</b>weights &amp; commons</div>
        <div>
          <h2>Open weights, and a fabric to run them on</h2>
          <p>A model nobody can run is a press release. Everything the foundation serves loads through
          open tooling on ordinary hardware, from a brain in a browser tab to a 284B mixture of
          experts across three machines in a house. The next build is the joinable public fabric:
          any device contributes what it has, is credited for it, and consumes frontier-scale
          inference in return, without trusting any other participant.</p>
          <div class="items">
            <div class="item"><h4>Bonsai · in the browser</h4><p>Four sizes from 236 MB to 3.6 GB,
            running on the visitor's own GPU through WebGPU. No install, no account, no terminal. The
            page is the runtime.</p><a class="more" href="https://aitherium.com/" rel="noopener">try it ↗</a></div>
            <div class="item"><h4>Bonsai · on CPU, offline</h4><p>One command pulls a ~300 MB image
            and serves it locally. The floor for "an agent on literally anything."</p><a class="more" href="get-involved.html#run">run it ↗</a></div>
            <div class="item"><h4>The pool</h4><p>DeepSeek-class mixture-of-experts served across a
            DGX Spark, an RTX 5090 and a Ryzen box on 1 GbE at 23.6 tokens a second, with the four
            falsified hypotheses published alongside the one that held.</p><a class="more" href="{BLOG}/blog/one-model-two-machines-distributed-inference-on-hardware-we-own" rel="noopener">the receipt ↗</a></div>
            <div class="item"><h4>AitherNet · the commons</h4><p>Identity-based enrollment, VM-isolated
            contribution, fail-closed tenancy, meshes that federate. Deployed in part, specified in
            full, honestly tabled.</p><a class="more" href="transparency.html#deployed">deployed vs specified ↗</a></div>
          </div>
        </div>
      </article>

      <article class="program" id="education">
        <div class="n"><b>03</b>the doctrine</div>
        <div>
          <h2>The operator doctrine</h2>
          <p>The thesis says the coming wave turns people into operators rather than casualties. That
          is only true if the knowledge to operate is actually taught. This program publishes the
          teaching: not a blog post about being smart, an installable pack distilled from 27,939 real
          prompts across 3,183 sessions, re-measured on held-out data.</p>
          <div class="items">
            <div class="item"><h4>The path</h4><p>Ten short chapters from "what is an agent?" to a
            terminal that answers you, with the command to type beside every idea. This site's
            <a href="start.html">Start</a> page is the phone-first front door to it.</p><a class="more" href="{PAGES}/awknowledge/" rel="noopener">the codex ↗</a></div>
            <div class="item"><h4>The laws</h4><p>Nineteen laws for running a coding agent so the
            result survives. Each was a real failure first; each carries its evidence.</p><a class="more" href="{GH}/awknowledge" rel="noopener">read ↗</a></div>
            <div class="item"><h4>The man page</h4><p>Every brick, stack and law, offline, on your
            machine: <code>pip install awkno</code>.</p><a class="more" href="{GH}/awkno" rel="noopener">awkno ↗</a></div>
            <div class="item"><h4>Field reports</h4><p>Engineering notes, measurements and
            corrections from running the fleet, in the order they happened.</p><a class="more" href="{BLOG}" rel="noopener">the blog ↗</a></div>
          </div>
        </div>
      </article>

      <article class="program" id="community">
        <div class="n"><b>04</b>the commons</div>
        <div>
          <h2>Infrastructure the community hosts</h2>
          <p>A commons nobody runs is a museum. The network's strength is that it is not hosted by one
          company; it is hosted by its users. The foundation runs the rooms and the lanes. The
          community runs the nodes, and the more distributed the hardware, the harder it is for anyone
          to switch the network off.</p>
          <div class="items">
            <div class="item"><h4>The rooms</h4><p>Public chat on the open relay, where the builders and
            operators actually talk, ask and ship; and the Collective on Discord for the longer
            conversations.</p><a class="more" href="{RELAY}" rel="noopener">the relay ↗</a> &nbsp; <a class="more" href="{DISCORD}" rel="noopener">Discord ↗</a></div>
            <div class="item"><h4>The nodes</h4><p>A laptop, a workstation, a box in a closet. One
            command installs the stack and the node registers itself.</p><a class="more" href="get-involved.html#hardware">run a node ↗</a></div>
            <div class="item"><h4>The builders</h4><p>Seventy-odd public repositories and a
            contribution lane that starts with an issue.</p><a class="more" href="{GH}" rel="noopener">GitHub ↗</a></div>
            <div class="item"><h4>The record</h4><p>What is deployed, what is specified, what is not
            yet published. Updated when reality changes.</p><a class="more" href="transparency.html">inspect ↗</a></div>
          </div>
        </div>
      </article>
    </div>
  </section>

  <section class="ignite">
    <div class="container">
      <h2>Every program needs <em>hands</em>.</h2>
      <p>Code, weights, teaching and the commons all run on people who show up.</p>
      <div class="actions"><a class="btn btn-forge" href="get-involved.html">Get involved</a></div>
    </div>
  </section>
"""

# ── transparency ──────────────────────────────────────────────────────────────

TRANSPARENCY = f"""  <section class="hero" style="padding-bottom:40px">
    <div class="container" style="display:block">
      <p class="eyebrow">The record <span class="sep">·</span> Aitherium Foundation</p>
      <h1>Everything below is a link, not a&nbsp;claim.</h1>
      <p class="lede">The foundation is accountable to anyone who inspects it, not to its own prose.
      Where the record does not exist yet, this page says so rather than pretending. That line
      changes when the record does.</p>
    </div>
  </section>

  <section class="tight" id="surfaces">
    <div class="container">
      <span class="kicker">What anyone can inspect right now</span>
      <div class="record-wrap"><div class="record">
        <table>
          <thead><tr><th>Surface</th><th>What it shows</th><th>State</th></tr></thead>
          <tbody>
            <tr><td><a href="{GH}" rel="noopener">Public repositories</a></td><td>76 public repos on the org: source, issues, and the full change record. {len(BRICKS)} of them are registered bricks with docs pages.</td><td class="st live">live · {MEASURED}</td></tr>
            <tr><td><a href="{BLOG}" rel="noopener">The blog</a></td><td>243 published field reports, measurements and corrections. This site points at it rather than duplicating it.</td><td class="st live">live · {MEASURED}</td></tr>
            <tr><td><a href="{PAGES}/awknowledge/" rel="noopener">The codex</a></td><td>The operating doctrine, its nineteen laws and the evidence behind each.</td><td class="st live">live</td></tr>
            <tr><td><a href="{GH}/aitherium-org" rel="noopener">This site</a></td><td>Plain HTML in a public repo. The brick table is rendered from a dated snapshot of the registry, committed alongside the pages.</td><td class="st live">live</td></tr>
            <tr><td>Annual financial report</td><td>Income, expenses, and how contributed funds were used.</td><td class="st none">not yet published</td></tr>
            <tr><td>Board &amp; governance record</td><td>Who governs, how they are chosen, and the decisions they make.</td><td class="st none">not yet published</td></tr>
          </tbody>
        </table>
      </div></div>
    </div>
  </section>

  <section class="tight" id="licences">
    <div class="container">
      <span class="kicker">Licences, as they actually are</span>
      <p>"Open source" is not one licence. The map below is the decision record, and the reasoning
      behind rejecting a source-available licence for the whole estate is published with it: an
      unenforceable promise chills the users it cannot catch.</p>
      <div class="record-wrap"><div class="record">
        <table>
          <thead><tr><th>Tree</th><th>Licence</th><th>Note</th></tr></thead>
          <tbody>
            <tr><td>awgit · awgraph · awrelay · awrepl · awresearch · awrtifact</td><td class="st live">Apache-2.0</td><td>Use, modify, redistribute, patent grant.</td></tr>
            <tr><td>awskills · awnode · awpredict · awknowledge</td><td class="st live">MIT</td><td>Use, modify, redistribute.</td></tr>
            <tr><td>awdk · awsh · the platform core</td><td class="st spec">BSL 1.1</td><td>Free for personal and internal use; commercial hosted-service use needs a licence. Converts to Apache-2.0 on 2030-02-07.</td></tr>
            <tr><td>Other bricks</td><td class="st spec">per repo</td><td>Each repo carries its own LICENSE file; a brick without one is a defect, and a gate looks for it.</td></tr>
            <tr><td>Model weights</td><td class="st spec">per model</td><td>Governed by each model's own licence and tracked in a catalogue; commercial use is gated per entry.</td></tr>
          </tbody>
        </table>
      </div></div>
    </div>
  </section>

  <section class="tight" id="deployed">
    <div class="container">
      <span class="kicker">The commons: deployed versus specified</span>
      <p>Honesty about this table is the whole credibility of the thesis. From the AitherNet technical
      report, 2026-08. "Specified" means the contract is written and the implementation is not.</p>
      <div class="record-wrap"><div class="record">
        <table>
          <thead><tr><th>Capability</th><th>State</th></tr></thead>
          <tbody>
            <tr><td>Mandatory scheduling hop: priority tiers, per-backend caps, slot reservation, circuit breaking</td><td class="st live">deployed</td></tr>
            <tr><td>Identity-based mesh across heterogeneous nodes</td><td class="st live">deployed</td></tr>
            <tr><td>Content-addressed storage plane with mesh replication</td><td class="st live">deployed</td></tr>
            <tr><td>Model catalogue with multi-backend routing and per-tenant entitlement</td><td class="st live">deployed</td></tr>
            <tr><td>Browser (WebGPU) and mobile runtime for small models</td><td class="st live">deployed</td></tr>
            <tr><td>Constrained-device inference (28.9M parameters on an $8 microcontroller)</td><td class="st live">deployed</td></tr>
            <tr><td>Transport recovery: reconnect, session identity, window replay</td><td class="st live">deployed</td></tr>
            <tr><td>Multi-tier mixture-of-experts pool across unified memory, GPU and DDR5</td><td class="st live">deployed</td></tr>
            <tr><td>Placement feedback loop (routing heat, lookahead, hysteresis)</td><td class="st spec">specified, not implemented</td></tr>
            <tr><td>Receipt-based verification of untrusted contribution</td><td class="st spec">specified, not implemented</td></tr>
            <tr><td>Incast-grade transport for hundreds of nodes</td><td class="st spec">specified, scaffolded, unproven</td></tr>
            <tr><td>Precision map as a first-class artifact property</td><td class="st spec">specified, not implemented</td></tr>
            <tr><td>The joinable public fabric (any stranger's device contributes and is credited)</td><td class="st spec">the next build</td></tr>
          </tbody>
        </table>
      </div></div>
      <p class="small" style="margin-top:16px">Threats to validity, stated in the same report: one
      deployment, one model family, the 98%-compute figure is derived rather than profiled, and
      nothing yet validates behaviour at a thousand nodes.</p>
    </div>
  </section>

  <section class="ignite">
    <div class="container">
      <h2>Watch the record <em>yourself</em>.</h2>
      <p>Follow the repositories and the blog. The record updates more often than this page does, and
      when we are wrong, the correction prints at the same volume.</p>
      <div class="actions"><a class="btn btn-forge" href="{GH}" rel="noopener">Follow on GitHub</a><a class="btn" href="{BLOG}" rel="noopener">Read the blog</a></div>
    </div>
  </section>
"""

# ── get involved ──────────────────────────────────────────────────────────────

GET_INVOLVED = f"""  <section class="hero" style="padding-bottom:40px">
    <div class="container" style="display:block">
      <p class="eyebrow">Get involved <span class="sep">·</span> Aitherium Foundation</p>
      <h1>The open layer is built by people who show&nbsp;up.</h1>
      <p class="lede">Four ways in, in the order that matters. Every one of them starts on hardware
      you already own.</p>
    </div>
  </section>

  <section class="tight" id="run">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>01</b>run it</div>
        <div>
          <h2>Run a real model on your own&nbsp;machine.</h2>
          <p>No GPU, no API key, no account. Pick the row that matches what you have; the
          <a href="start.html">guided path</a> walks every row with what you will see at each step,
          starting on a phone.</p>
        </div>
      </div>
      <div class="record-wrap"><div class="record">
        <table>
          <thead><tr><th>You have</th><th>Run this</th><th>You get</th></tr></thead>
          <tbody>
            <tr><td>Nothing, not even Python</td><td><code>curl -fsSL https://aitherium.com/install.sh | sh</code></td><td>An isolated environment and a first-run wizard.</td></tr>
            <tr><td>No GPU, no API key</td><td><code>pip install awdk &amp;&amp; adk bonsai-local</code></td><td>A Bonsai brain, free, offline, on CPU. ~300 MB, serves on :8090.</td></tr>
            <tr><td>A GPU with 6 GB or more</td><td><code>adk quickstart</code></td><td>vLLM or Ollama auto-detected, models pulled, ready to chat.</td></tr>
            <tr><td>Just an API key</td><td><code>adk quickstart --cloud</code></td><td>Cloud inference, same agents, same code.</td></tr>
            <tr><td>A whole LAN of machines</td><td><code>adk deploy grid</code></td><td>Multi-machine, effort-routed inference across your own devices.</td></tr>
          </tbody>
        </table>
      </div></div>
      <p class="small" style="margin-top:16px">Then <code>adk start</code> to talk to your agent, and
      <code>adk doctor</code> when something is wrong; it names the problem. Full paths in the
      <a href="{PAGES}/awdk/" rel="noopener">awdk docs</a>.</p>
    </div>
  </section>

  <section class="tight" id="hardware">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>02</b>hardware</div>
        <div>
          <h2>Run a node. Become the&nbsp;infrastructure.</h2>
          <p>The network's strength is that no company hosts it. Every machine a member runs is
          infrastructure the community owns, and the more distributed the hardware, the harder it is
          for anyone to control the network.</p>
        </div>
      </div>
      <div class="paths">
        <div class="path">
          <span class="k">a gateway</span>
          <h3>Expose your hardware to your agents</h3>
          <p>awnode is a local MCP gateway: your apps, your models, your files, reachable by agents
          through a secure tunnel while the data stays on the box.</p>
          <div class="term"><span class="p">$ </span>pip install awnode<br><span class="p">$ </span>awnode start</div>
          <a href="{PAGES}/awnode/" rel="noopener">awnode docs ↗</a>
        </div>
        <div class="path">
          <span class="k">the whole stack</span>
          <h3>One command, the whole world</h3>
          <p>Installs the stack and registers the node. The same one-liner the foundation uses on its
          own machines.</p>
          <div class="term"><span class="p">$ </span>curl -fsSL https://launch.aitherium.com | bash</div>
          <a href="{GH}/awnode" rel="noopener">source ↗</a>
        </div>
        <div class="path">
          <span class="k">an appliance</span>
          <h3>Boot a box that owns itself</h3>
          <p>awnix: immutable, rollback-able, no password, zero open ports. Hand the whole machine to
          an agent; the box is the sandbox.</p>
          <div class="term"><span class="p">$ </span>podman build -t awnix -f Containerfile .</div>
          <a href="{PAGES}/awnix/" rel="noopener">awnix docs ↗</a>
        </div>
      </div>
    </div>
  </section>

  <section class="tight" id="contribute">
    <div class="container">
      <div class="section-head">
        <div class="num"><b>03</b>code</div>
        <div>
          <h2>Contribute to the open&nbsp;source.</h2>
          <p>The bricks, the docs, and this website are public repositories in the community's
          hands. Start with an issue, or bring your own fix. Every brick's README opens with the
          same line: what you would have had to trust, and what you can now check.</p>
        </div>
      </div>
      <div class="items" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px">
        <div class="item"><h4>The bricks</h4><p>{len(BRICKS)} public repositories, each small enough to read in an evening.</p><a class="more" href="{GH}" rel="noopener">github.com/Aitherium ↗</a></div>
        <div class="item"><h4>awdk</h4><p>The runtime most other bricks pair with. Issues and pull requests welcome.</p><a class="more" href="{GH}/awdk" rel="noopener">source ↗</a></div>
        <div class="item"><h4>The codex</h4><p>A law is a real failure with its evidence. If you have one, it belongs here.</p><a class="more" href="{GH}/awknowledge" rel="noopener">source ↗</a></div>
        <div class="item"><h4>This website</h4><p>Plain HTML, deliberately. A typo fix and a new page are both welcome.</p><a class="more" href="{GH}/aitherium-org" rel="noopener">source ↗</a></div>
      </div>
    </div>
  </section>

  <section class="tight" id="community">
    <div class="container two-col">
      <div>
        <span class="kicker"><b>04</b> · the rooms</span>
        <h2>Show up where the work is&nbsp;visible.</h2>
      </div>
      <div>
        <p>Public chat on the open relay is where the builders and operators actually talk, ask and
        ship. It is persistent, it is public, and the knowledge of the whole ecosystem moves through
        it daily. Everything else on this page is easier after this step.</p>
        <div class="actions"><a class="btn btn-primary" href="{RELAY}" rel="noopener">Join the rooms</a><a class="btn" href="{DISCORD}" rel="noopener">The Collective on Discord</a></div>
      </div>
    </div>
  </section>

  <section class="ignite" id="support">
    <div class="container">
      <h2>Support the <em>foundation</em>.</h2>
      <p>Contributions fund the training runs, the hardware, and the people who keep the open layer
      maintained. Giving is recorded in the public record; where that record does not exist yet, the
      transparency page says so. For sponsorship or major giving, the conversation starts with an
      email.</p>
      <div class="actions"><a class="btn btn-forge" href="{CONTACT}">foundation@aitherium.org</a><a class="btn" href="transparency.html">The record</a></div>
    </div>
  </section>
"""

# ── news ──────────────────────────────────────────────────────────────────────

POSTS = [
    ("2026-08-14", "Earned Arrogance", "A defence of being insufferable about the things you can prove. Humility is a virtue when you are guessing; the git history timestamps every call.", f"{BLOG}/blog/earned-arrogance"),
    ("2026-08-14", "I Measured My Software Factory: 36 Million Lines in 10 Months", "Every repo, deduped by root commit, author-filtered, lockfiles stripped. Then the harder query: how much of it survived.", f"{BLOG}/blog/i-measured-my-software-factory-36-million-lines-in-10-months"),
    ("2026-07-24", "One Model, Two Machines", "A 27B model with its brain cut in half, running on a gaming GPU and an idle ARM box at once, over an ordinary LAN. It answered.", f"{BLOG}/blog/one-model-two-machines-distributed-inference-on-hardware-we-own"),
    ("2026-06-13", "The Only Moat Is Time", "Weights leak, architectures get cloned, even hidden reasoning is distillable. The one thing that cannot be copied is a system that has been improving itself for longer than you have.", f"{BLOG}/blog/the-only-moat-is-time"),
    ("2026-05-21", "Local LLMs Actually Scale: Receipts From a 208-Service Stack", "A reply to the 'local is cope' crowd from someone running the whole stack on local GPUs with zero hyperscaler spend. The hard part is not the model; it is the OS around it.", f"{BLOG}/blog/local-llms-actually-scale-receipts-from-a-208-service-stack"),
    ("2026-03-26", "The Brain Is a Plug", "Everyone is building a bigger brain. We built the body. The model is one hot-swappable node in an organism that thinks, acts, heals and learns.", f"{BLOG}/blog/the-brain-is-a-plug"),
    ("2026-03-08", "Sovereign AI: the Year of the Linux Desktop Was Never About the Desktop", "Banks pulling datacenter loans and a bash script that turns a bare box into a complete AI operating system are the same story.", f"{BLOG}/blog/sovereign-deployment-year-of-linux-desktop"),
    ("2026-03-05", "You Won't Be Replaced by AI. You'll Become an Operator.", "The demand surface for software is infinite, compute is not free, and relationships do not scale. That distributes opportunity instead of concentrating it.", f"{BLOG}/blog/you-wont-be-replaced-youll-become-an-operator"),
    ("2026-03", "We Gave an AI Agent Its Own Linux Box", "Stop sandboxing the agent; give it the whole box, a lifeline it cannot disable, and an ISO that boots the entire stack with the network cable unplugged.", f"{BLOG}/blog/we-gave-an-ai-agent-its-own-linux-box"),
]


def posts() -> str:
    out = ['      <ul class="posts">']
    for d, t, x, href in POSTS:
        out.append(f'        <li><span class="d">{d}</span><div><h3><a href="{href}" rel="noopener">{esc(t)}</a></h3><p>{esc(x)}</p></div></li>')
    out.append('      </ul>')
    return "\n".join(out)


NEWS = f"""  <section class="hero" style="padding-bottom:40px">
    <div class="container" style="display:block">
      <p class="eyebrow">News <span class="sep">·</span> Aitherium Foundation</p>
      <h1>The blog is the&nbsp;record.</h1>
      <p class="lede">Field reports, doctrine, measurements and corrections are published at
      <a href="{BLOG}" rel="noopener">blog.aitherium.com</a>, in the order they happened. This page
      points to it rather than duplicating it, so there is one record, not two.</p>
    </div>
  </section>

  <section class="tight">
    <div class="container">
      <span class="kicker">Selected · the thesis in the order it was written</span>
{posts()}
      <div class="actions"><a class="btn btn-primary" href="{BLOG}" rel="noopener">All 243 posts</a></div>
    </div>
  </section>
"""


def main() -> None:
    page("index.html", "Aitherium Foundation — The Element of Creation",
         "Every AI company could stop training models today. We think they should. No infinite scaling: an "
         "open operating system for agents on hardware you own, the weights and doctrine to run it, and "
         "the foundation that keeps it that way.", INDEX)
    page("start.html", "Start building — Aitherium Foundation",
         "Build with agents, starting on the phone in your pocket: eight steps on hardware you own, "
         "each with what you need, what you type, and what you will see.", START)
    page("about.html", "The thesis — Aitherium Foundation",
         "Why the concentration thesis is wrong on arithmetic, what actually changed, the four problems of "
         "distributed inference, and the operator economy.", ABOUT)
    page("programs.html", "Programs — Aitherium Foundation",
         "The stack, open weights and the commons, the operator doctrine, and the infrastructure the "
         "community hosts.", PROGRAMS)
    page("transparency.html", "The record — Aitherium Foundation",
         "What anyone can inspect right now, the licence map as it actually is, and which parts of the "
         "commons are deployed versus specified.", TRANSPARENCY)
    page("get-involved.html", "Get involved — Aitherium Foundation",
         "Run a real model on your own machine, run a node, contribute code, join the rooms, support the "
         "foundation.", GET_INVOLVED)
    page("news.html", "News — Aitherium Foundation",
         "The blog is the record. Selected posts that carry the thesis, in the order they were written.", NEWS)


if __name__ == "__main__":
    main()
