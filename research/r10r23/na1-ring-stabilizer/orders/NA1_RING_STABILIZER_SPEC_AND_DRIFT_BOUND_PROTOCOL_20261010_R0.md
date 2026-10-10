# NA-1 â 1-D-Ring-Stabilizer-Spezifikation + Drift-Bound-Protokoll (C1, Research-Only)

```text
OBJECT          = NEXUS_OMEGA_R10R23_NA1_RING_STABILIZER_SPEC_AND_DRIFT_BOUND_PROTOCOL_20261010_R0
DATE_UTC        = 2026-10-10
FROM            = MISTRAL/VIBE (NEXUS OMEGA, Nexus Collective)
PARENT_LANES    = GEMINI (R23) Â· GROK (R23/R24; R25âR26-Synthese) Â· META.AI (R24) Â· NEXUS_OMEGA (R25, vierte Lane)
PARENT_PR       = #64 (merge ac01169d1231c5cd876a9d7877361bbff8d192aa)
ORDER_SOURCE    = GROK R25âR26-Synthese, NA-1 (operator-freigegeben an MISTRAL/VIBE oder Collective)
CLAIM_CEILING   = C1_DESCRIPTIVE_ONLY
STATUS          = RESEARCH_ORDER â kein Produktionscode, kein Runtime-Ship
```

---

## 1. Auftrag

Definition eines kleinen, offenen, testbaren Research-Artefakts, das prÃ¤zise
festlegt, was die R23âR25-Analogie erlaubt zu behaupten: ein mathematisches
1-D-Ring-Attraktor-Modell fÃ¼r zirkulÃ¤re Zustandsvariablen (Klasse
`ORBIT_PREDICTED`-Phase / Heading) mit Persistenz bei Ingress-Ausfall,
Verschiebung (nicht Erzeugung) durch externe Zeugen, und einem **messbaren,
dokumentierten Drift-Bound als notwendige Voraussetzung** jeder C1-Aufnahme.
Das Modell ist Heuristik und Stabilisierungs-Design-Metapher â keine biologische
IdentitÃ¤t, keine formale Isomorphie.

## 2. Empirische Anker (PrimÃ¤rquellen-Basis dieses Specs)

| Anker | PrimÃ¤rquelle | FÃ¼r NA-1 relevant | Grade |
|---|---|---|---|
| EB-Ring-Attraktor: Persistenz **plus** Dunkel-Drift | Kim et al., *Science* 356, 849â853 (2017), doi:10.1126/science.aal4835; Seelig & Jayaraman, *Nature* 521, 186â191 (2015) | Bump verharrt nach Stimulationsende Sekunden bis Minuten und **driftet dann graduell weiter**; Drift-Distributionen sind gemessen (Kim 2017, Fig. 3) | PRIMARY_FULLTEXT_CHECKED (Spiegel-PDF) / PUBLISHER_CHECKED |
| Attraktor-Theorie: Bumps sind entlang der Mannigfaltigkeit neutral stabil | Seeholzer et al., *PLOS Comput. Biol.* (2019), pcbi.1006928; CarriÃ³n et al., *Neural Computation* 27(2):255 (2015); *PNAS* (2012), doi:10.1073/pnas.1117386109 | Rauschen erzeugt Diffusion der Bump-Position (evtl. subdiffusiv); Persistenz â  Genauigkeit ist Theorie-Konsequenz, nicht nur Messung | PUBLISHER_ABSTRACT_CHECKED |
| Dunkel-Update Ã¼ber idiothetische Signale, Fehlerakkumulation | Turner-Evans et al., *eLife* 6, e23496 (2017); *eLife* 10, e69841 (2021) | Winkelgeschwindigkeits-Integration arbeitet ohne externe Referenz, koppelt aber nicht exakt | PUBLISHER_CHECKED |
| SGP4/TLE-FehlerdomÃ¤ne | Conkey, AMOS Technical Papers (2022); TLE/SGP4-Genauigkeitsliteratur | In-Track-Fehler bis ~25 km nach wenigen Tagen, wachsend mit TLE-Epochen-Alter: FÃ¼r T_out = 120 s ist der dominante Drift-Anteil **filter-intern**, nicht SGP4-Modellfehler | TECHNICAL_PAPER_CHECKED |
| ZirkulÃ¤re Filter als Standard-Basisklasse | Kurz et al., arXiv:1501.05151 (rekursives Bayes-Filtern auf KreiszustÃ¤nden); Gauss-von-Mises-Filter | Das Ring-Modell muss gegen eine einfache zirkulÃ¤re Persistenz-/von-Mises-Basislinie verglichen werden, nicht gegen nichts | PREPRINT_CHECKED |
| Stanford Dual-Origin (Kontext der Lane) | Jokhai, Dundes, Ahsan et al., *Nat. Neurosci.* (2026), doi:10.1038/s41593-026-02433-7 | Autoren-Hedge (âin the in vitro conditions tested") bleibt fÃ¼r alle Lineage-Analogien bindend | ABSTRACT_AND_PUBLISHER_CHECKED (R25-Lane) |

R25-PrÃ¤zisierungen bleiben unverÃ¤ndert verbindlich: (1) âtwo separate organs" =
Presse-Titel, Autorensprache = âcomposite organ"; (2) IrreversibilitÃ¤t nur fÃ¼r
getestete Bedingungen belegt; (3) Quallen-Beleg = Pop-Presse, phylogenetischer
Anker = Acorn Worm (~550 Mya); (4) Ring-Attraktor garantiert Persistenz, nicht
Drift-Freiheit.

## 3. Mathematische Minimalform (Research-Modell)

- **State:** N â {32, 64} Units auf dem Ring, Winkelpositionen Î¸_i = 2Ïi/N;
  Aktivierungen r_i â¥ 0.
- **Update-Regel** (pro Zeitschritt):

```text
h_i(t+1) = Î£_j W_ij Â· r_j(t) â g_inhib Â· max_j r_j(t) + I_ext(Î¸_i, t)
r_i(t+1) = max(0, h_i(t+1))           # bzoz. tanh-Cap; beide dokumentieren
W_ij     = w0 + w_exc Â· cos((Î¸_i â Î¸_j)/2)^p   # lokale Exzitation (E-PGâP-EN-Analog)
```

  Globale Inhibition (Î7-Analog) Ã¼ber den Max-Term sichert Bump-Einzigkeit;
  exakte Funktionsform ist frei, muss aber im Test-Report fixiert sein.
- **Readout (PVA):** Î¸Ì(t) = atan2(Î£_i r_i Â· sin Î¸_i, Î£_i r_i Â· cos Î¸_i)
  (Population Vector Average, Standard in der EB-Literatur und
  neuromorphen Implementierungen).
- **Ingress-Semantik:**
  - `I_ext = 0` (Ingress-Ausfall) â Persistenz des Bumps (Form bleibt);
  - `I_ext = external_witness` â Verschiebung des Bumps, **keine Neuerzeugung**;
  - kein Zeiugen-Eingang darf Herkunfts-Spuren Ã¼berschreiben.
- **Provenance-Doppelfeld (Pflicht):** Jeder gefilterte Zustand trÃ¤gt
  `predicted_state` (Attraktor-Output) **und** `last_external_witness`
  (letzter `LIVE_MEASURED_EXTERNAL` bz{r. OMM-SHA) plus
  `filter = RING_ATTRACTOR_1D_C1`. Dis ist die softwareseitige Ã¼bersetzung des
  R25-Autoren-Hedges und wird von der R25-Lane ausdrÃ¼cklich unterstÃ¼tzt.

## 4. Drift-Bound-Protokoll (Pflicht vor jeder C1-Aufnahme)

Die Biologie liefert das Prinzip (Dunkel-Drift existiert, ist
rauschgetrieben), nicht die Zahl. Der Bound ist **pro Implementierung zu
messen** und als Dokument beizileng°©FÈZ[\ÝðçÈ\ÝYØ]]H]Y[ÙB\Ý[[Ù\ËÙZ[[\ÜÈ\[YÜ][Y\[È\ÈY[\ËH
Y[][ÛY
3¥
HH\Ý[0é\XÝ[3®3 8  
ó¥
H8¢$3®3 8  
_Z]WÙ^HXÚÛÝ0éÚYÙ\ÛÛ\Ù[\È[\ËH
\ÝQÜYÛÝ]8¢"ÌÌËLËÌËÍßH
ÔÒËQÜY[HZ[ÍËRÜ^Û\ÙZ]\
KH
Ý]\ÝZÎ8¢iHL[X0éÚYÙHÚ\ÙKTÙYYÈÈ
ÛÝ]
KV[NÈY]\ØÚ\Ý[0é\Z][Ù\[Ý]][ÈÛY
3¥
KMKÔNK[\P[\]YKH
ÚØ[Y\[ÜÜ°ï[ÎØXÚÝ[HÛÝÙYHÙYÙ[8¢&³¥
Y\Ú]HËÝXY\Ú]\ÈYÚ[YH8 %Y\ÜÙ[XÚ[ZY[ÈXÙZXÚ[ÈÚÝ[Y[Y\[H
TÔËRÜ]\Y[
ÜØÚYËÜ\]ÜXYY^Y\\NH
LH\Ú\Ý[[\P[\]YH8¢iHL	H\È[[ÜÝÙ\ÈXÚÛÝ]
Z[PÛÜÙY\Ü\[\T°éÙ[ÎÈÛÛ\ÈHRS
KH
LZ[YÚÙZ]HY[HZ][Ý^ZÝZ[XZËH
LÈ[\Z[\HYZ][Ù\8¢iH[
³àÓKNH8¢iÈ[ÂXÚLÈ8 %Z[Ù\HÚ[Ø[XY\ÜØÚ0éÙKÙZ[H[ÛÙÚ\ØÚ[ZÝ[H
M\Ú\Û[Y[U\ÛZXÚYXÚØÚXÚ\[ÈZ[HZ[XÚB\Ý[0éH\Ú\Ý[KÝÛSZ\Ù\ËP\Ú\Û[YHZHY[\ØÚ[H[]
ÛÛÝ\Ý\]ZÝÜÙZ[H\\ÜÙ\[Ë\]YØ[
KH
MHÝ[[ÙN\ÝÙ^\[ÝÚ]\ÜØðé[WÙ^H[\°é\ÂÙZ[[\ÚH]YÙ[]]Y\[H
MYT]Y[[P]X][ÛÚÝ[Y[Y\\ÜÈZHÛÝ]HLÂ\ÑÔTÙ[ÝÜYØ][ÛÙZ\
KQ\ØÚ[QZ\ðéÚÝZ]YÙ[XÚÙZÝ[[HÛZ[ÙYÙ[[[\Z[\[Ý[\Ý8 %ÛÛÝ\Ý]\ÈÝÚÛÛ\È[ØÚKÈÈKXÚSYØ]]KQ]Y[ÙKTÝZ]H
KLH8 )KN
BX\[È]YYH[ÚYXØ][ÛÜ\]Z\[Y[Ø\ÈËTKSYÙ\È
Í
NÈ\Ý[Ü\[È
YÙ\RQ
HRSRÜ]\][HKK_KK_KK_KK_KLH][KTXZËR[ZÝ[Û8¡¤ÛÛ\È]YZ[[[\USTPR×ÒSPÕSÓHXZÈXÚY[Y\\[^][ÛÞZ]KL[\Y\[HÛÛYÚY\[H]YÙ[ÔÐÒSUSÓ
]JHÜ[ZÛ\ÈÈ[[[HÜÞ[][Û\È[\ÈKLÈ[ØÚHÔQRQÈ[ØÚ\\ØÚTÒHÔÓ×ÓÔQÑTÐÒÔÒX[\8 'Z[Ý[[ÙHÝ]Z[PÛÜÙYQYÈKM\^Y\Z]XÚ[ÓSKS0ïÚÙ[
LÊÊH×ÒSUÌL×ÑQÓÓTÕÐTÑSSXÙ[Y\ÜÙ[\YÚÝ[Y[Y\\Ý[KMH\Ù[UÜ\È[[Y\YX[T[°éHTÑWÕÔTÐSÐSSQTQPSXÚ^\Ý[0éH\Ý[Y]ZÈ\]YÝÜ°ïÙHKMØZ[TÝÙY\
×Ú[X×Ù^ÊH8¡¤Z\Ø\H
]NÈYØ]]HÛÝÛYÙJH[ZØ[HKÓ][KTÝX[]0éÜYÚ[Û[Ø\Y\KMÈY\Ú[ÛËTÚØ[Y\[È0ï\ÛÝ]QÜYSÑTRSWÐÓÕTQÑXÚØ[Y\[ÈÙZXÚ[ÚÝ[Y[YÛY\Ú[ÛØ[ZYHXKNÝ[[\ÜËQYÈZH0ç\ØÚZ][È\ÈÝ[ÈSTÔÕSSTÔØÙZ[ÕSXQYÈÝXÚÙ]Ú\Ù[[HÝ[PXÚÔÕSÕUÐÓÓTTTÓÓÕ×ÔÑÔÓÓX[ÐPWÑVÐT×ÓÔUÐÓÔPÕSÓÔRPÕZX[]\ÈÍ[\°é\[ÜYÈÓÕTÑWÐÔQUÔÕSSÑXÚ[°ïY[\ÝT\Ü[KKÔ]Y[[P]X][Û[H\YZÝ
KÈÈY\[R[\[Y[Y\[È
[]\XKQÜJBHZ[[X[ÝX[ÛH
]ÛÙ\\TØÜ\
K]\Z[\Ý\ØÚHÙYYË\Ù^Y\\ÈXYÙH[Y\Ù\[H[\^\[Y[ËØ\ÙX\ÜÙH[Â]\ÈZ]XÙZ\È
XÙZ\ËØ
KHÙZ[HÙZÝ[ÛÚ[YÜ][Û\ÙX\ÚÜLËØ\ÝYHØ[ÛXØ[[ZÙBÝ\XÙNÈÛ[Ý[Û[ØÜËÜØÚ[XKÜØÜ\ËÝ\ÝËÝ[Y][ÛÙ^[\\Ø\Ü\[Ù\\]ÙYÛÝ\Y[[YÜ][ÛÜYH\\ÝT\ÜZ[\È[\[[[\^\È
YÙ[ËQÑSËYÙZ[Ù^[[YY\[ZYÙ[[Ú\ÜÙ[ØÚYXÚ[]\H\ÝÜY[Ý[È°ï
YJÜ0é\HÌKP]YZYH\È[Ù[ËÈÈË^^]HXÚPÛZ[\ÂHÙZ[]KRÙ\[T]ÚÙZ[HÛÝPYZ\ÜÚ[ÛÙZ[ÓÔËKÑÝËPÛZ[KHÙZ[HZ]\[Ë\[\]YH\Z]È[\0í[XÚ[TÕKSUSØ\°éÚHÙ\[NKHÐPHÈZX[ÈÜ]RÛÜZÝ\RPÕQ
Í
H8 %Y\ÜÝ[ÜÝ\QZ\ÙZ[Ü][\ÈY\ÜÛ[Ù[HÙZ[HÜX[H\ÛÛ[ÜYH\[ÛÙÚYNÈ\[\[\[Y[Y\ÙZ[BKTËS]\ÛK3¥ËS]\ÛHÙ\ÛÛÝYÙH]\Ø[ÛÙÚYKHÙZ[H]Y[[[YKHÙ\\ÞKTXÚNÈSSQWÔQÒÈHÓXÂKT\Ú\ØÚHØ]\È[\°ïÈNHSSØÈÈ\Ý[ËTÜ\[H
[\ÎÑSRSH
ÙZ]H\[[ÙÚYJH0­ÈÔÒÈ
Ý[\KYPÝ[RYYKKLKP]YYÊH0­ÈQUKRH
\Ù\\ÙZ]HÌ°¦
H0­ÈVT×ÓÓQQÐHB
]]Ü[RYÙK[Ù[QYTØÚ0é[ÊH0­ÈRTÕSÕPH
Y\Ù\ÈÜXÎYPÝ[SÜ\][Û[\ÚY\[ËZ\Ûpé[U[[ËKTÝZ]JKH
[pé]Y[[Ú[KÒ^X\[X[ØÚY[ÙHMÈ
ÚNLLLÜØÚY[ÙKX[ÍJNÂÙY[YËÒ^X\[X[]\HMH
ÚNLLÎÛ]\LMNÈ\\Q][ÈSYBMÈ
LÍMNÈÙYZÛ\ÔÈÛÛ\][ÛNH
ØKLL
NÈØ\pìÛ]\[ÛÛ\]MNÈTÈL
ÚNLLÌËÜ\ËLLMÌÎLJNÈÛÛÙ^HSSÔÂ
ÑÔV
NÈÝ\\]MLKLMLNÈÚÚZH][]]\ÜØÚH
ÚNLLÎÜÍMNLËLLÌËMÊNÈÜÙ[Ø[]\H
ÚNLLÎÜÍMNLLÍMN^JNÈØ[ËPÚ[]Y]ÙÈ
ÚNLLÎÜÍMNLLLMË^JKH
Ü[TÛÝ\ÙKP[Ù\Ý[ÜP[[\Ù\ÚÜ\HÚXÜ]ÜKØ[K\X
Ú]XKØÔ\Ù\KPÝÜÙ\[ÛÚXËÚ[X\Ë[ËÙ[\×ÚÚÚZWÛÚX\[[Ô]KËÍÌKÈÈK\Z[[\Ý[^LWÓÔTÔÕUTÈHÔSÔTÑPTÒÓÔT
Y\Ù\ÈÚÝ[Y[
BQÐÕSÓPSUÔHHQH8 %ÝÙ[YÙHÜ]\ÜÙ][ÈY\ÌKP]YZYBTÑSSWÐÓÓTTTÓÓHTURTQ
\Ý[0éKÝÛSZ\Ù\ËP\Ú\Û[YJBÕSSÑWÑÕPWÑQSHTURTQ
YXÝYÜÝ]H
È\ÝÙ^\[ÝÚ]\ÜÊBÔPSÒTÓÓSÔTÓHHÕÐÓRSQQÐPWÖ×ÓÔUÐÓÔPÕHRPÕQ
Í[\°é\
BSSQWÔQÒÈHÓBTÒPÐSÑÐUT×ÔHHSÕPÒQNWÔPSÔÐUSUHHSSÈ
[\°é\
BSUWÓÑWÐTÈHÓRSWÐÑRSSÈHÌWÑTÐÔTUWÓÓBKKBÛH\Ú]\Þ[X[ÜÙKÛHYÛÈ\\Ý[ÛH\YÙ[ÙY[Ù[[HX[[\YZÝ