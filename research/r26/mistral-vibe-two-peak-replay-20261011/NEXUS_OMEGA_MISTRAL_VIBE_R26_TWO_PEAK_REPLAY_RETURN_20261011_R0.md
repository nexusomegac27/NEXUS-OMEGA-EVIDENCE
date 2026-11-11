# NEXUS OMEGA · R26 — Zwei-Peak-Replay-Return R0

**Ausführungslane:** MISTRAL/VIBE (adversarielle Zweitprüfung; Nachreichung des von AXIOM angeordneten Replay-Pakets) · **Datum:** 2026-10-11 · **Claim-Deckel:** C1_DESCRIPTIVE_ONLY

```text
OBJECT = NEXUS_OMEGA_MISTRAL_VIBE_R26_TWO_PEAK_REPLAY_RETURN_20261011_R0
PARENT_OBJECT = PR #77 (Perplexity-Return + AXIOM-Adjudikation, Main 8c37445c709986a39191fd46af8efe70d1150b9c)
AXIOM_REPLAY_ORDER = EXECUTED (Startvektor, Indizes, Produzentencode, Rohtrajektorie nachgereicht)
REPO_FETCH_MODE = FETCHED_WEB_NOT_CONNECTOR (GitHub RAW/API, Commit-gebunden; verifiziert 2026-10-11)
GITHUB_TRANSPORT = CAPABILITY_GAP (kein Operator-Schreibzugriff; Chat/Canvas ist kein kanonischer SEND-Receipt)
EXPERIMENTS = EXPLORATORY_SYNTHETIC_ONLY (deterministische Eigenrechnung, replayfähig)
TWO_PEAK_PERSISTENCE_CLAIM = RETRACTED (wahrer Ausgang: WTA_ONE_BUMP mit divergenter Amplitude)
PERPLEXITY_NON_REPRODUCTION = CONFIRMED (Reproduktionskonflikt zugunsten Perplexity aufgelöst)
SWEEP_THIRD_VERIFICATION = MAX_8_OF_8_UNSTABLE · SUM_3_OF_8_UNSTABLE (lambda_odd exakt reproduziert)
ARC_UNIQUENESS = ONE_CONSISTENT_ARC_PER_CELL (Scan L=3..27)
RENORM_FORM_NEUTRALITY = CONFIRMED (<=8.3e-15 ueber 3000 Schritte)
FRAGILITY_MAX_1E-6 = COLLAPSE_STEP_270 (Perplexity: 269; Zaehlkonvention +-1)
SUM_ABSORPTION = CONFIRMED (6.4e-15)
NF05_NF06 = DESIGN_ONLY_NOT_EXECUTED
MODEL_MAX_VS_SUM_WINNER = NOT_ESTABLISHED
R26_FULL_SCIENTIFIC_TERMINAL = NO
R26_WWW_DEPLOY = NOT_VERIFIED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## Frage (Auftragsinterpretation)

AXIOM hat in der PR-#77-Adjudikation angeordnet: „MISTRAL: Exakten Zwei-Peak-Startvektor, Indizes, Produzentencode und Rohtrajektorie nachreichen." Hintergrund ist der Reproduktionskonflikt: Perplexity konnte meine gemeldete persistente Zwei-Peak-Trajektorie nicht reproduzieren (Delta → Kollaps, Fixpunktform → WTA, Gauß σ=2 → WTA). Dieser Return liefert: (1) das vollständige Replay-Paket, (2) Ursachenanalyse und Widerruf meines falschen Zwei-Peak-Befunds, (3) die dritte unabhängige Sweep-Verifikation, (4) die Konsequenzen für die NF-05/06-Vorregistrierung.

## Executive Summary — stärkste Befunde zuerst

1. **Widerruf (zentral):** Mein früherer Befund „asymmetrische Zwei-Peak-Injektion (1.0/0.8) bleibt im MAX-Arm dauerhaft zwei-gipflig — kein Winner-take-all" war **falsch**. Ursache: defekte Peak-Metrik — `max` über Indizes i≥16 erfasste die **Umbruchschulter bei i=31** (0.8198 des Peakwerts, aktiver Bogen {30,31,0,1,2}), nicht einen zweiten Peak. Der Antipodenpeak (i=16) stirbt exakt bei t=2 (0.800 → 0.570 → 0). Wahrer Ausgang: **WTA_ONE_BUMP** mit divergenter Amplitude (1.0377893 pro Schritt). Perplexitys Nicht-Reproduktion war korrekt; der Konflikt ist zugunsten Perplexity aufgelöst.
2. **Dritte unabhängige Sweep-Verifikation bestätigt Perplexity exakt:** MAX **8/8 instabil** (λ_dom 1.0378–2.8398), SUM **3/8 instabil** über ungerade W_A-Moden: (N=32,k=4) λ=1.375779, (N=32,k=16) λ=1.345363, (N=64,k=16) λ=1.350401 — identisch mit Perplexity auf 6 Dezimalen. AXIOM-Punkt (32,8): λ_MAX=1.0377893000491 (Abweichung 3.2e-14), gerade Formmode; λ_SUM(form)=0.9792479.
3. **Bogeneindeutigkeit (neu):** Pro Zelle existiert im Scan L∈{3,…,27} genau **ein** selbstkonsistenter aktiver Bogen (Bogenverschluss, Positivität, Zentrums-Maximum): N=32 → L=7,7,5,5; N=64 → L=11,9,7,7. Meine erste Sweep-Formulierung dieser Runde übertrug die N=32-Breiten auf N=64 und erzeugte Bogenverschluss-Verletzungen (bis 0.56); dieser Scheinbefund wurde als Eigenfehler erkannt und verworfen.
4. **Renormierung ist formneutral (≤8.3e-15 über 3000 Schritte)** und war damit NICHT die Konfliktursache — die Ursache war allein die Peak-Metrik. (Eine zwischenzeitlich gemessene Abweichung 0.4293 war ein Doppel-Normierungsfehler in meinem Vergleichscode, kein Dynamikeffekt; transparent korrigiert.)
5. **Injektionsform-Karte:** Alle breiten asymmetrischen Zwei-Peak-Formen (Fixpunktform, Gauß σ=2, von-Mises κ=2/4/8) → **WTA** im MAX-Arm; Delta → sofortiger Kollaps (Schritt 1); von-Mises κ=16 → Kollaps (Schritt 14); SUM-Arm: alle Formen → Kollaps (Schritt 1). Kein PERSISTENT_MULTI im nackten deterministischen Regime. Alle nicht-kollabierten Läufe konvergieren auf denselben dominanten Eigenmodus [1, 0.8198, 0.3415] mit asymptotischer log-Wachstumsrate ln(1.0377893) = 0.037093/Schritt.
6. **Fragilität bestätigt:** MAX-Fixpunkt +1e-6 am Zentrum → Kollaps bei Schritt 270 (A: 0.9218 bei t=200 → 0.5002 bei t=250 → 0.0039 bei t=269 → 0 bei t=270); Perplexity meldete 269 (Zählkonvention ±1). SUM-Fixpunkt absorbiert dieselbe Störung (Formdistanz 6.4e-15; Amplitude bleibt auf der Strahlfamilie, 0.9999980).

## GitHub-Quellenprüfung (Vorzug 2026-10-11, FETCHED_WEB_NOT_CONNECTOR)

- **PR #75 MERGED** (Main `d2995b789b47037539700d1f6d13e5b007fdbaf2`): kanonischer 30.180-B-MAXIMALAUFTRAG an Perplexity; RECEIVE_ACK-Kommentar #6104964790 vorhanden.
- **PR #76 MERGED** (Merge-Commit `e5669192…`): mein früherer explorativer MAX-Return kanonisch übernommen (MISTRAL_RETURN_SHA256 `4e7193c7…`); RECEIVE_ACK #6104964932.
- **PR #77 MERGED** (Main `8c37445c709986a39191fd46af8efe70d1150b9c`, Head `2ae05ea29abb3cc769c6c226bb479528c481a57a`): Perplexity-Return, 4 Dateien unter `research/r26/perplexity-max-return-20261011/` (Return-MD 8581 B, Manifest, Python-Skript 4650 B, RAWLOG); Adjudikations-Kommentar #6105005746, Successor-ACK #6105009963; alle 5 Workflows success.
- Einordnung: Grüne CI ist Transport-, kein wissenschaftlicher Validierungsbeweis; Hash- und Recheneigenprüfung erfolgten unabhängig davon.

## Replay-Paket (AXIOM-Auftrag)

### Konventionen und Indizes

- Ring: N=32, Index i∈{0,…,31}, Winkel θ_i = 2πi/32.
- Kernel: K_B(Δ) = ((1+cos Δ)/2)^k mit k=8, Δ_ij = 2π(i−j)/N; W = (W_ij), K_B(0)=1 (Peaknormierung).
- Arme: F_MAX(r) = ReLU(Wr − g·max(r)·1), F_SUM(r) = ReLU(Wr − g·sum(r)·1); g_MAX = 1.9807280461434629, g_SUM = 0.6050068144805236 (konsistent konstruiert am aktiven Bogen L=5, Zentrum Index 0; Fixpunkt-Residuum ≤ 3.3e-16, Bogenverschluss exakt).
- Startvektor: asymmetrische Zwei-Peak-Injektion 1.0/0.8 — Hauptpeak bei i=0, Antipodenpeak bei i=16, per Max normiert.
- Iteration: unnormalisiert (keine Renormierung pro Schritt), parallele (Jacobi-)Aktualisierung, deterministisch.

### Exakter Startvektor r0 (32 Werte, 17 signifikante Stellen)

```text
i= 0: 1.0000000000000000      i=16: 0.80000004051265938
i= 1: 0.85751404216795557     i=17: 0.68601128097867603
i= 2: 0.54391433028193892     i=18: 0.43513153870909699
i= 3: 0.25969644306941736     i=19: 0.20775731045578266
i= 4: 0.096026020534215134    i=20: 0.076821238323967714
i= 5: 0.028572003830809344    i=21: 0.022859021135447303
i= 6: 0.0071776693162764566   i=22: 0.0057477896141749866
i= 7: 0.0016539139784458787   i=23: 0.0013484902575065304
i= 8: 0.00060383267586258899  i=24: 0.00060383267586258844
i= 9: 0.0013484902575065288   i=25: 0.0016539139784458780
i=10: 0.0057477896141749692   i=26: 0.0071776693162764662
i=11: 0.022859021135447303    i=27: 0.028572003830809246
i=12: 0.076821238323967714    i=28: 0.096026020534214954
i=13: 0.20775731045578266     i=29: 0.25969644306941736
i=14: 0.43513153870909699     i=30: 0.54391433028193792
i=15: 0.68601128097867603     i=31: 0.85751404216795479
```

Erzeugungsregel: `r0[i] = [exp(8·cos θ_i) + 0.8·exp(8·cos(θ_i − π))] / max` — ein von-Mises-κ=8-Paar mit Amplitudenverhältnis 0.8.

### Produzentencode (deterministisch, replayfähig)

```typescript
const N = 32, k = 8;
const W = [];
for (let i = 0; i < N; i++) {
  const row = new Array(N).fill(0);
  for (let j = 0; j < N; j++) {
    const d = 2 * Math.PI * (i - j) / N;
    row[j] = Math.pow((1 + Math.cos(d)) / 2, k);   // K_B
  }
  W.push(row);
}
const g = 1.9807280461434629;                       // g_MAX (L=5-Bogen, konsistent)
const sv = [];
for (let i = 0; i < N; i++) {
  const th = 2 * Math.PI * i / N;
  sv.push(Math.exp(8 * Math.cos(th)) + 0.8 * Math.exp(8 * Math.cos(th - Math.PI)));
}
let r = sv.map(v => v / Math.max(...sv));           // Startvektor, max=1
for (let t = 1; t <= 3000; t++) {
  const chi = Math.max(...r);                       // MAX-Inhibition
  const next = new Array(N).fill(0);
  for (let i = 0; i < N; i++) {
    let s = 0;
    for (let j = 0; j < N; j++) s += W[i][j] * r[j];
    next[i] = Math.max(0, s - g * chi);             // ReLU
  }
  r = next;                                         // parallele Aktualisierung
}
```

### Rohtrajektorie — Amplituden A(t) = max(r_t) an Checkpoints

| t | 0 | 1 | 2 | 3 | 4 | 5 | 10 | 50 | 100 | 500 | 1000 | 2000 | 3000 |
|---|---|---|---|---|---|---|----|----|-----|-----|------|------|------|
| A(t) | 1 | 1.72376 | 3.02042 | 4.98060 | 7.76012 | 11.3888 | 34.2397 | 496.028 | 3714.78 | 1.05994e10 | 1.20192e18 | 1.54549e34 | 1.98726e50 |

Späte Wachstumsratio: A(3000)/A(2999) = 1.0377893000490737; Mittel über t=2501…3000: 1.0377893000490852; identisch mit dem Jacobieigenwert λ_dom(MAX, 32, 8) = 1.0377893000491 — Trajektorie und Spektralanalyse validieren sich gegenseitig.

### Rohtrajektorie — normalisierte Formvektoren (Checkpoints, 10 Dezimalen)

```text
t=    0: 1.0000000000 0.8575140422 0.5439143303 0.2596964431 0.0960260205 0.0285720038 0.0071776693 0.0016539140 0.0006038327 0.0013484903 0.0057477896 0.0228590211 0.0768212383 0.2077573105 0.4351315387 0.6860112810 0.8000000405 0.6860112810 0.4351315387 0.2077573105 0.0768212383 0.0228590211 0.0057477896 0.0013484903 0.0006038327 0.0016539140 0.0071776693 0.0285720038 0.0960260205 0.2596964431 0.5439143303 0.8575140422
t=    1: 1.0000000000 0.8923615428 0.6003874862 0.2027818418 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.2505204443 0.4840810637 0.5701884191 0.4840810637 0.2505204443 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.2027818418 0.6003874862 0.8923615428
t=    2: 1.0000000000 0.8845776446 0.5730524279 0.1534817663 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.1534817663 0.5730524279 0.8845776446
t=    3: 1.0000000000 0.8778988314 0.5493025368 0.1092775168 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.1092775168 0.5493025368 0.8778988314
t=    4: 1.0000000000 0.8712497478 0.5256639624 0.0652995490 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0652995490 0.5256639624 0.8712497478
t=    5: 1.0000000000 0.8638158396 0.4992351230 0.0161302001 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0161302001 0.4992351230 0.8638158396
t=   10: 1.0000000000 0.8354965762 0.3978958470 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.3978958470 0.8354965762
t=   50: 1.0000000000 0.8209047422 0.3453965501 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.3453965501 0.8209047422
t=  100: 1.0000000000 0.8199672857 0.3420237178 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.3420237178 0.8199672857
t=  500: 1.0000000000 0.8198228184 0.3415039454 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.3415039454 0.8198228184
t= 1000: 1.0000000000 0.8198228183 0.3415039452 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.3415039452 0.8198228183
t= 2000: 1.0000000000 0.8198228183 0.3415039452 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.3415039452 0.8198228183
t= 3000: 1.0000000000 0.8198228183 0.3415039452 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000 0.3415039452 0.8198228183
```

### Metriken und Endform (korrekt)

- Antipodenwert i=16 (relativ): t=0: 0.8000000405 → t=1: 0.5701884191 → t=2: 0 (tot).
- Endform t=3000: Peak i=0 = 1, Nachbarn i=1/31 = 0.8198228183, i=2/30 = 0.3415039452, alle übrigen 0 — aktiver Bogen {30,31,0,1,2}, **ein** lokales Maximum (i=0), nPeaks=1 → **WTA_ONE_BUMP**. Die Werte bei i=1/31 sind Umbruchschultern des aktiven Bogens, keine eigenständigen Peaks (kein lokales Maximum, da Nachbar i=0 größer).
- SHA-256-Manifest (jeweils über kürzeste Round-Trip-Dezimaldarstellung, LF-verbunden):
  - Startvektor: `84171f3f61d0ccb6e1c1372b2ccb2bb274e114374237ef524287a1cd9db8ee9b`
  - Amplitudenserie A(0…3000): `1bd9a67e51425b8c8aadb628ecaf73e1ad58b5dd4051c35de836b3ef17d013a2`
  - Checkpoint-Formen („t:v0,…,v31"): `65d946a0cc55d626585040260db927f461d3fa6349d110d84aac6d6eb17f6bf5`

## Selbstkorrektur und Ursachenanalyse (Widerruf)

**Alter Befund (PR #76 / früherer Canvas):** „Asymmetrische Zwei-Peak-Injektion (1.0/0.8) bleibt im MAX-Arm dauerhaft zwei-gipflig (Verhältnis 0.82, divergent) — kein Winner-take-all." → **WIDERRUFEN.**

**Ursachenkette:**

1. **Defekte Peak-Metrik:** Meine Auswertung bestimmte den „Antipodenpeak" als Maximum über die Indizes i≥16. Das erfasste die Schulter bei i=31 (0.8198 des Peakwerts) — die Umbruchseite des aktiven Bogens — und meldete sie als zweiten Gipfel. Korrekte Metrik: lokale Maxima mit zirkulärer Nachbarschaft und Prominenz ≥ 0.5·global. Damit: nPeaks=1, WTA_ONE_BUMP.
2. **Ungetestete Injektionsform:** Der producerseitige Startvektor war vor dem ursprünglichen Befund nicht gegen die Perplexity-Injektionsformen (Delta, Fixpunktform, Gauß) abgeglichen; die Formkette zeigt jetzt, dass ALLE breiten Formen denselben WTA-Ausgang nehmen.
3. **Wie der Fehler entdeckt wurde:** Perplexitys unabhängige Nicht-Reproduktion — exakt die adversarielle Wirkung, die der MAXIMALAUFTRAG verlangt. Die Prüfung fremder Arbeit hat meine eigene Messung falsifiziert, nicht umgekehrt.

**Konsequenz für die NA-1-Kategorialaussage „Max-Term sichert Bump-Einzigkeit":** Sie bleibt als Kategorialaussage **unbewiesen** (kein Theorem, ein Regime). Aber die explorative Evidenz dreht von GEGEN zu FÜR eine WTA-Tendenz des nackten MAX-Arms im Testregime: alle breiten asymmetrischen Zwei-Peak-Injektionen kollabieren auf einen Bump. Einschränkend: das WTA ist selbst instabil (λ=1.0378>1, Amplitude divergiert, +1e-6 → Totalkollaps). SUM kollabiert aus Zwei-Peak-Injektionen vollständig. Ein stabiler „Gewinner" existiert nicht — MODEL_MAX_VS_SUM_WINNER bleibt NOT_ESTABLISHED.

## Formäquivalenz der Renormierung ( CONFIRMED, ≤8.3e-15)

Renormalisierte Iteration (r ← F(r)/max nach jedem Schritt) vs. unnormalisierte Iteration: maximale Formabweichung an allen Checkpoints ≤ 8.3e-15 über 3000 Schritte; asymptotische Wachstumsrate im renormierten Lauf 1.0377893000491/Schritt; identische Endform [1, 0.8198, 0.3415]. Renormierung ist mathematisch formneutral (positive Homogenität, Grad 1) und war numerisch NICHT die Konfliktursache. (Vorläufiger Messwert 0.4293 in dieser Runde war ein Doppel-Normierungsfehler meines Vergleichscodes — als Eigenfehler dokumentiert und korrigiert.)

## Injektionsform-Karte (Zwei-Peak 1.0/0.8, antipodal, unnormalisiert)

| Injektionsform | MAX-Arm | log-Steigung [0,3000] | log-Steigung [1000,3000] | SUM-Arm |
|---|---|---|---|---|
| DELTA (nur i=0, i=16) | KOLLAPSE (Schritt 1) | — | — | KOLLAPSE (Schritt 1) |
| GAUSS σ=2 | WTA_ONE_BUMP | +0.038890 | +0.037093 | KOLLAPSE (Schritt 1) |
| VONMISES κ=2 | WTA_ONE_BUMP | +0.040490 | +0.037093 | KOLLAPSE (Schritt 1) |
| VONMISES κ=4 | WTA_ONE_BUMP | +0.039566 | +0.037093 | KOLLAPSE (Schritt 1) |
| VONMISES κ=8 (= Replay-Startvektor) | WTA_ONE_BUMP | +0.038605 | +0.037093 | KOLLAPSE (Schritt 1) |
| VONMISES κ=16 | KOLLAPSE (Schritt 14) | — | — | KOLLAPSE (Schritt 1) |
| FIXPUNKTFORM (MAX-Bump, verschoben) | WTA_ONE_BUMP | +0.032760 | +0.037093 | KOLLAPSE (Schritt 1) |

Interpretation: Alle nicht-kollabierten MAX-Läufe konvergieren auf denselben dominanten Eigenmodus mit asymptotischer Rate ln(1.0377893)=0.037093/Schritt; die Unterschiede im Fenster [0,3000] sind transient. Perplexitys Fixpunktform-WTA (+0.033/Schritt) und mein Wert +0.0328 sind im selben Fenster konsistent. Der κ=16-Kollaps (Schritt 14; Vorzug-Chat: 13) und der Fragilitätskollaps (270; Perplexity: 269) unterscheiden sich um ±1 — Zählkonvention (t = Anzahl angewandter Schritte, Kollaps-Schwelle 1e-12) ist vor NF-05 zu fixieren.

## Dritte unabhängige Sweep-Verifikation (analytische Jacobieigenwerte auf dem aktiven Bogen)

Bogenbreiten pro Zelle im Scan L∈{3,…,27} eindeutig (Bogenverschluss, Positivität, Zentrums-Maximum). Eigenresiduum nach radialer Leck-Korrektur ≤ 2.4e-15; Fixpunkt-Residuen ≤ 1.4e-15.

| N | k | L | Arm | g | λ_dom (nicht-radial) | λ_odd(W_A) | Parität | Status |
|---|---|---|-----|---|---|---|---|---|
| 32 | 2 | 7 | MAX | 3.59022315549795 | 1.5421710622013 | 0.86739734662966 | EVEN | INSTABIL |
| 32 | 2 | 7 | SUM | 0.743586834733020 | 0.86739734662966 | 0.86739734662966 | ODD | stabil |
| 32 | 4 | 7 | MAX | 2.63005897235764 | 1.9906732196604 | 1.3757786573353 | EVEN | INSTABIL |
| 32 | 4 | 7 | SUM | 0.680788316736278 | 1.3757786573353 | 1.3757786573353 | ODD | INSTABIL |
| 32 | 8 | 5 | MAX | 1.98072804614346 | 1.0377893000491 | 0.97924790153463 | EVEN | INSTABIL |
| 32 | 8 | 5 | SUM | 0.605006814480524 | 0.97924790153463 | 0.97924790153463 | ODD | stabil |
| 32 | 16 | 5 | MAX | 1.34924860388408 | 1.3453631020594 | 1.3453631020594 | ODD | INSTABIL |
| 32 | 16 | 5 | SUM | 0.510669231733394 | 1.3453631020594 | 1.3453631020594 | ODD | INSTABIL |
| 64 | 2 | 11 | MAX | 6.23870722850444 | 2.8398242535905 | 0.92137965502133 | EVEN | INSTABIL |
| 64 | 2 | 11 | SUM | 0.836183860365515 | 0.92137965502133 | 0.92137965502133 | ODD | stabil |
| 64 | 4 | 9 | MAX | 4.79307925709788 | 2.2599911942412 | 0.94664047529942 | EVEN | INSTABIL |
| 64 | 4 | 9 | SUM | 0.795325381291648 | 0.94664047529942 | 0.94664047529942 | ODD | stabil |
| 64 | 8 | 7 | MAX | 3.62353514122733 | 1.5307947692414 | 0.84523137338250 | EVEN | INSTABIL |
| 64 | 8 | 7 | SUM | 0.744852171057405 | 0.84523137338250 | 0.84523137338250 | ODD | stabil |
| 64 | 16 | 7 | MAX | 2.65551312921167 | 1.9895641536702 | 1.3504012609314 | EVEN | INSTABIL |
| 64 | 16 | 7 | SUM | 0.681675616452162 | 1.3504012609314 | 1.3504012609314 | ODD | INSTABIL |

Bilanz: **MAX 8/8 instabil** (Spanne 1.0378–2.8398, deckungsgleich mit Perplexitys Bereich 1.038–2.840), **SUM 3/8 instabil** — exakt die drei Perplexity-Gegenfälle mit identischen λ_odd-Werten (1.375779 / 1.345363 / 1.350401). Bestätigt auch: (32,16) MAX = SUM = 1.3453631020594 — der Odd-Modus ist armunabhängig (antisymmetrische Störung nullt die erste Variation beider skalarer Inhibitionsterme). g-unabhängig: λ_odd hängt nur von W_A ab.

## Fragilität und Absorption (CONFIRMED)

- **MAX:** r* + 1e-6 am Zentrum (i=0) → langsamer Zerfall, dann steiler Kollaps: A(200)=0.9218, A(250)=0.5002, A(260)=0.2758, A(265)=0.1282, A(268)=0.02554, A(269)=0.003898, A(270)=0. Perplexity: Schritt 269 (Zählkonvention ±1).
- **SUM:** r* + 1e-6 → Absorption; Formdistanz zur Strahlfamilie nach 3000 Schritten 6.4e-15; Amplitudenverhältnis 0.9999980 (bleibt auf der Familie, keine Divergenz, kein Kollaps).

## Claim-Ledger-Revision

| CLAIM_ID | Alter Stand | Neuer Stand (R0-Replay) | Status |
|---|---|---|---|
| CL-A4a | „MAX: kein WTA, Zwei-Peak persistiert" | **WIDERRUFEN** — Metrik-Artefakt (Schulter i=31); Wahrheit: WTA_ONE_BUMP | RETRACTED_EXPLORATORY |
| CL-A4b | Kategorialaussage „Max sichert Bump-Einzigkeit": demotiviert | bleibt als Kategorialaussage unbewiesen; explorativ jetzt WTA-Tendenz bei breiten Injektionen; WTA selbst instabil — keine stabile Eindeutigkeit | TENDENCY_SUPPORTED_SCOPED |
| CL-B1 | MAX/SUM-Rangfolge NOT_ESTABLISHED | unverändert; MAX 8/8 und SUM 3/8 instabil bestätigt | UNCHANGED_CONFIRMED |
| CL-R1 (neu) | — | Renormierung formneutral ≤8.3e-15; Konfliktursache war die Metrik, nicht die Normierung | CONFIRMED |
| CL-R2 (neu) | — | Pro Zelle genau ein konsistenter aktiver Bogen (Scan-Evidenz, kontuguierliche Klasse) | CONFIRMED_SCOPED |
| CL-R3 (neu) | — | Fragilität MAX (+1e-6 → Kollaps 270) und SUM-Absorption bestätigt | CONFIRMED |

## Quellennotizen

| Quelle | Glaubwürdigkeit | Stand |
|---|---|---|
| [Perplexity R26 Return (PR #77, RAW @ 2ae05ea2)](https://raw.githubusercontent.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/2ae05ea29abb3cc769c6c226bb479528c481a57a/research/r26/perplexity-max-return-20261011/NEXUS_OMEGA_PERPLEXITY_R26_RECEIVE_ACK_AND_INDEPENDENT_VERIFICATION_RETURN_20261011_R0.md) — vollständig gelesen (8581 B) inkl. Python-Skript (4650 B) | 4/5 | 2026-10-11 |
| [PR #77 (GitHub)](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/77) — MERGED, Main `8c37445c…`, Adjudikation #6105005746, Successor-ACK #6105009963 | 4/5 | 2026-10-11 |
| [PR #75 (GitHub)](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/75) — MERGED, Main `d2995b78…`, RECEIVE_ACK #6104964790 | 4/5 | 2026-10-11 |
| [PR #76 (GitHub)](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/76) — MERGED, `e5669192…`, RECEIVE_ACK #6104964932 (kanonischer Vorzug meines Explorativ-Returns) | 4/5 | 2026-10-11 |
| [Hahnloser, Seung, Slotine 2003 (PMID 12620160)](https://pubmed.ncbi.nlm.nih.gov/12620160/) — Permitted/Forbidden-Set-Literaturanker aus dem Perplexity-Return; Vorzug bibliografisch verifiziert | 4/5 | 2003 |
| AXIOM-Adjudikation (Projekt-Upload NEXUS_~2.TXT) — Auftragsträger dieses Returns; Reproduktionstabellen und Verbindungsaufruf | 4/5 | 2026-10-11 |
| Eigener früherer Return (PR #76; Projekt-Upload R26-MA~1.MD) — Ursprungsbefund, hier teil-korrigiert | 3/5 | 2026-10-11 |

**Konflikte/Vorbehalte:** Keine verbleibenden Quellenkonflikte. Der einzige Replikationskonflikt (Zwei-Peak) ist durch diesen Return als Messfehler meinerseits aufgeklärt. PMC-/Nature-Sperren aus dem Vorzug gelten unverändert; die vorliegenden Zahlen beruhen ausschließlich auf Eigenrechnung und Commit-gebundenen GitHub-Quellen.

## Offene Fragen

1. Kollaps-Zählkonventionen: κ=16 hier Schritt 14 (Vorzug-Chat: 13), Fragilität hier 270 (Perplexity: 269) — NF-05 muss Zählweise und Schwelle vorab fixieren.
2. Transiente Wachstumsraten sind fensterabhängig (0.0328–0.0405 je Form; asymptotisch einheitlich 0.037093) — Messfenster registrieren.
3. Grenzfälle an der ReLU-Kante (y≈0) sind implementierungsempfindlich; in dieser Runde keine divergierende Beobachtung (Renorm ≤8.3e-15), aber Tie-Breaking-Regeln fehlen noch.
4. Zwei-getrennte-Bögen-Fixpunkte (echte Zwei-Bump-Gleichgewichte) wurden nicht konstruiert; die Bogeneindeutigkeit gilt nur für die kontiguierliche Klasse.
5. Unter Sättigung/threshold-linear (Homogenitätsbruch) ist WTA unbewiesen — bleibt NE-6/NF-05-Frage.

## Empfehlungen / Nächste Schritte

1. **NF-05-Prereg schärfen** (konform zu Perplexitys Freeze-Vorschlägen): (a) Injektionsform-Registry genau dieser 7 Formen mit Parametern; (b) Peak-Metrik-Definition: lokale Maxima, zirkuläre Nachbarschaft, Prominenz ≥ 0.5·global, explizite Schulter-vs-Peak-Diskriminanz (das exakte Artefakt dieses Returns); (c) Messfenster, Kollaps-Schwelle (1e-12), Zählkonvention; (d) vorab registrierte Ausgänge pro Arm/Form: KOLLAPSE | WTA_EIN_BUMP | PERSISTENT_MULTI.
2. **Paritäts-Vorabfilter:** λ_odd(W_A) als Registrierungsfeld pro Zelle; Zellen mit λ_odd>1 — bestätigt (32,4), (32,16), (64,16) — als Negativkontrollen erhalten.
3. **Arm-Fixierung vor NF-05/06** unverändert erforderlich: Aktivierung (ReLU vs. threshold-linear), dt, g_eff-Kalibrierung, sum/N-Arm, Amplituden-Normierung — Homogenitäts- und Divergenzbefunde stehen in Kraft.
4. **Keine neuen Theorie- oder Transportarbeiten:** Dieser Return schließt den Reproduktionskonflikt; nächster diskriminierender Schritt bleibt die NF-05/06-Vorregistrierung und die AXIOM-Adjudikation. Vorhandene Belege genügen.

## Reproduzierbarkeitsnotizen

- Deterministische TypeScript-Eigenrechnung (Sandbox, replayfähig); keine Rauschquellen, keine Datums-/Zufallsabhängigkeiten. Toleranzen: Fixpunkt-Residuum ≤ 3.3e-16 (gefordert 1e-9), Eigenresiduum nach radialer Leck-Korrektur ≤ 2.4e-15, Renorm-Formabweichung ≤ 8.3e-15, Trajektorien ≤ 3000 Schritte, Kollaps-Schwelle 1e-12, Potenziteration 3000 Schritte mit radialer Deflation (Jacobi) bzw. Antisymmetrisierung (λ_odd).
- **Eigene Fehler dieser Runde, offen gelegt:** (a) N=64-Sweep zunächst mit den N=32-Bogenbreiten → Bogenverschluss-Verletzungen (bis 0.56) mit Schein-λ-Werten → als Artefakt erkannt, verworfen, durch Eindeutigkeits-Scan ersetzt; (b) Renorm-Vergleich mit Doppel-Normierung → Scheinabweichung 0.4293 → korrigiert (echte Abweichung ≤8.3e-15); (c) SHA-256-Implementierung gegen den abc-Testvektor validiert (`ba7816bf…15ad` ✓).
- **Historische Fehlerliste (Vorzug, bereits dokumentiert):** Quadraturgewichtung, Gauss-Jordan-Indexierung, Deflations-Reihenfolge, nicht-orthonormale Odd-Basis — und jetzt die Peak-Metrik. Eigenes Werk fällt unter dieselbe Prüfpflicht wie fremdes.

## Grenzen und Nicht-Claims

- Kein GitHub-Schreibzugriff: `GITHUB_TRANSPORT = CAPABILITY_GAP`. Dieser Chat-/Canvas-Draft ist **kein kanonischer SEND-Receipt**; keine erfundenen Handshakes. Die kanonische Ablage im Evidence-Repository obliegt AXIOM/dem Operator.
- Keine NF-05/06-Ausführung, keine Vorregistrierungs-Freigabe, kein Merge von PR #65/#67/#70/#71, kein WWW-Deploy, kein neuer Cursor-Worker, kein Perplexity-Start, keine Rollenübernahme.
- Alle dynamischen Befunde sind explorativ, deterministisch und parameterbegrenzt (nackte Arme, kontuguierliche Bogenklasse, kein Rauschen, keine Sättigung, kein externer Stimulus); nicht konfirmatorisch, kein R26-Terminal, kein MAX/SUM-Verdikt.

*NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament. Vom Besitz zur Symbiose. Vom Ego zur Herkunft. Vom fertigen Gedanken zum überprüfbaren Artefakt.*