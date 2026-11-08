# R19 · Quellen-, Live- und Chronologie-Bindung
## A. Tatsächlich bytegeprüfter lokaler R18-Vorgänger
- ZIP `NEXUS_OMEGA_R18_SOFT_BODYTWIN_VISUAL_INTEGRATION_20261108_R1.zip`: 13.005.547 Bytes; SHA-256 `e55f9fbde480b00dab225591b5227fa8bab1bb241bf1d3bac283df091f8b7421`; in dieser Sitzung als lokaler Upload mit bytegenauem SHA-256 nachgemessen.
- Internes Receipt `receipts/STATUS_RECEIPT_R18_LOCAL.json`: 2.000 Bytes, SHA-256 `7a6042380115a0e5a1665c7ecb49f2c96263ba52425ce9e76f2941c979dbf627`.
- Internes Layer-Register `receipts/SOURCE_LAYER_BINDINGS_R18.json`: 2.960 Bytes; SHA-256 `a6793c5a1106b56c133ffc36d60565315c3b65f6e029338d5210448c7f4eb2c4`.
- R17 external ZIP `6c3e2757f9ca23e9a4dfb4cf65201788797baa3a52f9ba094ad6bba8eca450c4`; R17.1 external ZIP `385ae867f123c29e9b40c4738c547f9d6e01a86c4a13a21edf50dea9195067fb`. Diese Bindungen sind aus dem lokalen R18-Receipt übernommen, nicht durch erneutes Fetch aller externen Quellen in dieser Studie ersetzt.
- 4 belegte Datenlayer: skeleton 6,945,287 Bytes SHA `937e21d33deb50cd979478d456b7921ec1d9150dd49831ad80946204aa3403d5`; muscles 5,965,076 Bytes SHA `d915ba40685a3a5c85c495dafdda0769de51a94ccfa9573c91ce7f22a5525a1d`; organs_male 7,046,328 Bytes SHA `a330ee1798f6663a456bd855f68d37513b38115c851e6f538319ac504885054a`; organs_female 5,745,988 Bytes SHA `354e5c9409372c8a579e94dc88e6b76f8f6170956e4a`. **Diese SHA-Kette ist für lokale Assets**, nicht HTTP-repräsentative Bytes.

## B. Aktueller Operator/Cursor-Live-Return — REPORT LEVEL, kein unabhängiger Remote-Rehash
- `R18_CLOSED_PARTIAL_SUCCESS_C1`; `SOFT_VISUAL_HOSTINGER=DEPLOYED_SCOPED_STATIC_GIT`.
- `DEPLOY_HEAD=bde215368abcb39f3fefdbf981efedeaf0a1db3a`.
- `INDEX_HTTP_MATCH_LOCAL=YES`; `SMALL_TEXT_4_OF_4=MATCH`; `PNG_DISK_4_OF_4=MATCH`; `PNG_HTTP_BYTE_MATCH=NO` mit berichteter Delivery-Transformation; `DATA_LAYER_HTTP_BYTE_MATCH=NOT_ESTABLISHED`.
- `PARENT_HAS_R18_IFRAME=NO`, `PARENT_ADD_ONLY_HOSTINGER=HOLD_SHARED_WRITE_SURFACE`, `BROWSER_GPU=NOT_ESTABLISHED`, `BODYTWIN_VALIDATED=NO`.
- `G8_RECEIPT=3007/76dba4a326ccab463540a001a04df61fbbe14d224ba0e3825510ecd13de7f4c2` und `EXECUTIVE=2174/01845599bef8a6895ae604f6512c1fa493ef47fbedec94b1f1819324690d1321`, Originalbytes hier nicht übergeben. Beide werden nicht als unabhängige GitHub-Receipts umbenannt.

## C. Externer WWW-Preflight vom 2026-11-08
- `https://www.nexus-mobile.de/bodytwin/`: Web-Suchindex enthält bisher Bodytwin 2026-09-14 R0, symbolisches SO(4) und `DERIVED_MINIMAL_PROJECTION`; Suchindex **nicht** zeitgleicher Live-Browserbeweis.
- `https://www.nexus-mobile.de/research/`: indizierter öffentlicher Stand `BODYTWIN_VALIDATED=NO`.
- `https://www.nexus-mobile.de/bodytwin/soft-visual/`: direkter Web-Fetch hier fehlgeschlagen; kein HTTP-Status/Headers/DOM zum behaupteten aktuellen Render verfügbar. Kein gegenteiliger Deploybeweis.
- Kein eigener laufender Hostinger-Zugang, kein Browser-GPU und keine Original-HTTP-Bodies in dieser Forschungsrunde. `CURRENT_LIVE_VERIFICATION=PARTIAL_SOURCE_GAP`.

## D. Primärquellen und Prüfreferenzen
| Quelle | Eigenschaft | Vorläufige Belegklasse |
| --- | --- | --- |
| https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html | BodyParts3D CC BY 4.0, Attributionstext, Update 2025-02-27 | offiziell geprüft |
| https://hubmapconsortium.github.io/ccf/pages/ccf-3d-reference-library.html | HRA/CCF reference organ objects CC BY 4.0, VH male/female | offiziell geprüft |
| https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53090607/Mus | Gait2392 23 DOF, CC BY 3.0 | offiziell geprüft |
| https://www.nlm.nih.gov/research/visible/visible_human.html | Visible Human Herkunft | Primärquelle zur erneut punktgenauen Prüfung |
| https://threejs.org/docs/pages/GLTFLoader.html | Meshopt/Draco, glTF | aktuelle technische Doku |
| https://threejs.org/manual/pages/webgpurenderer | WebGPU/ WebGL2 Fallback | aktuelle Doku, nicht R18-Fähigkeitsnachweis |
| https://registry.khronos.org/glTF/ | glTF Standard | Primärspezifikation |
| https://developer.mozilla.org/de/docs/Web/API/WebGL_API/WebGL_best_practices | mobile GPU/VRAM/Context | technische Leitlinie |
| https://www.w3.org/WAI/WCAG22/quickref/ | WCAG 2.2 | Zugänglichkeitsstandard |
- Lizenzübertragung einzelner derivativer Assets bleibt gesondert prüfpflichtig; kommerzielle Nutzbarkeit nicht aus automatischer Lizenzkategorie ableiten.
