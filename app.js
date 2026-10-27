/* Aitherium Foundation — aitherium.org
   Progressive enhancement only. Every page is complete with JS off:
   the nav is a list, the periodic-table cells are real links, the detail
   panel shows the first element by default. This file adds the mobile nav
   toggle and lets a hovered / focused element cell fill the detail panel. */
(function () {
  'use strict';

  // ── light / dark ─────────────────────────────────────────────────────
  // Light is the default; the head script already applied any stored choice
  // before first paint. This only wires the menubar switch and persists it.
  var root = document.documentElement;
  var KEY = 'aitherium-theme';
  function syncSwitch(btn) {
    var dark = root.getAttribute('data-theme') === 'dark';
    btn.setAttribute('aria-pressed', String(dark));
    var label = dark ? 'Light mode' : 'Dark mode';
    btn.setAttribute('aria-label', label);
    btn.setAttribute('title', label);
  }
  function setTheme(theme) {
    root.setAttribute('data-theme', theme);
    try { window.localStorage.setItem(KEY, theme); } catch (e) { /* private mode: session only */ }
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', getComputedStyle(root).getPropertyValue('--fk-bg').trim());
  }
  Array.prototype.forEach.call(document.querySelectorAll('[data-theme-toggle]'), function (btn) {
    syncSwitch(btn);
    btn.addEventListener('click', function () {
      setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
      syncSwitch(btn);
    });
  });

  // ── mobile nav ───────────────────────────────────────────────────────
  var toggle = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ── built on open source ─────────────────────────────────────────────
  // The credits are not a hand-kept list: they are read live from the
  // ecosystem registry's public copy (built_on: name, upstream,
  // integrated_as, optional license). The block ships `hidden` and is only
  // revealed once at least one row rendered, so a failed fetch or an absent
  // field leaves no empty box and no error text. Remote strings go in
  // through textContent only; links must be http(s).
  var credits = document.querySelector('[data-built-on]');
  if (credits && window.fetch) {
    var rowsEl = credits.querySelector('tbody');
    window.fetch(credits.getAttribute('data-built-on'), { credentials: 'omit' })
      .then(function (r) { if (!r.ok) throw new Error(String(r.status)); return r.json(); })
      .then(function (data) {
        var list = data && Array.isArray(data.built_on) ? data.built_on : [];
        var rows = 0;
        list.forEach(function (c) {
          if (!c || typeof c.name !== 'string' || !c.name) return;
          // Second layer: the public copy is already filtered upstream, but a
          // studied-only `reference` entry must never render here even if that
          // filter regresses, and an unverified licence is never printed.
          if (c.state === 'reference' || c.status === 'reference') return;
          if (c.license_verified === false) c = Object.assign({}, c, { license: '' });
          var tr = document.createElement('tr');
          var name = document.createElement('td');
          if (typeof c.upstream === 'string' && /^https:\/\//i.test(c.upstream)) {
            var a = document.createElement('a');
            a.href = c.upstream;
            a.rel = 'noopener';
            a.textContent = c.name;
            name.appendChild(a);
          } else {
            name.textContent = c.name;
          }
          var what = document.createElement('td');
          what.textContent = typeof c.integrated_as === 'string' ? c.integrated_as : '';
          var lic = document.createElement('td');
          lic.className = 'st';
          lic.textContent = typeof c.license === 'string' ? c.license : '';
          tr.appendChild(name); tr.appendChild(what); tr.appendChild(lic);
          rowsEl.appendChild(tr);
          rows++;
        });
        if (rows) credits.hidden = false;
      })
      .catch(function () { /* stays hidden: no box, no error text */ });
  }

  // ── the periodic table ───────────────────────────────────────────────
  var table = document.querySelector('.pt');
  var detail = document.querySelector('.pt-detail');
  if (!table || !detail) return;

  var cells = Array.prototype.slice.call(table.querySelectorAll('.el[data-id]'));
  if (!cells.length) return;

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // "pip install x" is a command; "see the repo" is a sentence. Only the first gets a prompt.
  function isCommand(s) {
    return /^(pip|pipx|uv|npm|npx|git|podman|docker|curl|bash|sh|python|adk|awnode)\b/.test(String(s || '').trim());
  }

  function render(cell) {
    var d = cell.dataset;
    cells.forEach(function (c) { c.classList.toggle('on', c === cell); });
    var left =
      '<div>' +
        '<div class="hd"><span class="sy">' + esc(d.sy) + '</span>' +
        '<span class="nm">' + esc(d.id) + '</span>' +
        '<span class="kd">' + esc(d.kind) + '</span></div>' +
        '<p class="tx">' + esc(d.tagline) + '</p>' +
        (d.install ? (isCommand(d.install)
          ? '<div class="term"><span class="p">$ </span>' + esc(d.install) + '</div>'
          : '<div class="how">' + esc(d.install) + '</div>') : '') +
        '<div class="links">' +
          '<a href="' + esc(d.repo) + '" rel="noopener">source ↗</a>' +
          (d.docs ? '<a href="' + esc(d.docs) + '" rel="noopener">docs ↗</a>' : '') +
        '</div>' +
      '</div>';
    var right =
      '<div>' +
        (d.trust ? '<span class="tv trust">instead of trusting</span><p>' + esc(d.trust) + '</p>' : '') +
        (d.check ? '<span class="tv check">you check</span><p>' + esc(d.check) + '</p>' : '') +
      '</div>';
    detail.innerHTML = left + right;
  }

  var timer = 0;
  cells.forEach(function (cell) {
    cell.addEventListener('mouseenter', function () {
      window.clearTimeout(timer);
      timer = window.setTimeout(function () { render(cell); }, 60);
    });
    cell.addEventListener('focus', function () { render(cell); });
    cell.addEventListener('click', function (e) {
      // first tap on touch shows the detail; a second tap follows the link
      if (window.matchMedia && window.matchMedia('(hover: none)').matches && !cell.classList.contains('on')) {
        e.preventDefault();
        render(cell);
      }
    });
  });

  var initial = table.querySelector('.el.on[data-id]') || cells[0];
  render(initial);
})();
