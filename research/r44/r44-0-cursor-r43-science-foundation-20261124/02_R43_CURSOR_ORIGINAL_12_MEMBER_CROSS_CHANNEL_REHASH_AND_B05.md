# AXIOM 2026-11-24 independent R43 Cursor return replay — exact 12 files and B05 seal defect

**Grounded operator originals**: ZIP `NEXUS_OMEGA_CURSOR_R43_ALL_NINE_ROUNDS_SCIENTIFIC_CUSTODY_AND_OFFLINE_REPAIR_RETURN_20261124_R0.zip` 11447B SHA256 `a47e0175ea33d6f1b4082ce0feb25695f9215eac0ec2ebb77dbb5833a7ae5055`, sidecar 167B SHA256 `4718eeab7b59d9d79215784dd02a67b38276e0ab5083f5ff4230987b7e58ea17`. `sha256sum` independently executed, sidecar contents exact ZIP hash. Python zipfile CRC PASS 12 members.

**Independent GitHub file source**: [Draft PR #428](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/428) OPEN DRAFT HEAD `031430f2f6846065b624b3f30006cf5644f8e800`, path `research/r43/r43-cursor-pre-r44-return-20261124/`. All twelve GitHub files independently fetched, UTF8 byte and SHA256 matched uploaded zip exact `12/12` using JS SHA256 independently test-vectored against SHA("") and SHA("abc"). This verifies GitHub transport parity, not experimental truth.

| Original member name | Exact bytes | AXIOM SHA256 | Internal manifest name? |
|---|---:|---|---|
| 00_EXECUTIVE.md | 1195 | `cdc89513f76ba876eda5d885a4086a86ff985a0b7101dcad57ac3fc8f11a7b97` | YES |
| 01_HANDSHAKE.md | 782 | `991ab90388ccb277950a782f999f1bcef3cc38069438b7d4174c7485f99bf590` | YES |
| 02_EPISTEMIC_WALLS.md | 502 | `c6634493ece801fac04898df166c704c0bb56f55850bb701603efa5394bfa169` | YES |
| 03_RESULT.md | 896 | `bfd8d30bebe1e5d8d532a0de1670721ea4b6885487719bb898e4bf400a2e97b7` | YES |
| 04_MACHINE.json | 1571 | `8954f494bed301fd686c42f479771d258457600c54b4b1f17059ddfcccff01c9` | YES |
| 05_C0_C3_EXECUTION_LOG.md | 827 | `d7312b1c397c1a9aef138ed56d2109a2d1eb5d3f8e9711d8f79c82157f56840e` | YES |
| 06_B01_B04_CONTRADICTION_LEDGER.md | 1942 | `955462487eb81877a52d7396cbff0f82eca683dbe6e56d3718c3e5301e0e8326` | YES |
| 07_C2_OFFLINE_STATUS.md | 2417 | `2f5a39608d9e1346452ce766326717670537e1c9191cfd87a798b33db8adb443` | YES |
| 08_M9_CROSSWALK.md | 1256 | `2a244fde56d3ecb98eca69121a5e9769f2fc84214e799d0965ee5e32ff84f8d2` | YES |
| 09_OBJECT_CUSTODY.md | 2816 | `1d45ae22489f17e079e543369fe2123a107793883a389012fb65c7966d0fc7ca` | YES |
| 10_PACKAGE_RECEIPT.json | 2051 | `560188c01b2cd3269b116499d44762c5f5cf26907878a5decac27ba092ab5761` | NO, extra file |
| 99_SHA256SUMS.txt | 878 | `b377dab6690d6add74ec3b56ec5b0bed1342acb84a0ad3f460e8bdc95d87b622` | N/A SELF, not self listed |

**B05 independent contradiction**. The extra `10_PACKAGE_RECEIPT.json`, itself correct/matching bytes, claims PREVIOUS 10336B ZIP, SHA `f70eb6bc5ebcbdebdaa6f757805162c90b7e0c2fa0809022fc298d54b868098a`, 11 members, sidecar166B SHA `4f03bb1f0cc53cc31c3238640296310bc1ac75c749c4dbc29ea14fc0ae0c1f22` and internal 99 manifest868B SHA `6d4b5ce0a709699df18fefa16a87759922c20070f784d7ddc7439223950f85a9`; final delivered has 11447B, 12, sidecar167B hash `4718ee…` and internal 99 878B `b377da…`. This pattern is consistent with an intermediate pre-append package snapshot, but this chronology was **not independently proven**. Treat as `B05_FINAL_PACKAGE_RECEIPT_NOT_CURRENT`/ `FINAL_EMBEDDED_RECEIPT_SELF_SEAL_NOT_ESTABLISHED`. 10 core listed payloads are 10/10 correct and actual final outer sidecar is correct. Do not confuse B05 with B03 prior Manus missing PDF.

**Necessary addendum**: preserve old ZIP/report immutably; issue a new explicit `FINAL_TRANSPORT_SEAL_CURRENT_ZIP` outside ZIP with current size, SHA, sidecar, 12 members and 10+receipt manifest coverage; optional additive member hash for receipt and manifest rather than self-referential ZIP seal. Need producer/custodian source and independent rehash. Do NOT alter original historical return or retroactively claim 12/12 MANIFEST_MATCH.

**Other scientific claims scoped**: C0 live ACK and C3 actual Draft verified; C2 FC2 13 neg/7 pos reported but original 9803B receipt SHA00612c… and test code absent this ZIP, no AXIOM independent runner execution now; source-only. No Grok abstention bytes, FDA sample bytes, independent external evaluator.
