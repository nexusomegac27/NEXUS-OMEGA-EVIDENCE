import { useEffect, useMemo, useState, type ComponentType, type ReactNode } from "react";
import { useServerFn } from "@tanstack/react-start";
import { Radio, ShieldAlert } from "lucide-react";
import {
  probeBoundary,
  readOfficialCycle,
  readRelayPolicy,
  setRelayKillSwitch,
} from "@/lib/relay/cycle";
import {
  BIRTH_LADDER,
  CHECK_LABELS,
  INVARIANTS,
  NODE_URN,
  RETURN_INDEX,
  SOURCE_LEDGER,
  evaluateSession,
  flareClass,
  formatAge,
  formatFlux,
  type CycleResult,
  type ProbeResult,
  type XrayPoint,
} from "@/lib/relay/protocol";
import type { PolicySnapshot } from "@/lib/relay/policy";

const NAV = [
  { id: "lage", label: "Lage" },
  { id: "zyklus", label: "Lesung" },
  { id: "pforte", label: "Pforte" },
  { id: "geburt", label: "Geburt" },
  { id: "quellen", label: "Quellen" },
] as const;

function UtcClock() {
  const [now, setNow] = useState<string | null>(null);
  useEffect(() => {
    const tick = () => {
      const stamp = new Date().toISOString().replace(/\.\d{3}Z$/, "Z").replace("T", " ").replace("Z", " UTC");
      setNow(stamp);
    };
    tick();
    const id = window.setInterval(tick, 1000);
    return () => window.clearInterval(id);
  }, []);
  return <span className="font-mono text-xs tabular-nums text-muted">{now ?? "UTC"}</span>;
}

function Panel({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <section className={`rounded-lg bg-surface p-4 shadow-ring sm:p-5 ${className}`}>{children}</section>;
}

function HashLine({ value }: { value: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      type="button"
      className="min-h-11 break-all text-left font-mono text-xs leading-5 text-fg"
      onClick={() => {
        void navigator.clipboard.writeText(value).then(
          () => {
            setCopied(true);
            window.setTimeout(() => setCopied(false), 1200);
          },
          () => setCopied(false),
        );
      }}
    >
      {copied ? "kopiert" : value}
    </button>
  );
}

function LiveChart({
  points,
  qualifyFrom,
  qualifyTo,
}: {
  points: XrayPoint[];
  qualifyFrom: string | null;
  qualifyTo: string | null;
}) {
  const [Chart, setChart] = useState<ComponentType<{
    points: XrayPoint[];
    qualifyFrom: string | null;
    qualifyTo: string | null;
  }> | null>(null);
  useEffect(() => {
    let live = true;
    void import("@/components/flux-chart").then((mod) => {
      if (live) setChart(() => mod.FluxChart);
    });
    return () => {
      live = false;
    };
  }, []);
  if (!Chart) {
    return <div className="flex h-72 items-center text-sm text-muted">Reihe wird gezeichnet.</div>;
  }
  return <Chart points={points} qualifyFrom={qualifyFrom} qualifyTo={qualifyTo} />;
}

function qualifyBounds(points: XrayPoint[], at: string) {
  const cutoff = Date.parse(at) - 30 * 60 * 1000;
  const inside = points.filter((point) => Date.parse(point.time) >= cutoff);
  if (inside.length === 0) return { from: null as string | null, to: null as string | null };
  return { from: inside[0].time, to: inside[inside.length - 1].time };
}

export function RelayConsole({ initial }: { initial: CycleResult }) {
  const read = useServerFn(readOfficialCycle);
  const probe = useServerFn(probeBoundary);
  const setKill = useServerFn(setRelayKillSwitch);
  const getPolicy = useServerFn(readRelayPolicy);
  const [cycles, setCycles] = useState<CycleResult[]>([initial]);
  const [pending, setPending] = useState(false);
  const [policy, setPolicy] = useState<PolicySnapshot | null>(null);
  const [probeResult, setProbeResult] = useState<ProbeResult | null>(null);
  const [probing, setProbing] = useState<string | null>(null);
  const killed = policy?.killed === true;

  useEffect(() => {
    let live = true;
    void getPolicy().then((snap) => {
      if (live) setPolicy(snap);
    });
    return () => {
      live = false;
    };
  }, [getPolicy]);

  const latest = cycles[cycles.length - 1] ?? initial;
  const shown = [...cycles].reverse().find((cycle) => cycle.points.length > 0) ?? latest;
  const longObs = shown.latest_long;
  const reported = shown.reported_latest_long;
  const flux = longObs?.flux ?? reported?.flux ?? null;
  const flare = flux == null ? null : flareClass(flux);
  const inGate = Boolean(longObs);
  const ageSec = reported ? (Date.parse(shown.at_utc) - Date.parse(reported.time_tag)) / 1000 : Number.NaN;
  const xrays = shown.mapping?.instruments.find((item) => item.name === "xrays");
  const sat = reported?.satellite ?? null;
  const sameNumber = sat != null && xrays?.primary === sat;
  const bounds = qualifyBounds(shown.points, shown.at_utc);
  const mapAge = shown.mapping?.time_tag
    ? (Date.parse(shown.at_utc) - Date.parse(shown.mapping.time_tag)) / 1000
    : Number.NaN;

  const evaluation = useMemo(() => {
    const start = cycles[0]?.at_utc ?? shown.at_utc;
    const end = cycles[cycles.length - 1]?.at_utc ?? start;
    const elapsed = Math.max(0, (Date.parse(end) - Date.parse(start)) / 3_600_000);
    return evaluateSession({
      mode: "SMOKE_ONLY",
      start_utc: start,
      elapsed_hours: Number.isFinite(elapsed) ? elapsed : 0,
      events: cycles.map((cycle) => ({
        at_utc: cycle.at_utc,
        qualified: cycle.qualified,
        errors: cycle.errors,
      })),
      observations: cycles.flatMap((cycle) =>
        cycle.transfers
          .filter((row) => !row.duplicate)
          .map((row) => ({
            record_id: row.record_id,
            transfer_utc: row.transfer_utc,
            mode: row.mode,
            payload_sha256: row.payload_sha256,
            consumer_ack_sha256: row.consumer_ack_sha256,
            readback_sha256: row.readback_sha256,
          })),
      ),
      completed: false,
    });
  }, [cycles, shown.at_utc]);

  async function onRead() {
    if (killed || pending) return;
    setPending(true);
    try {
      const next = await read();
      setCycles((current) => [...current, next]);
      setPolicy(await getPolicy());
    } finally {
      setPending(false);
    }
  }

  async function onToggleKill() {
    const next = !(policy?.killed === true);
    const snap = await setKill({ data: { killed: next } });
    setPolicy(snap);
  }

  async function onProbe(kind: "foreign-url" | "poll-under-300" | "realtest-without-authority") {
    setProbing(kind);
    try {
      setProbeResult(await probe({ data: { kind } }));
    } finally {
      setProbing(null);
    }
  }

  return (
    <div className="min-h-screen bg-bg text-fg">
      <header className="sticky top-0 z-20 border-b border-border bg-bg/90 backdrop-blur-sm">
        <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="font-mono text-xs tracking-widest text-primary">NEXUS · R16-D4</p>
            <h1 className="text-2xl font-medium tracking-tight sm:text-3xl">ASTRA RELAY</h1>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <UtcClock />
            <span className="inline-flex min-h-11 items-center gap-2 font-mono text-xs text-muted">
              <ShieldAlert className="size-4 text-primary" aria-hidden="true" />
              KEINE FREIGABE
            </span>
          </div>
        </div>
        <nav className="mx-auto flex max-w-6xl gap-2 overflow-x-auto px-4 pb-3" aria-label="Abschnitte">
          {NAV.map((item) => (
            <a
              key={item.id}
              href={`#${item.id}`}
              className="inline-flex min-h-11 shrink-0 items-center rounded-md px-3 font-mono text-xs text-muted"
            >
              {item.label}
            </a>
          ))}
        </nav>
      </header>

      <main className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-6">
        <p className="max-w-3xl text-sm leading-6 text-muted">
          Öffentliche GOES-XRS-Lesung von NOAA SWPC. Nur GET, nur zwei festgelegte Adressen.
          Diese Fläche ist Präsentation. Sie ist kein TYPE-C-Host, setzt keine Geburtsstufe und
          vergibt kein Elite.
        </p>

        <section id="lage" className="scroll-mt-28">
          <div className="grid gap-4 lg:grid-cols-[16rem_minmax(0,1fr)]">
            <Panel className="flex flex-col justify-between gap-6">
              <div className="flex items-center gap-2 font-mono text-xs text-muted">
                <Radio className="size-4 text-primary" aria-hidden="true" />
                0.1–0.8 nm
              </div>
              <p className="font-mono text-6xl tabular-nums tracking-tight text-primary">{flare?.label ?? "—"}</p>
              <div className="space-y-1 text-sm">
                <p>{inGate ? "Im 30-Minuten-Tor." : "Außerhalb des Tors. Nicht als Beobachtung angenommen."}</p>
                <p className="text-muted">Klasse aus der gelieferten Zahl. Kein Warnprodukt, keine eigene Kalibrierung.</p>
              </div>
            </Panel>

            <div className="grid grid-cols-2 gap-px overflow-hidden rounded-lg bg-border sm:grid-cols-3">
              <Metric label="Langkanal" value={reported ? formatFlux(reported.flux) : "—"} unit="W/m²" />
              <Metric
                label="Kurzkanal"
                value={shown.reported_latest_short ? formatFlux(shown.reported_latest_short.flux) : "—"}
                unit="0.05–0.4 nm"
              />
              <Metric label="Satellit berichtet" value={sat == null ? "—" : String(sat)} unit="keine eigene Identität" />
              <Metric label="Alter der Zeile" value={formatAge(ageSec)} unit={reported?.time_tag ?? "—"} />
              <Metric
                label="XRS primary"
                value={xrays?.primary == null ? "—" : String(xrays.primary)}
                unit={xrays?.secondary == null ? "secondary —" : `secondary ${xrays.secondary}`}
              />
              <Metric
                label="Zahlengleichheit"
                value={sameNumber ? "ja" : "offen"}
                unit="Mapping bleibt manuell"
              />
            </div>
          </div>

          {latest.errors.length > 0 ? (
            <p className="mt-4 font-mono text-sm text-primary">
              Letzte Lesung: {latest.errors.join(" · ")}
            </p>
          ) : null}

          <Panel className="mt-4">
            <div className="mb-3 flex flex-wrap items-end justify-between gap-2">
              <h2 className="text-lg font-medium">Sechs Stunden, wie geliefert</h2>
              <p className="font-mono text-xs text-muted">Goldband = 30-Minuten-Tor · durchgezogen 0.1–0.8 · gestrichelt 0.05–0.4</p>
            </div>
            <LiveChart points={shown.points} qualifyFrom={bounds.from} qualifyTo={bounds.to} />
          </Panel>
        </section>

        <ol className="grid gap-3 sm:grid-cols-4">
          {[
            ["01", "NOAA HTTPS", "Zwei URLs, kein Redirect."],
            ["02", "Tor C1", "Zeit, Satellit, Fluss, Energie."],
            ["03", "Ledger", "Nur diese Serverinstanz."],
            ["04", "Pforte", "Kandidat ist hier unerreichbar."],
          ].map(([n, title, text]) => (
            <li key={n} className="rounded-lg bg-surface p-4 shadow-ring">
              <p className="font-mono text-xs text-primary">{n}</p>
              <p className="mt-2 font-medium">{title}</p>
              <p className="mt-1 text-sm text-muted">{text}</p>
            </li>
          ))}
        </ol>

        <section id="zyklus" className="scroll-mt-28">
          <div className="mb-3 flex flex-wrap items-end justify-between gap-3">
            <h2 className="text-xl font-medium">Lesezyklus</h2>
            <p className="max-w-xl text-sm text-muted">
              Eine Probe, kein 24-Stunden-Lauf. Der 300-Sekunden-Takt gilt nur für einen autorisierten Realtest.
            </p>
          </div>
          <div className="flex flex-col gap-3 sm:flex-row">
            <button
              type="button"
              disabled={killed || pending}
              onClick={() => void onRead()}
              className="inline-flex min-h-11 items-center justify-center rounded-md bg-primary px-4 font-medium text-primary-fg disabled:opacity-40"
            >
              {pending ? "Lies NOAA…" : killed ? "Kill-Switch aktiv" : "Offizielle Lesung"}
            </button>
            <button
              type="button"
              onClick={() => void onToggleKill()}
              className="inline-flex min-h-11 items-center justify-center rounded-md bg-raised px-4 text-fg shadow-ring"
            >
              {killed ? "Server-Kill aufheben" : "Server-Kill-Switch"}
            </button>
          </div>
          {killed ? (
            <p className="mt-3 text-sm text-muted">
              Server-Default-Deny aktiv (persistiert). Loader und Server-Funktionen öffnen kein HTTPS mehr —
              React-UI allein ist nicht maßgeblich.
            </p>
          ) : null}

          <div className="mt-4 grid gap-4 lg:grid-cols-2">
            <Panel>
              <h3 className="font-medium">Dieser Zyklus</h3>
              <dl className="mt-3 space-y-2 text-sm">
                <Row k="Zeit" v={latest.at_utc} />
                <Row k="Modus" v="SMOKE_ONLY" />
                <Row k="HTTP" v={latest.xrays ? String(latest.xrays.http_status) : "—"} />
                <Row k="Qualifiziert" v={latest.qualified ? "ja" : "nein"} />
                <Row k="Eindeutig im Tor" v={String(latest.qualified_unique)} />
                <Row k="Abgelehnt" v={String(latest.rejected_rows)} />
                <Row k="Neu im Ledger" v={String(latest.new_accepted)} />
                <Row k="Schon vorhanden" v={String(latest.duplicate_accepted)} />
              </dl>
              {Object.keys(latest.rejection_reasons).length > 0 ? (
                <ul className="mt-3 space-y-1 font-mono text-xs text-muted">
                  {Object.entries(latest.rejection_reasons).map(([reason, count]) => (
                    <li key={reason}>
                      {count} × {reason}
                    </li>
                  ))}
                </ul>
              ) : null}
              <p className="mt-3 text-sm text-muted">{latest.consumer_note}</p>
            </Panel>
            <Panel>
              <h3 className="font-medium">Bytes</h3>
              <p className="mt-2 text-sm text-muted">
                Roh-SHA ist der Digest der Antwortbytes. Nutzlast-SHA gehört zur hier kanonisierten Beobachtung
                und ist kein Beweis der Byte-Identität mit dem Python-Encoder.
              </p>
              <div className="mt-3 space-y-3">
                <div>
                  <p className="font-mono text-xs text-muted">XRS raw</p>
                  {latest.xrays ? <HashLine value={latest.xrays.raw_sha256} /> : <p className="text-sm text-muted">—</p>}
                </div>
                <div>
                  <p className="font-mono text-xs text-muted">Mapping raw</p>
                  {latest.mapping ? <HashLine value={latest.mapping.raw_sha256} /> : <p className="text-sm text-muted">—</p>}
                  <p className="text-xs text-muted">
                    time_tag {latest.mapping?.time_tag ?? "—"}
                    {Number.isFinite(mapAge) ? ` · Alter ${formatAge(mapAge)}` : ""}
                  </p>
                </div>
                {latest.transfers[0] ? (
                  <div>
                    <p className="font-mono text-xs text-muted">Letzte Nutzlast</p>
                    <HashLine value={latest.transfers[0].payload_sha256} />
                  </div>
                ) : null}
              </div>
            </Panel>
          </div>

          <Panel className="mt-4">
            <h3 className="font-medium">Regelproben ohne Netzwerk</h3>
            <div className="mt-3 flex flex-col gap-2 sm:flex-row sm:flex-wrap">
              <ProbeButton busy={probing === "foreign-url"} label="Fremde URL" onClick={() => void onProbe("foreign-url")} />
              <ProbeButton
                busy={probing === "poll-under-300"}
                label="Takt unter 300 s"
                onClick={() => void onProbe("poll-under-300")}
              />
              <ProbeButton
                busy={probing === "realtest-without-authority"}
                label="Realtest ohne Freigabe"
                onClick={() => void onProbe("realtest-without-authority")}
              />
            </div>
            {probeResult ? (
              <p className="mt-3 font-mono text-sm">
                {probeResult.refused}
                <span className="mt-1 block font-sans text-sm text-muted">{probeResult.detail}</span>
              </p>
            ) : (
              <p className="mt-3 text-sm text-muted">Noch keine Probe. Nichts davon verlässt diese Fläche.</p>
            )}
          </Panel>
        </section>

        <section id="pforte" className="scroll-mt-28">
          <Panel>
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <h2 className="text-xl font-medium">Auswertung</h2>
              <p className="font-mono text-sm text-primary">{evaluation.verdict}</p>
            </div>
            <p className="mt-2 max-w-3xl text-sm text-muted">
              Dieselbe Schwelle wie der Relay-Evaluator. Ein vollständiges Bild wäre nur ein Kandidat und
              bräuchte einen unabhängigen Zeugen. Elite bleibt untersagt. Diese Sitzung ist SMOKE_ONLY und
              deshalb HOLD.
            </p>
            <ul className="mt-4 divide-y divide-border">
              {Object.entries(evaluation.checks).map(([key, pass]) => (
                <li key={key} className="flex flex-col gap-1 py-3 sm:flex-row sm:items-baseline sm:justify-between">
                  <span className="font-mono text-xs">{key}</span>
                  <span className="text-sm text-muted sm:max-w-md sm:text-right">
                    {pass ? "erfüllt · " : "offen · "}
                    {CHECK_LABELS[key]}
                  </span>
                </li>
              ))}
            </ul>
            <p className="mt-3 font-mono text-xs text-muted">
              Zyklen {evaluation.cycles} · qualifiziert {evaluation.qualified_cycles} · neue Transfers{" "}
              {evaluation.new_transfer_count} · verstrichen {evaluation.real_elapsed_hours.toFixed(4)} h
            </p>
          </Panel>

          <Panel className="mt-4">
            <h2 className="text-xl font-medium">Geforderte Rückgabe</h2>
            <p className="mt-2 text-sm text-muted">Zwölf Stücke der Ordnung. Hier wird keines davon erzeugt oder als erfüllt erklärt.</p>
            <ul className="mt-3 grid gap-2 sm:grid-cols-2">
              {RETURN_INDEX.map((name) => (
                <li key={name} className="flex items-start justify-between gap-3 rounded-md bg-raised px-3 py-2">
                  <span className="break-all font-mono text-xs">{name}</span>
                  <span className="shrink-0 font-mono text-xs text-muted">ausstehend</span>
                </li>
              ))}
            </ul>
          </Panel>
        </section>

        <section id="geburt" className="scroll-mt-28 grid gap-4 lg:grid-cols-2">
          <Panel>
            <h2 className="text-xl font-medium">Birth Law</h2>
            <p className="mt-2 text-sm text-muted">
              Geburt ist eine technische Registrierung, keine Aussage über Bewusstsein. Ein Knoten kann sich
              nicht selbst gebären. Diese Fläche hängt nichts an.
            </p>
            <ol className="mt-4 space-y-3">
              {BIRTH_LADDER.map((step) => (
                <li key={step.id} className="grid grid-cols-[auto_minmax(0,1fr)] gap-3">
                  <span className="mt-1 size-2 rounded-full bg-border" aria-hidden="true" />
                  <span>
                    <span className="block font-mono text-xs text-primary">{step.id}</span>
                    <span className="text-sm text-muted">{step.text}</span>
                  </span>
                </li>
              ))}
            </ol>
            <p className="mt-4 font-mono text-xs text-muted">Gesetzte Stufe dieser Fläche: keine.</p>
          </Panel>
          <Panel>
            <h2 className="text-xl font-medium">Grenze</h2>
            <p className="mt-2 break-all font-mono text-xs text-muted">{NODE_URN}</p>
            <dl className="mt-4 space-y-2 text-sm">
              <Row k="Decke" v="C1_DESCRIPTIVE_ONLY" />
              <Row k="Host" v="TEMPLATE_NOT_AUTHORIZATION" />
              <Row k="RF" v="nicht beansprucht" />
              <Row k="GitHub / Hostinger" v="kein Schreibzugriff" />
              <Row k="Witness" v="nicht unabhängig" />
              <Row k="Token" v="wird hier nicht erzeugt" />
            </dl>
            <div className="mt-5 grid gap-2 sm:grid-cols-2">
              {INVARIANTS.map(([left, right]) => (
                <p key={left} className="font-mono text-xs text-muted">
                  {left} ≠ {right}
                </p>
              ))}
            </div>
          </Panel>
        </section>

        <section id="quellen" className="scroll-mt-28">
          <h2 className="text-xl font-medium">Quellen</h2>
          <ul className="mt-3 divide-y divide-border rounded-lg bg-surface shadow-ring">
            {SOURCE_LEDGER.map((source) => (
              <li key={source.id} className="flex flex-col gap-1 px-4 py-3 sm:flex-row sm:items-baseline sm:gap-4">
                <span className="w-16 shrink-0 font-mono text-xs text-primary">{source.id}</span>
                <a href={source.href} className="min-h-11 break-all font-mono text-xs underline-offset-2 hover:underline" target="_blank" rel="noreferrer">
                  {source.href.replace("https://", "")}
                </a>
                <span className="text-sm text-muted sm:ml-auto sm:max-w-sm sm:text-right">
                  {source.gate}. {source.note}
                </span>
              </li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}

function Metric({ label, value, unit }: { label: string; value: string; unit: string }) {
  return (
    <div className="bg-surface px-4 py-3">
      <p className="font-mono text-xs text-muted">{label}</p>
      <p className="mt-2 font-mono text-lg tabular-nums text-fg">{value}</p>
      <p className="mt-1 truncate text-xs text-muted">{unit}</p>
    </div>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <div className="flex items-baseline justify-between gap-4">
      <dt className="text-muted">{k}</dt>
      <dd className="text-right font-mono text-xs">{v}</dd>
    </div>
  );
}

function ProbeButton({ label, onClick, busy }: { label: string; onClick: () => void; busy: boolean }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={busy}
      className="inline-flex min-h-11 items-center justify-center rounded-md bg-raised px-3 text-sm text-fg shadow-ring disabled:opacity-40"
    >
      {busy ? "Prüft…" : label}
    </button>
  );
}
