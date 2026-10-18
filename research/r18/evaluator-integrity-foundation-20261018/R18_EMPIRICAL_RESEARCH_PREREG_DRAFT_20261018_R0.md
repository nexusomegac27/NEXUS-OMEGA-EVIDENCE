# NEXUS OMEGA · R18 experimentelle Falsifikation — Präregistrierungsentwurf, keine Ausführung

```text
OBJECT = NEXUS_OMEGA_AXIOM_R18_INTEGRITY_AND_BYZANTINE_VALIDATION_PREREG_DRAFT_20261018_R0
STATUS = DESIGN_ONLY_NOT_REGISTERED_NOT_AUTHORIZED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
RUNTIME = FROZEN
R18_SHADOW_LOOP = HOLD
```

## Primäre Fragestellung

Verändert ein *versionierter und rechtmäßig verwendbarer* Filter-/Refine-Mechanismus unter derselben klar definierten Stör- und Angriffslage die Accuracy **starker ehrlicher Agenten** gegenüber den Alternativen: Einzelagent, unabhängige Mehrheitsabgabe ohne Nachrichtenverkehr, CP-WBFT (originale Senderkonfidenz) und – nur falls tatsächlich konstruiert – CP-WBFT mit extern und unabhängig kalibrierter Probe?

**Grundlage:** SAC arXiv:2605.09076v1/v2 getrennt dokumentieren, originaler Evaluator ist selbst ein LLM. Keine Realstudie, kein Zugriff auf Produktionsknoten, keine Live-Generierung. Dieser Entwurf ist ein **nicht ausgeführtes Experiment**.

## Ausschluss vor jeder Untersuchung

1. Korrektheit der Aufgabenreferenz undefiniert → `HOLD_REFERENCE`.
2. Originalquelle unversioniert/Quelldatei fehlend/Lizenz der Software nicht geklärt → `HOLD_SOURCE_LICENSE`.
3. Generator hat Schreibzugriff auf Prüfer oder unabhängigen Log-Anker → `REJECT_INTEGRITY`.
4. Ungebundene Angreiferfähigkeit, unbekannte lokale Fehlerzahl, nicht nachprüfbarer Graph → `HOLD_THREAT_TOPOLOGY`.
5. Evidenzlücken zu Privacy, Keys, Teilnehmern oder Autorisierung → `HOLD_SCOPE`.
6. `R18_47_CONDITIONS` nicht ratifiziert → `HOLD_OUTER_AUTHORITY` für jeden Shadow-/Runtime-Loop.

## Abgegrenzte Arbeitspakete

- **E0 Ground-Truth-Korpus:** öffentliche, rechtmäßig nutzbare Aufgaben; getrennte Versionen MATH30-v1 / MATH100-v2; unabhängige Review der Antworten; kein Einsatz privater NEXUS-Inhalte.
- **E1 Statistische Kontrolle:** vor Datenanalyse geplantes AB/BA-Pairing je Aufgabe und Topologie, ausreichend viele Aufgaben nach methodisch begründeter Power, stratifizierte Schwierigkeit; Runden und einzelne Agentenantworten nicht als unabhängige Stichproben zählen. Konfidenzintervalle der auf Aufgabenebene gepaarten Differenzen; vorab definierte Nichtunterlegenheitsgrenze (nicht hier erfunden).
- **E2 Angriffslage:** F-local-konforme Fehlerfälle plus **separate** Annahmeverletzungen; Senderkonfidenz 1.0, empfangsseitige LLM-Judge-Prompt-Injection, kolludierende Agenten, gemeinsame LLM-Fehler, unterschiedliche Uhr-/Antwortreihenfolgen, Replay, Paketverlust und Quellendrift. Jedes Experiment braucht ein eindeutiges `ATTACK_SCOPE`.
- **E3 Graph-Orakel:** Adjazenzmatrix, gerichteter/ungerichteter Typ, Robustheitsgrad-Zertifikat, Gradbedingungen und Per-Round-Message-Ledger; Quelle der Robustheit getrennt von semantischem Label.
- **E4 Ressourcen:** Kosten und Qualität getrennt als `task_accuracy`, `strong_preservation`, `H_MAJORITY`, `FAA`, `BFTI`, `bytes`, `tokens`, `joules_if_measured`, `time`, `abort_reason`, `missing_denominator`. Kein Einzelproxy.
- **E5 Evaluator-Eigenprüfung:** Source/Build/Dependency/Identity-Hash, getrennte Credentials und frozen Prompt/Oracle. LLM-Judges zusätzlich für Positions-, Verbosity-, Selbstpräferenz- und Rekalibrierungseffekte auditieren; nur Ground-Truth-Benchmarks für zuverlässige Accuracy-Behauptungen.
- **E6 Negative-Ledger:** jede Kandidatenablehnung mit `run_id`, `spec_hash`, `candidate_hash`, `oracle_hash`, `reason`, `timestamp_utc`, `prev_hash`, `checkpoint_ref`; unabhängiger Checkpoint verhindert unbemerkten Total-Rewrite. Keine ungeprüften personenbezogenen Rohtexte veröffentlichen.

## Erwartete Falsifier

`F1` SAC verschlechtert die starke Gruppe über die **vorher** deklarierte Nichtunterlegenheitsgrenze. `F2` CP-WBFT mit geschützt kalibriertem Probe-Reader ist mindestens so robust unter gegebener Aufgabe. `F3` r-Robustheit validiert angeblich semantische Richtigkeit. `F4` simulierte LLM-Verifikation lässt absichtlich falsche, prompt-injizierte Antworten durch. `F5` voreilige Effizienzaggregation überstimmt ein Integritätsveto. `F6` ein externer Key/Checkpoint/Rechain-Test akzeptiert veränderte Loghistorie. `F7` Fehl- und HOLD-Ausgänge verschwinden aus Nenner/Logs. `F8` eine Basis ohne Agentenkommunikation schlägt alle komplexen Kandidaten.

## Exit-Artefakte (nur nach gesonderter Erlaubnis)

`run_manifest.json`, `versioned_table.csv`, `topology_certificate.json`, `immutable_oracle_bundle`, `negative_fixture_ledger`, `quality_metric_report`, `resource_vector`, `independent_receiver_ack`, `gap_register` und ein unterschriebener Operatorentscheid **falls** Autorisierung beantragt wird. Die Anzahl der Proben, das Power-Ziel und konkrete Toleranzschwellen fehlen derzeit. Deshalb **kein experimenteller Start**.
