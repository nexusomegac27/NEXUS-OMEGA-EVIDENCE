PRIVACY_REDACTION_R46_2_R1
==========================
DEFECT =
 Prior public R0 return member 11_ADB_PREFLIGHT.json contained unredacted ADB device serial.

ACTIONS_THIS_BIND =
 1 PRIVATE_ORIGINAL_R0.zip preserved byte-identical under 00_PRIVACY/ (DO_NOT_MUTATE)
 2 EXTRACT_R0 redacted derivative: ADB serial fields → REDACTED (REDACTED_COUNT=2)
 3 Public follow-up return MUST ship redacted ADB preflight only
 4 Encoding: JSON written UTF-8 (no UTF-16-LE pollution)
 5 Git history rewrite = NO_UNILATERAL; propose authorized cleanup path only

PROPOSED_HISTORY_CLEANUP =
 Operator/AXIOM may authorize a separate scoped rewrite or superseding public path
 that replaces leaked serial in published artifacts. Cursor does not rewrite history
 from this bind.

PUBLIC_SERIAL = REDACTED
PRIVATE_LOCUS = 00_PRIVACY/PRIVATE_ORIGINAL_R0/
