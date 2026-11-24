#!/bin/bash
# R44-6 receiver fetch: exact-commit downloads (no piping into shell; files only)
set -u
COMMIT="89ccff827d564309cba3274bff94a6d577e6853a"
BASE="https://raw.githubusercontent.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/${COMMIT}/research/r44/r44-6-github-source-access-and-bodytwin-20261124"
DEST="/home/z/my-project/scripts/r44_6_receiver/fetch/r44_6_package"
A63="https://raw.githubusercontent.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/a63ee94607b73fa4f5b1ae788306f462d93cfcc9/research/r44/r44-5-operator-start-binding-20261124"
DEST_A63="/home/z/my-project/scripts/r44_6_receiver/fetch/r44_5_additive_at_a63ee946"
mkdir -p "$DEST" "$DEST_A63"

files=(
  00_START_HERE_EXPERT_MANUAL.md
  01_EXPERT_MAXI_ORDER.md
  02_SOURCE_REGISTRY.json
  03_CONTROL_MATRIX.json
  04_RETURN_SCHEMA.json
  05_INTAKE_FINDINGS.md
  06_MACHINE_CONTRACT.json
  99_SHA256SUMS.txt
  R44_6_EXPERT_ORDER_R0.zip
  R44_6_EXPERT_ORDER_R0.zip.sha256
)
for f in "${files[@]}"; do
  curl --fail --location --max-time 120 --silent --show-error "$BASE/$f" -o "$DEST/$f"
  rc=$?
  echo "FETCH rc=$rc $f"
done

a63files=(
  10_R44_5_R1_ORDER_CHAT_TRANSMISSION_SNAPSHOT_RECEIVER_PUBLISHED.md
  11_R44_5_RECEIVER_CUSTODY_AND_SCOPE_CONTRACT_C1.json
  99_SHA256SUMS_R44_5_RECEIVER_ADDITIVE_20261124.txt
)
for f in "${a63files[@]}"; do
  curl --fail --location --max-time 120 --silent --show-error "$A63/$f" -o "$DEST_A63/$f"
  rc=$?
  echo "FETCH rc=$rc $f"
done
echo "--- SIZES ---"
wc -c "$DEST"/* "$DEST_A63"/* 2>/dev/null
