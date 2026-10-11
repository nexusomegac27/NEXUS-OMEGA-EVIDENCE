// SPDX-License-Identifier: Apache-2.0
// NEXUS OMEGA C1 public ticker: read-only presentation, never a control plane.
export const TICKER = Object.freeze({
  repo: "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
  publicFeed: "/status/public-event-registry.json",
  githubAPI: "https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits?sha=main&per_page=6",
  pollMs: 15 * 60 * 1000,
  maxAgeMs: 24 * 60 * 60 * 1000,
  claim: "C1_DESCRIPTIVE_ONLY"
});

const ISO = (v) => typeof v === "string" && Number.isFinite(Date.parse(v));
const HEX40 = /^[0-9a-f]{40}$/;
const TYPE = new Set(["NODE", "RELEASE", "RESEARCH", "HOLD", "SYSTEM"]);
const STATE = "TRANSPORT_ONLY_NOT_RUNTIME_AUTHORITY";

function isFresh(when, now, maxAge) {
  const age = now - Date.parse(when);
  return age >= -5 * 60 * 1000 && age <= maxAge;
}

export function parsePublicFeed(data, now = Date.now()) {
  if (!data || typeof data !== "object" ||
      data.object !== "NEXUS_PUBLIC_EVENT_REGISTRY_DERIVATIVE_V1" ||
      data.canonical_authority !== false ||
      data.claim_ceiling !== TICKER.claim ||
      !ISO(data.updated_at_utc) || !Array.isArray(data.events)) {
    throw new Error("INVALID_PUBLIC_EVENT_REGISTRY");
  }
  if (Date.parse(data.updated_at_utc) > now + 5 * 60 * 1000) {
    throw new Error("FUTURE_PUBLIC_EVENT_REGISTRY");
  }
  const sequences = new Set();
  const events = data.events.map((event) => {
    if (!event || !Number.isSafeInteger(event.canonical_sequence) ||
        event.canonical_sequence < 1 ||
        sequences.has(event.canonical_sequence) ||
        !TYPE.has(event.event_type) ||
        event.claim_ceiling !== TICKER.claim ||
        !ISO(event.timestamp_utc) ||
        Date.parse(event.timestamp_utc) > now + 5 * 60 * 1000 ||
        typeof event.short_description !== "string" ||
        typeof event.object !== "string" ||
        event.short_description.length > 180 ||
        event.object.length > 120) {
      throw new Error("INVALID_OR_DUPLICATE_EVENT");
    }
    sequences.add(event.canonical_sequence);
    // The public feed can only point to local read-only detail pages.
    const path = event.detail_link;
    const href = typeof path === "string" &&
      /^\/(?!\/)[A-Za-z0-9/_?.=&%-]{1,220}$/.test(path) &&
      !path.includes("..") ? path : null;
    return {
      id: "event:" + event.canonical_sequence,
      type: event.event_type,
      description: event.short_description,
      object: event.object,
      stamp: event.timestamp_utc,
      sequence: event.canonical_sequence,
      href,
      level: "PUBLIC_DERIVATIVE_C1"
    };
  });
  // Event registry canon explicitly orders by sequence, NOT wall clock.
  events.sort((a, b) => b.sequence - a.sequence);
  return {
    source: "WWW_PUBLIC_EVENT_REGISTRY",
    updated: data.updated_at_utc,
    freshness: isFresh(data.updated_at_utc, now, TICKER.maxAgeMs) ?
      "RECENT_SOURCE" : "STALE_SOURCE",
    events: events.slice(0, 5)
  };
}

export function parseGitHubCommits(data, now = Date.now()) {
  if (!Array.isArray(data) || data.length > 30) {
    throw new Error("INVALID_GITHUB_RESPONSE");
  }
  const seen = new Set();
  const items = [];
  for (const item of data) {
    const sha = item && item.sha;
    const stamp = item?.commit?.committer?.date;
    const msg = item?.commit?.message;
    if (!HEX40.test(sha || "") || !ISO(stamp) || typeof msg !== "string" ||
        Date.parse(stamp) > now + 5 * 60 * 1000) {
      throw new Error("INVALID_GITHUB_COMMIT");
    }
    if (seen.has(sha)) continue;
    seen.add(sha);
    const description = msg.split(/\r?\n/, 1)[0].slice(0, 160) ||
      "GitHub commit (kein Beschreibungstext)";
    items.push({
      id: "git:" + sha,
      type: "GITHUB_COMMIT",
      description,
      object: sha.slice(0, 12),
      stamp,
      href: "https://github.com/" + TICKER.repo + "/commit/" + sha,
      level: STATE,
      sha
    });
    if (items.length === 6) break;
  }
  return {
    source: "GITHUB_MAIN_COMMITS",
    updated: items.length ? items[0].stamp : null,
    freshness: items.length &&
      isFresh(items[0].stamp, now, TICKER.maxAgeMs) ?
      "RECENT_SOURCE" : "STALE_SOURCE",
    events: items
  };
}

const CSS = [
  ":host{display:block;font:inherit;color:inherit}",
  ".nexus-ticker{border:1px solid #67727a55;border-radius:12px;padding:1rem;max-width:850px}",
  ".nexus-ticker h2{font-size:1.1rem;margin:0 0 .35rem}",
  ".nexus-ticker p{margin:.25rem 0 .8rem}",
  ".nexus-ticker section{padding-top:.65rem;margin-top:.75rem;border-top:1px solid #7775}",
  ".nexus-ticker h3{font-size:.96rem;margin:0 0 .45rem}",
  ".nexus-ticker ol{margin:0;padding-left:1.3rem}",
  ".nexus-ticker li{padding:.35rem 0;overflow-wrap:anywhere}",
  ".nexus-ticker time,.nexus-ticker small{display:block;font-size:.76rem;opacity:.8}",
  ".nexus-ticker .state{font-size:.79rem;letter-spacing:.03em}",
  ".nexus-ticker a{color:inherit;text-decoration:underline;text-underline-offset:2px}",
  ".nexus-ticker .warning{font-weight:700}",
  "@media(prefers-reduced-motion:reduce){.nexus-ticker *{animation:none!important}}"
].join("\n");

function element(doc, tag, value, cls) {
  const n = doc.createElement(tag);
  if (value !== undefined) n.textContent = String(value);
  if (cls) n.className = cls;
  return n;
}

function dateLabel(stamp) {
  try {
    return new Intl.DateTimeFormat("de-DE", {
      dateStyle: "medium", timeStyle: "short", timeZone: "UTC"
    }).format(new Date(stamp)) + " UTC";
  } catch {
    return "Ungültiger Zeitpunkt";
  }
}

function renderSection(doc, parent, heading, source, error) {
  const section = element(doc, "section");
  section.append(element(doc, "h3", heading));
  const msg = source
    ? (source.freshness === "RECENT_SOURCE" ?
        "Quelle erreichbar · datierter Stand" : "Quelle veraltet · kein aktueller Zustandsnachweis")
    : "Quelle derzeit nicht erreichbar · Status unbekannt";
  section.append(element(doc, "p", msg, !source || source.freshness !== "RECENT_SOURCE" ?
    "state warning" : "state"));
  if (source?.updated) {
    section.append(element(doc, "small", "Quellenzeit: " + dateLabel(source.updated)));
  }
  const list = element(doc, "ol");
  if (!source?.events.length) {
    list.append(element(doc, "li", error ? "Kein neuer Beleg verfügbar." : "Keine Einträge."));
  } else {
    for (const ev of source.events) {
      const item = element(doc, "li");
      const a = element(doc, "a", ev.description);
      if (ev.href) {
        a.href = ev.href;
        a.rel = "noopener noreferrer";
        if (ev.href.startsWith("https:")) a.target = "_blank";
      } else {
        a.removeAttribute("href");
      }
      item.append(a);
      const time = element(doc, "time", dateLabel(ev.stamp));
      time.dateTime = ev.stamp;
      item.append(time, element(doc, "small",
        ev.type + " · " + ev.object + " · " + ev.level));
      list.append(item);
    }
  }
  section.append(list);
  parent.append(section);
}

async function boundedJSON(fetchFn, url) {
  const r = await fetchFn(url, {method: "GET", mode: "cors", credentials: "omit",
    cache: "default", headers: {Accept: "application/json"}});
  if (!r.ok) throw new Error("HTTP_" + r.status);
  const declared = Number(r.headers?.get?.("content-length") || 0);
  if (declared > 180000) throw new Error("OVERSIZE");
  const txt = await r.text();
  if (txt.length > 180000) throw new Error("OVERSIZE");
  return JSON.parse(txt);
}

export async function readSources(fetchFn, now = Date.now()) {
  const [feed, gh] = await Promise.allSettled([
    boundedJSON(fetchFn, TICKER.publicFeed).then(x => parsePublicFeed(x, now)),
    boundedJSON(fetchFn, TICKER.githubAPI).then(x => parseGitHubCommits(x, now))
  ]);
  return {
    public: feed.status === "fulfilled" ? feed.value : null,
    github: gh.status === "fulfilled" ? gh.value : null,
    errors: [feed.status === "rejected", gh.status === "rejected"],
    checked_at_utc: new Date(now).toISOString()
  };
}

export function mountTicker(host, opts = {}) {
  if (!host || typeof host.attachShadow !== "function") {
    throw new Error("MISSING_TICKER_HOST");
  }
  const doc = host.ownerDocument;
  const win = doc.defaultView;
  const fetchFn = opts.fetch || win.fetch.bind(win);
  const shadow = host.shadowRoot || host.attachShadow({mode: "open"});
  const style = element(doc, "style", CSS);
  shadow.replaceChildren(style);
  let latest = null;
  let lastReadAt = 0;
  let disposed = false;
  let inFlight = false;

  function render(state) {
    const box = element(doc, "div", undefined, "nexus-ticker");
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "NEXUS OMEGA Status-Ticker");
    box.append(element(doc, "h2", "NEXUS OMEGA · Quellen-Ticker"));
    box.append(element(doc, "p",
      "C1_DESCRIPTIVE_ONLY · GitHub-Transport ist keine WWW-Freigabe oder Node-Liveness."));
    box.append(element(doc, "small", "Letzter Abruf: " +
      dateLabel(state.checked_at_utc) + " · Aktualisierung höchstens alle 15 Minuten."));
    renderSection(doc, box, "WWW-Ereignisregister (öffentliche Ableitung)",
      state.public, state.errors[0]);
    renderSection(doc, box, "GitHub-Main (atomare Commit-Belege, nur Transport)",
      state.github, state.errors[1]);
    const footer = element(doc, "p",
      "Kein Modellaufruf, kein Tracking-SDK, keine automatische Node-Ausführung. " +
      "Bei Quellenausfall bleibt der Status ausdrücklich unbekannt.");
    footer.className = "state";
    box.append(footer);
    // Replace the whole view only once after both independent reads finish.
    shadow.replaceChildren(style, box);
  }

  async function refresh(force = false) {
    if (disposed || inFlight) return;
    const now = Date.now();
    if (!force && now - lastReadAt < TICKER.pollMs) return;
    if (doc.visibilityState === "hidden" || (win.navigator && win.navigator.onLine === false)) return;
    lastReadAt = now;
    inFlight = true;
    try {
      latest = await readSources(fetchFn, now);
      if (!disposed) render(latest);
    } finally {
      inFlight = false;
    }
  }

  const initial = element(doc, "p", "Quellenstand wird geprüft …");
  shadow.append(initial);
  const interval = win.setInterval(() => { void refresh(); }, TICKER.pollMs);
  const onVisible = () => { if (doc.visibilityState === "visible") void refresh(); };
  doc.addEventListener("visibilitychange", onVisible);
  void refresh(true);
  return {
    refresh,
    getSnapshot: () => latest,
    dispose: () => {
      disposed = true;
      win.clearInterval(interval);
      doc.removeEventListener("visibilitychange", onVisible);
    }
  };
}

if (typeof document !== "undefined") {
  const boot = () => {
    const node = document.querySelector("[data-nexus-status-ticker]");
    if (node) mountTicker(node);
  };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, {once: true});
  } else {
    boot();
  }
}
