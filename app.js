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
