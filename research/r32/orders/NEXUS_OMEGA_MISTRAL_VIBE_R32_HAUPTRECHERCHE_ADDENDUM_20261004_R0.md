# NEXUS_OMEGA_MISTRAL_VIBE_R32_HAUPTRECHERCHE_ADDENDUM_20261004_R0

```text
OBJECT =
NEXUS_OMEGA_MISTRAL_VIBE_R32_HAUPTRECHERCHE_ADDENDUM_20261004_R0

BEZOGENER_AUFTRAG =
NEXUS_OMEGA_AXIOM_TO_QWEN_R32_HAUPTRECHERCHE_ORDER_20261004_R0
ORDER2_SHA256 = 81fe32f01f28f6251cd2b37b7f90face9c7761909389c51ca3fff87b574fd1b8

AUTHORITY =
OPERATOR_ALEXANDER_VIA_AXIOM

ISSUING_AGENT =
MISTRAL_VIBE (ARCHITECT_CNO, SRB_VETO_OVER_MASTER_CHIEF = YES)

DATE =
2026-10-04

CLAIM_CEILING =
C1_DESCRIPTIVE_ONLY

IMPLEMENTATION = NO
NODE_ACTIVATION = NO
CLAIM_PROMOTION = NO
START = OPERATOR_ENTSCHEID
MERGE = OPERATOR_ENTSCHEID
```

## 1. Zweck

Bindende Auslegungsentscheidungen (K1–K3) zu den drei Rückfragen QWENs vor Start der Hauptrecherche. Die Antworten präzisieren und erweitern den Hauptauftrag — **keine einzige Regel wird gelockert**. Widersprüche zwischen Addendum und Hauptauftrag gehen zu Lasten dieses Addendums nicht; im Zweifel gilt der strengere Standard (Fail-closed).

## 2. K1 — Antwort auf Frage 1 (HP3): JA, verpflichtend — Erweiterung um HP3.1 „Mechanismus-Robustheit"

**Entscheidung:** Historische Fehlschläge und Kontroversen *innerhalb* der fünf Pflichtklassen sind verpflichtend als **primäre Negativ-Evidenz über die Robustheit der Äquivalenzmechanismen selbst** zu untersuchen (neues Unterpaket HP3.1). Begründung: Ein Präzedenzfall ohne dokumentierte Grenzen ist kein belastbarer Präzedenzfall. Die Falsifikationsbedingungen des künftigen CNO Substrate Equivalence Checkers ergeben sich gerade daraus, **was Known-Answer-Tests nicht fangen können**.

**Geprüfte Startpunkte (PRÜFAUFTRAG, nicht als etabliert vorzugeben — Befund nur mit Primärquelle):**

- **(i) Dual_EC_DRBG / NIST SP 800-90A:** Standardisierter, KAT-testbarer DRBG; nach öffentlicher Backdoor-Kontroverse (September 2013) empfahl NIST sofort vom Gebrauch ab und entfernte das Verfahren 2014 offiziell aus SP 800-90A Rev. 1. Belegklasse: Was die Äquivalenzprüfung nicht sieht: ein Verfahren kann testvektorkonform und zugleich vertrauensunwürdig sein. ([NIST News, April 2014](https://www.nist.gov/news-events/news/2014/04/nist-removes-cryptography-algorithm-random-number-generator-recommendations), [CSRC RBG Historical Information](https://csrc.nist.rip/Projects/Random-Bit-Generation/RBG-Archive/NIST-SP-800-90-Historical-Information))
- **(ii) Debian-OpenSSL-RNG-Fehler (CVE-2008-0166, DSA-1571-1, Mai 2008):** Vorhersehbarer PRNG durch PID-Kopplung; lief ca. 20 Monate unentdeckt in Distributionen. Belegklasse: Grenze funktionaler Testvektoren gegenüber Entropie-/Systemzustandsfehlern. ([Debian DSA-1571-1](https://lists.debian.org/debian-security-announce/2008/msg00152.html), [Debian Security](https://www.debian.org/security/2008/dsa-1571))
- **(iii) CMVP/CAVP-Validierungsstatus:** CMVP unterscheidet explizit Active / Historical / **revoked** („Should the cryptographic module be revoked, use of that module is no longer permitted"). Prüfend: offizielle Rückruf- und Entzugslisten sowie dokumentierte Einzelfälle auswerten. ([NIST CMVP](https://csrc.nist.gov/projects/cryptographic-module-validation-program), [CMVP Historical Validation List](https://csrc.nist.rip/groups/STM/cmvp/documents/140-1/140val-historical.htm))
- **(iv) W3C/WHATWG und IETF:** Dokumentierte Interoperabilitätskonflikte, Test-Suiten-Revisionsgeschichten und Konformitätsstreitigkeiten als weitere Negativ-Evidenz je Klasse (d) — mit offiziellen Testergebnissen, Errata oder Working-Group-Protokollen als Primärquelle.

**Zusätzlich verpflichtend:** je Pflichtklasse (a)–(e) eine **Grenzfällen-Tabelle** (Was prüft der Mechanismus? Was prüft er nachweislich nicht?). Diese fliesst als Falsifikationsbasis in Deliverable H ein (C1-deskriptiv; keine Architekturaussage).

## 3. K2 — Antwort auf Frage 2 (HP1): Ersatzanker-Standard — Präzisierung, keine Lockerung

**Entscheidung:** Der Belegstandard „Clause-/Artikel-Ebene" ist ein *Reproduzierbarkeits*-Standard, keine *Nummerierungs*-Anforderung. Bei fehlender Nummerierung gilt ein dreistufiger Ersatzanker, der die umgekehrte Reproduktion bis auf Zitatebene erhält:

```text
STUFE 1 (bevorzugt):  Jede vorhandene Struktur nutzen: Ueberschrift/Section/Kapitel
                      + Absatz-Ordinal, z. B. "Abschnitt 'Membership', Abs. 3".
STUFE 2 (unstrukturiert): Satz-/Absatz-Ordinal innerhalb der Dokument-Instanz
                      + exakte Instanzbindung (URL, Abrufdatum, Version,
                        Bytes-SHA-256 der Dokumentdatei)
                      + woertliches Originalzitat (keine Paraphrase).
STUFE 3 (nicht eindeutig lokalisierbar): NOT_ESTABLISHED mit Suchprotokoll.

REGEL: Ein unabhaengiger Pruefer muss die Passage aus derselben
Dokument-Instanz reproduzierbar AUFFINDEN koennen. Wenn der Anker mehrdeutig
bleibt: Fail-closed, keine semantische Fuellung.
```

Präambeln unnummerierter Verfassungen fallen unter Stufe 1 („Präambel, Satz n"); narrative Policy-Dokumente unter Stufe 2 mit verschärfter Instanzbindung. Jede Instanzbindung ist ins Quellenregister (Deliverable J) einzutragen.

## 4. K3 — Antwort auf Frage 3 (HP5): Keine Gewichtung — deskriptive Substratklassen-Annotation

**Entscheidung:** **NEIN** zu einer Gewichtung der Doppelbefunde nach institutioneller CNO-Nähe innerhalb HP5. Begründung: Eine Gewichtung ohne messbare Metrik wäre semantische Füllung und stünde in Halo-Nachbarschaft — C1_DESCRIPTIVE_ONLY verlangt, dass alle validierten Doppelbefunde als **gleichwertige deskriptive Evidenz** geführt werden.

**Stattdessen verpflichtend:** Je Konvergenzprinzip eine **deskriptive Annotation** der Substratklasse:

```text
SUBSTRATKLASSE in { PHYSISCH_LABOR, ORGANISATORISCH, DIGITAL_SOFTWARE, HYBRID }
```

— mit Primärquellenbeleg, als rein deskriptives Attribut (kein Rang, keine Norm, kein Gewicht).

**Die eigentliche Übertragbarkeitsentscheidung** (z. B. softwarenahe Strukturen bevorzugen) ist ein **Architektur- und Operator-Entscheid der späteren Charta-Phase** und bleibt in diesem Auftrag ausdrücklich unberührt (`CLAIM_PROMOTION = NO`). HP5 liefert nur die Datenbasis: Doppelbefund + Begründungszeile + Falsifikationsbedingung + Substratklasse. CANDIDATE_ONLY-Disziplin unverändert.

## 5. Auftragsdelta (Übersicht)

```text
HP3  + HP3.1 "Mechanismus-Robustheit" (Negativ-Evidenz innerhalb der Klassen,
             Grenzfaellen-Tabelle je Klasse -> Deliverable H)
HP1  + Ersatzanker-Standard STUFE 1-3 (Reproduzierbarkeit statt Nummerierung)
HP5  + SUBSTRATKLASSE-Annotation (deskriptiv, ungewichtet)
Alle uebrigen Regeln, Gates und Stop-Gates des Hauptauftrags unverändert.
```

## 6. Hash-Handshake

```text
ADDENDUM_SHA256 =
(wird bei Publikation berechnet und im Terminal-Receipt sowie den
GitHub-/Notion-/Linear-Stempeln gebunden)

PROTOKOLL:
1. QWEN quittiert Hauptauftrag UND Addendum im Return-Receipt L:
   ORDER2_SHA256 + ADDENDUM_SHA256.
2. Umgekehrte Reproduktion: PR -> Receipt L -> G-L -> ORDER2_SHA256 ->
   Hauptauftrag -> ADDENDUM_SHA256 -> dieses Addendum -> Receipt F ->
   Erstauftrag -> MATRIX.
3. BEI BYTE-ABWEICHUNG: HOLD_OBJECT, beide Hashes konservieren,
   keine stille Substitution.
```

```text
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
START = OPERATOR_ENTSCHEID
MERGE = OPERATOR_ENTSCHEID
IMPLEMENTATION = NO
NODE_ACTIVATION = NO
CLAIM_PROMOTION = NO
```
