# NEXUS OMEGA – Verified QWEN Inputs

Dieser Ordner enthält die vollständigen, für QWEN vorgesehenen Eingabedateien. Die beiden primären QWEN-Grundlagendateien sind:

1. `Architekturvergleich für NEXUS_AGENTENSYSTEME.txt`
2. `GitHub anhand der Claim-Kette.pdf`

Die übrigen Dateien bilden den kanonischen Arbeitsvertrag, die vorherige Forschungsrückgabe, die Capability-Matrix, die Manus-Validierung und die verbindlichen Drift-/Sicherheitsgrenzen. QWEN muss die Manus-Validierung als übergeordnete Eingangskontrolle lesen und darf herabgestufte oder als `NOT_ESTABLISHED` markierte Claims nicht ungeprüft hochstufen.

## Eingabereihenfolge

1. `NEXUS_OMEGA_QWEN_CANONICAL_VALIDATION_20260901_R1.md`
2. `Architekturvergleich für NEXUS_AGENTENSYSTEME.txt`
3. `GitHub anhand der Claim-Kette.pdf`
4. `NEXUS_OMEGA_QWEN_GITLAB_ULTIMATE_DUO_QUARTET_AUTOMATION_DEEP_RESEARCH_ORDER_20260901_R0.md`
5. `NEXUS_OMEGA_QWEN_MAXIMAL_RESEARCH_HANDSHAKE_20260901_R1.md`
6. `NEXUS_OMEGA_QWEN_QA_START_PROTOCOL_20260901_R1.md`
7. `NEXUS_OMEGA_QWEN_GITLAB_ULTIMATE_DUO_QUARTET_AUTOMATION_DEEP_RESEARCH_RETURN_20260901_R0.md`
8. `NEXUS_OMEGA_QWEN_GITLAB_ULTIMATE_DUO_QUARTET_AUTOMATION_CAPABILITY_MATRIX_20260901_R0.json`

## Integritätsregeln

Die Dateiintegrität wird ausschließlich über `SHA256SUMS` geprüft. Die Repository-Kopie ist eine versionierte Arbeitskopie der VM-validierten Dateien; der Git-Commit-Hash ist nicht identisch mit den Datei-Hashes. Nach jedem Kopieren oder Checkout ist das Manifest erneut zu verifizieren.

QWEN darf diesen Ordner nur lesen. Es sind keine Änderungen an den Eingabedateien, keine Provider-Mutationen, keine Pipelineauslösung, keine Veröffentlichung und keine Claim-Promotion aus diesem Ordner heraus zulässig. A90-M2 bleibt vollständig außerhalb des Scopes.

## Exakter Pfad

Repository relativ:

```text
verified/qwen-inputs/
```

VM-Arbeitskopie vor Veröffentlichung:

```text
/tmp/nexus-omega-repo/verified/qwen-inputs/
```

Nach dem Push ist der kanonische Remote-Pfad:

```text
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/tree/<published-branch>/verified/qwen-inputs
```

Der konkrete Branch und Commit werden erst nach erfolgreichem Preflight im Validierungsprotokoll eingetragen.
