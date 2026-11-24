#!/usr/bin/env bash
# R44-6 SOURCE_RECEIVER_PREFLIGHT — pinned-commit raw downloads (TRANSFER_POLICY = GITHUB_ONLY)
# Route per 00_START_HERE_EXPERT_MANUAL.md step 1-2: raw.githubusercontent at FULL_COMMIT, no branch tips.
set -u
OWNER=nexusomegac27
REPO=NEXUS-OMEGA-EVIDENCE
COMMIT=89ccff827d564309cba3274bff94a6d577e6853a
BASE="https://raw.githubusercontent.com/${OWNER}/${REPO}/${COMMIT}"
SUBDIR="research/r44/r44-6-github-source-access-and-bodytwin-20261124"
OUT=/home/z/my-project/scripts/r44_6_preflight/fetched
mkdir -p "${OUT}/order"
RECEIPT="${OUT}/fetch_receipt.txt"
: > "${RECEIPT}"

fetch() {
  url="$1"; out="$2"
  rm -f "${out}"
  code=$(curl -sS -L --max-time 60 -w '%{http_code}' -o "${out}" "${url}" 2>"${OUT}/curl_err_$(basename "${out}").log")
  rc=$?
  bytes=$(stat -c %s "${out}" 2>/dev/null || printf '0')
  sha=$(sha256sum "${out}" 2>/dev/null | awk '{print $1}')
  printf 'rc=%s http=%s bytes=%s sha256=%s file=%s\n     url=%s\n' "${rc}" "${code}" "${bytes}" "${sha}" "$(basename "${out}")" "${url}" >> "${RECEIPT}"
}

# Order package at pinned commit
fetch "${BASE}/${SUBDIR}/R44_6_EXPERT_ORDER_R0.zip"        "${OUT}/order/R44_6_EXPERT_ORDER_R0.zip"
fetch "${BASE}/${SUBDIR}/R44_6_EXPERT_ORDER_R0.zip.sha256" "${OUT}/order/R44_6_EXPERT_ORDER_R0.zip.sha256"
for f in 00_START_HERE_EXPERT_MANUAL.md 01_EXPERT_MAXI_ORDER.md 02_SOURCE_REGISTRY.json \
         03_CONTROL_MATRIX.json 04_RETURN_SCHEMA.json 05_INTAKE_FINDINGS.md \
         06_MACHINE_CONTRACT.json 99_SHA256SUMS.txt; do
  fetch "${BASE}/${SUBDIR}/${f}" "${OUT}/order/${f}"
done

echo "=== fetch_receipt ==="
cat "${RECEIPT}"
