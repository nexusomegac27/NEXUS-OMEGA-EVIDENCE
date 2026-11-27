# R46-4 order stack transfer note

The complete order stack ZIP (26947 bytes, SHA-256 364002738039870ed3a8f03cc3b79174a6ff573e8beada3b0631bd84fed4f679, 9 members, store-only deterministic build, fixed timestamps 2026-11-27 16:00 UTC) is delivered as base64 transport file NEXUS_OMEGA_R46_4_GLM_R1_ORDER_STACK_20261127.zip.b64 because the API custody route carries UTF-8 payloads only.

Recover byte-exact: base64 -d NEXUS_OMEGA_R46_4_GLM_R1_ORDER_STACK_20261127.zip.b64 > NEXUS_OMEGA_R46_4_GLM_R1_ORDER_STACK_20261127.zip
Verify: sha256sum must equal the sidecar value; internal manifest 99_SHA256SUMS.txt (8 payload members) and CRC 9/9 were verified before push.
Manifest SHA-256: 84f4fab1a9f6c9fcf0c49d018a3395b373e8aa9421e1ca8490173728fe6fa0ca
