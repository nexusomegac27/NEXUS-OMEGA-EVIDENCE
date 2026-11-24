# R43-8 original-custody and direct independent score reproduction audit

Raw original user files:
```text
R43_7_~1.ZIP 66342 B SHA256 6c067d212984e11f207894188fdc286ac7e8df8f6aca840ff2240a6199fe864b ZIP_CRC=PASS
INNER_EXPERT_RECEIVER 48421 B SHA256 430768a66f2c609a939c41cc8bea8f5dc1cca9a8733d6dc367f744ad3cdbc17a ZIP_CRC=PASS 11/11
R43_7_~2.ZIP 67854 B SHA256 38c091449c1be27fdffb4457c1b2413305015f7fa30abd7fb52aba4e61e78b4e ZIP_CRC=PASS 81/81
SOURCE~1(1).ZIP 723548 B SHA256 058b5784cb2cdf7377d916c8c4163371578dea5d3715e74c6a97aa3e2af69fea ZIP_CRC=PASS 13/13
REPORT_1 9674 B e4e8a10bf8b6af4b0933f895f2637038ed8aad871d4d0ccdcffde8f21dbc8286
REPORT_2 25462 B 8a290f85fd4bb8be6bdef9c42ab707381b4f4ce3d50fb220d45568ccd1063b3a
REPORT_3 21458 B 1ff0986e612cec7fb8d2a5c5c758468401b26df10cf66a520ec9d37fe1d30ff0
```

Original split.json:
```text
TRAIN 12 = clock_jump_drift(F00–F05) + mount_slip(F10–F15)
DEV 6 = sensor_noise(F20–F25)
TEST 6 = network_latency_correlation(F30–F35)
```
THIS IS A 1-DOMAIN TEST and a 4-domain generated bank, not 4-domain out-of-distribution validation. All labels live under producer-owned `01_FRESH_HOLDOUT_FROZEN/labels_protected` included in original ZIP, so public/privacy-safe R43-8 docs cite aggregates only; not a protected external holdout. MHEALTH original 75.6MB ZIP not in received files.

Original six primary label JSON files `F30…F35` and original five prediction JSON files read in original ZIP and scored independently in Python by AXIOM:
```text
IS_ALPHA_0.1_HALF = halfwidth + [max(0,(point-halfwidth)-truth)+max(0,truth-(point+halfwidth))]/0.1
v0_frozen = 18.303982903117085, coverage 3/6
v2_adaptive = 18.303982903117085, coverage 3/6
fusion_cost_matched = 18.303982903117085, coverage 3/6
ref_only = 6.6217, coverage 6/6
b_wide = 1000.0, coverage 6/6
```
The `v0`, `v2` and labeled fusion primary `predictions` objects contain identical six point/interval values; this is stronger evidence for NO DELTA than just a matching summary. The ref-only method consumes `reference_measurement` in task object; it is not a phone-only deployable model. The other 18 generated tasks were NOT independent primary TEST; secondary stratified sensitivity in producer receipt cannot retroactively replace primary test.

Producer E31 MHEALTH: 75567983B SHA256 16ad0ce709f3f00df18f348610d15bce0884b79e2143f57f446493673f02b8e0, producer-reported cross-subject binary correct 80/81/81, exact CI recorded, UCI DOI 10.24432/C5TW22 CC BY4.0 first-party verified; no raw MHEALTH data in operator provided archive so no independent data rehash or rerun by AXIOM here. E34 local test-root suites are not operator-authenticated independent evaluator. E29 simulated localhost 200 2×4 is not public W1; old P04 real 2×4 body/header remains PARTIAL only. All sources currently C1 research only.
