/* AITHERIUM FAMILY KIT — spotlight + clock (static flavour)   @family-spotlight v1
   ⌘K / Ctrl+K (or "/") opens a search over the JSON index the page ships in
   its application/json element #fk-index: [{t: title, h: href, k: kind, d: detail}].
   This file is inlined into a script element, so it must never contain a
   closing script tag, even in a comment.
   No dependencies, nothing fetched. With JS off the ⌘K control is a plain link
   to the page's "About this OS" panel, so every destination stays reachable. */
(function () {
  var d = document;
  var clock = d.querySelector("[data-fk-clock]");
  function tick() {
    var n = new Date();
    var day = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"][n.getDay()];
    var p = function (x) { return (x < 10 ? "0" : "") + x; };
    clock.textContent = day + " " + p(n.getHours()) + ":" + p(n.getMinutes());
  }
  if (clock) { tick(); setInterval(tick, 15000); }

  var src = d.getElementById("fk-index");
  var items = [];
  try { items = JSON.parse(src ? src.textContent : "[]"); } catch (e) { items = []; }
  if (!items.length) return;

  var box = d.createElement("div");
  box.className = "fk-spot";
  box.setAttribute("role", "dialog");
  box.setAttribute("aria-modal", "true");
  box.setAttribute("aria-label", "Search");
  box.innerHTML = '<div class="fk-spot-box"><label class="fk-spot-in"><span class="fk-caps">⌘K</span>' +
    '<input type="search" autocomplete="off" spellcheck="false" placeholder="jump to a page, a brick, a command" ' +
    'aria-controls="fk-spot-list"></label><ul id="fk-spot-list" role="listbox"></ul></div>';
  d.body.appendChild(box);
  var input = box.querySelector("input"), list = box.querySelector("ul"), sel = 0, shown = [], last = null;

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function score(it, q) {
    if (!q) return 1;
    var t = (it.t || "").toLowerCase(), hay = t + " " + (it.k || "") + " " + (it.d || "").toLowerCase();
    if (t.indexOf(q) === 0) return 3;
    if (t.indexOf(q) > -1) return 2;
    return hay.indexOf(q) > -1 ? 1 : 0;
  }
  function render() {
    var q = input.value.trim().toLowerCase();
    shown = items.map(function (it, i) { return { it: it, s: score(it, q), i: i }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s || a.i - b.i; })
      .slice(0, 40);
    sel = Math.min(sel, Math.max(0, shown.length - 1));
    list.innerHTML = shown.length ? shown.map(function (x, i) {
      return '<li role="option" aria-selected="' + (i === sel) + '"><a href="' + esc(x.it.h) + '">' +
        '<span class="t' + (/^aw/.test(x.it.t || "") ? " m" : "") + '">' + esc(x.it.t) + '</span>' +
        (x.it.d ? '<span class="d">' + esc(x.it.d) + '</span>' : '') +
        '<span class="k">' + esc(x.it.k || "") + '</span></a></li>';
    }).join("") : '<li class="fk-none">nothing matches that</li>';
  }
  function open() {
    last = d.activeElement;
    box.classList.add("open");
    input.value = ""; sel = 0; render(); input.focus();
  }
  function close() {
    box.classList.remove("open");
    if (last && last.focus) last.focus();
  }
  function move(n) {
    if (!shown.length) return;
    sel = (sel + n + shown.length) % shown.length; render();
    var li = list.children[sel]; if (li && li.scrollIntoView) li.scrollIntoView({ block: "nearest" });
  }

  d.addEventListener("keydown", function (e) {
    var k = e.key, isOpen = box.classList.contains("open");
    var typing = /^(INPUT|TEXTAREA|SELECT)$/.test((e.target && e.target.tagName) || "") || (e.target && e.target.isContentEditable);
    if ((e.metaKey || e.ctrlKey) && (k === "k" || k === "K")) { e.preventDefault(); if (isOpen) close(); else open(); return; }
    if (!isOpen) { if (k === "/" && !typing) { e.preventDefault(); open(); } return; }
    if (k === "Escape") { e.preventDefault(); close(); }
    else if (k === "ArrowDown") { e.preventDefault(); move(1); }
    else if (k === "ArrowUp") { e.preventDefault(); move(-1); }
    else if (k === "Enter" && shown[sel]) { e.preventDefault(); location.href = shown[sel].it.h; }
  });
  input.addEventListener("input", function () { sel = 0; render(); });
  box.addEventListener("click", function (e) { if (e.target === box) close(); });
  var triggers = d.querySelectorAll("[data-fk-spotlight]");
  for (var i = 0; i < triggers.length; i++) {
    triggers[i].addEventListener("click", function (e) { e.preventDefault(); open(); });
  }
})();
