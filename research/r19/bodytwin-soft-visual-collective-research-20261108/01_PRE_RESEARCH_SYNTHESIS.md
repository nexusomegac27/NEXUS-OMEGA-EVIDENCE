# R19 · Vorrecherche, konkrete Befunde und konkurrierende Entwicklungsrichtungen
## 1. Was wir tatsächlich haben
R18 hat einen lokal gehashten, in der Folge durch Cursor statisch bereitgestellten anatomischen Add-on Viewer. Die nachgelieferten Cursor-Receipts belegen auf Report-Ebene einen scoped Hostinger/Git-Deploy; der Parent-/bodytwin/-Viewer integriert ihn noch nicht. Die HTTP-PNG-Transformationslücke und der HTTP-Datenlayer-Readback bleiben offen, GPU-WebGL ist unbewiesen. Keine Neu-Erhebung der R17.1 Anatomie ist nötig: 203 Skelett + 88 Muskulatur + VH male/female exklusive Organgruppen sind Materialgrundlage.

## 2. Wissenschaftlicher Kern
- Medizinisch kuratierte **Referenzoberflächen** sind nicht medizinische Messung. Geschlechtsbezogene Organreferenzen sind keine vollständigen zwei sex-spezifischen Körpermeshes.
- Gait2392 ist ein 23-DOF Lower-limb/Torso Modell; ohne BodyParts3D-to-OpenSim registration, Bind Poses, Skin Weights und konsistente Maße entsteht kein validiertes Rig.
- Ein Smartphone-Segment-Quaternion genügt nicht für Ganzkörperpose. Unrealistische ungemessene Bewegungen sind als `UNOBSERVED` zu kennzeichnen.
- R17.1 30 optimierte Strukturen -> 96,173 Tris sind ein Subset-Test, nicht Gesamtgröße des Visuals (statische Assembly etwa 709,594 Dreiecke laut R18-Fundament).
- Unter `P'=q_L P q_R^{-1}` erfordert eine reine räumliche SO(3)-Rotation via Konjugation `q_L=q_R=q`; `q_L=q_IMU,q_R=1` ist gerade keine unveränderte w-Hyperebene. Eigenständige formale Tests nötig.

## 3. Drei evolutionäre Architekturpfade (kein Präjudiz)
**A — Anatomisches Referenzlabor:** BP3D/HRA hierarchische Layer mit auswählbaren FMA/UBERON-Objekten, präziser Provenienz, vereinzeltem Raycast, LOD, Körperansichten und offline Failover. Geringes Risiko; statische Referenz.
**B — Holographischer Forschungs-Bodytwin:** dieselben unveränderten Mesh-IDs plus nicht-kausaler Fresnel-/Laser-/Contour-Shader und normierte Interaktion. Visualisierungsmodus, niemals Nachweis physikalischer Laser oder Messung.
**C — Dual-Pane SO(4) / Anatomie:** bisherige abstrahierte SO(4)-Projektion bleibt unverändert; der anatomische Viewer erscheint nur als verlinkte Zusatzfläche bzw. kontrollierter iframe bei explizitem Add-only PASS. Keine semantische Statusübertragung aus Soft zu Hard.

## 4. Priorisierte offene Probleme
P0 HTTP-MIME/Content-Encoding/Png byte/pixel transformation; Data-Layer HTTP unverifiziert.
P0 Shared-Write-Surface: keine blinde Parent-iframe-Injektion, kein überlappendes Deployment.
P0 GPU real + Mobile WebGL Kontextverlust; hier nur lokale DOM-Fallback Evidenz.
P1 echte weibliche Körperreferenz auf eigener Rechte-/Ontologie-/Registrierungsbasis.
P1 statische Mesh-zu-Segment- und Biomechanik-Registrierung.
P1 Asset LOD und Per-Device Budget.
P2 Historische Evidenz-/SO(4)-Kopplung als erklärter Forschungsmodus, nicht kinematische Wahrheit.
P2 bitemporale Auditierung: source SHA, HTTP representation SHA, decoded pixel comparison, browser capture receipts.

## 5. Rang und Priorität
R19 ist zunächst **Forschung in Papierform**. Kein Automatismus des Agentenkollektivs wird angenommen. Jede AI-Lane schreibt ihre eigene vollständige technische Entwicklungsversion und die Alternativkandidaten. AXIOM erstellt danach eine Konfliktmatrix; Cursor erhält erst durch gesonderte Operatorautorisierung einen Ausführungsauftrag. Geschlossenes Paket ≠ geschlossene Forschung.
