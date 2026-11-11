/**
 * NEXUS Elite Node UI — registry derivative helpers (token-neutral, C1).
 * Symbiosis: Node states UI; UI never defines the Node.
 */
(function (global) {
  "use strict";

  function pad(n) {
    return String(n).padStart(2, "0");
  }

  function formatAge(ms) {
    if (!Number.isFinite(ms) || ms < 0) return "UNKNOWN";
    var s = Math.floor(ms / 1000);
    var d = Math.floor(s / 86400);
    s %= 86400;
    var h = Math.floor(s / 3600);
    s %= 3600;
    var m = Math.floor(s / 60);
    s %= 60;
    if (d > 0) return d + "d " + pad(h) + "h " + pad(m) + "m " + pad(s) + "s";
    return pad(h) + "h " + pad(m) + "m " + pad(s) + "s";
  }

  function bindAgeTimer(el, birthIso) {
    if (!el || !birthIso) return;
    var birth = Date.parse(birthIso);
    if (!Number.isFinite(birth)) {
      el.textContent = "UNKNOWN";
      return;
    }
    var reduced =
      typeof matchMedia === "function" &&
      matchMedia("(prefers-reduced-motion: reduce)").matches;

    function tick() {
      el.textContent = formatAge(Date.now() - birth);
    }
    tick();
    if (reduced) return;
    var id = setInterval(tick, 1000);
    el.dataset.timerId = String(id);
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderRelationGraph(svgEl, listEl, node) {
    if (!node) return;
    var relations = Array.isArray(node.relations) ? node.relations : [];
    var w = 640;
    var h = 280;
    var cx = 160;
    var cy = h / 2;
    var rx = 420;
    var ry = h / 2;

    if (svgEl) {
      svgEl.setAttribute("viewBox", "0 0 " + w + " " + h);
      svgEl.setAttribute("role", "img");
      svgEl.setAttribute(
        "aria-label",
        "Relation graph for " + (node.node_name || "node")
      );
      var parts = [];
      parts.push(
        '<circle class="g-hub" cx="' +
          cx +
          '" cy="' +
          cy +
          '" r="46"></circle>'
      );
      parts.push(
        '<text class="g-hub-label" x="' +
          cx +
          '" y="' +
          (cy + 4) +
          '" text-anchor="middle">HOMEOSTASIS</text>'
      );
      relations.forEach(function (rel, i) {
        var t =
          relations.length === 1
            ? 0.5
            : i / Math.max(relations.length - 1, 1);
        var angle = -0.55 + t * 1.1;
        var tx = rx;
        var ty = ry + Math.sin(angle) * 90;
        parts.push(
          '<line class="g-edge" x1="' +
            (cx + 46) +
            '" y1="' +
            cy +
            '" x2="' +
            (tx - 70) +
            '" y2="' +
            ty +
            '"></line>'
        );
        parts.push(
          '<rect class="g-sat" x="' +
            (tx - 70) +
            '" y="' +
            (ty - 22) +
            '" width="140" height="44" rx="2"></rect>'
        );
        parts.push(
          '<text class="g-sat-type" x="' +
            tx +
            '" y="' +
            (ty - 4) +
            '" text-anchor="middle">' +
            escapeHtml(rel.type || "?") +
            "</text>"
        );
        parts.push(
          '<text class="g-sat-tgt" x="' +
            tx +
            '" y="' +
            (ty + 14) +
            '" text-anchor="middle">' +
            escapeHtml(shortTarget(rel.target)) +
            "</text>"
        );
      });
      svgEl.innerHTML = parts.join("");
    }

    if (listEl) {
      if (!relations.length) {
        listEl.innerHTML = "<li>No relations declared</li>";
        return;
      }
      listEl.innerHTML = relations
        .map(function (rel) {
          return (
            "<li><span class=\"rel-type\">" +
            escapeHtml(rel.type) +
            "</span> → " +
            escapeHtml(rel.target) +
            "</li>"
          );
        })
        .join("");
    }
  }

  function shortTarget(t) {
    if (!t) return "?";
    var s = String(t);
    if (s.length <= 22) return s;
    return s.slice(0, 10) + "…" + s.slice(-8);
  }

  function fillSummary(root, registry) {
    if (!root || !registry || !registry.summary) return;
    var s = registry.summary;
    var map = {
      "data-born": s.total_born_nodes,
      "data-live": s.currently_live,
      "data-latest": s.latest_birth,
      "data-status": s.current_homeostasis_status,
    };
    Object.keys(map).forEach(function (attr) {
      var el = root.querySelector("[" + attr + "]");
      if (el) el.textContent = map[attr] == null ? "—" : String(map[attr]);
    });
  }

  async function loadJson(url) {
    var res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("fetch " + url + " → " + res.status);
    return res.json();
  }

  global.NexusElite = {
    formatAge: formatAge,
    bindAgeTimer: bindAgeTimer,
    renderRelationGraph: renderRelationGraph,
    fillSummary: fillSummary,
    loadJson: loadJson,
    escapeHtml: escapeHtml,
  };
})(typeof window !== "undefined" ? window : globalThis);
