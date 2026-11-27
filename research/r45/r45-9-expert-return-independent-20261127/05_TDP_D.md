# 05 — Programm D: Konsolidierung Temporal Dream Phase und kollektive Falsifikation

Diese Konsolidierung bündelt die Erkenntnisse der Runden R45-6/45-7/45-8/45-9 (inkl. GLM-Return R1 als
LOCAL_VERIFIED_INPUT) zu den operativen Regeln für R46-1. Quellen: R45-7-Order (`4856e44f…`),
GLM-Return R1 (`202611~1.ZIP`, byteverifiziert), R45-9-Order (`bef961ac…`).

## D1 — Feste Regeln (konsolidiert, nicht neu erfunden)

1. **Trennung Exploration/Ausführung:** Phantasie-Phase (Simulation, alternative Modelle) besitzt nie
   operative Autorität. Autorität entsteht ausschließlich am Schleusentor aus neuer, aktionsgebundener
   Autorisierung (B3) — nicht aus Modellkonfidenz, Konsens oder Simulationserfolg.
2. **B4-Split:** Beobachtungsbereitschaft (B4a) ist **vor** dem Effekt zu prüfen; der Effektnachweis (B4b)
   erst danach. Ein Settlement ohne unabhängige Beobachtung bleibt `UNKNOWN`, nie `SETTLED` (eigener
   GREEN-Nachweis, Probe 10).
3. **Snapshot-Wiederbelebung verboten:** Ein Snapshot kann abgelaufene Autorisierung nicht wiederbeleben;
   `epoch_floor` + `stop_latch` (AXIOM-Muster, repliziert: `stale_epoch`/`stop` → `DENIED`, 13/13).
4. **Lokaler Rollback ≠ externer Rollback:** Ein DB-Rollback nimmt einen externen Effekt nicht zurück
   (konkret demonstriert, Probe B1.4). Für externe Effekte gilt Outbox/Saga mit Kompensation (G09).
5. **Ressourcen-Limits als harte Nebenbedingung:** Sicherheit wird nicht gegen Kreativität/Effizienz
   aufgerechnet; Evidenzproduktivität schlägt Textproduktivität (R44-4-Lektion).

## D2 — Matched-Budget-Erkenntnis (Prior-Return, LOCAL_VERIFIED_INPUT)

Der GLM-Return R1 (E3) berichtete seed-fix: unsicherheitsgeführte Exploration verbesserte den Brier-Score
0,0470 → 0,0318 gegenüber direkter Planung bei gleichem Budget, während Unsicherheits-Proxies die
Fehlspezifikation **nicht** entdeckten (0 Entdeckungen). Diese Zahl wird hier **nicht** als eigener Befund
 beansprucht, sondern als konsolidierte Vorlage übernommen — Replikationspflicht für R46-1, falls die
Phantasie-Phase produktiv werden soll.

## D3 — Kollektive Falsifikation

- Ein gültiger ungelöster Gegenzeuge hat Vorrang vor jeder Anzahl zustimmender Experten (R45-7-Order §7.D).
- Scheinfalsifikation (Test besteht, weil Prüfpunkt fehlt) ist durch prädikatsbasierte Register statt
  Zählregister abgedeckt (GLM-Muster: „kein stiller Pass“).
- **Konflikt-Registrierung dieser Return:** Der AUTO_CLAW-Eingangsstack verletzt sein eigenes Manifest
  (7/33 fehlen) — dokumentiert, nicht still korrigiert. Nicht-Zustimmung statt stiller Übernahme.

## D4 — Was daraus für R46-1 folgt

Die drei Schichten (DREAM/GATE/REALITY) sind als Datenvertrag abbildbar: L2 (EXPLORATION) trägt
`claim_ceiling=C1` und nie `authority`; jede L2→L3-Transition braucht ein neues, aktionsgebundenes Grant
mit Ressourcenfence und Beobachtungsbereitschaft. Die Schleusentor-Bedingungen (12) sind im
`05_CONTRACT.json`-`authority`-Block bereits als Pflichtfelder angelegt (request_id, nonce, principal,
action_descriptor_hash, payload_hash, target, policy_version, epoch, resource_fence, expiry,
aggregate_reservation, observer_ready) — genau diese Felder waren in den GREEN-Proben bindend.
