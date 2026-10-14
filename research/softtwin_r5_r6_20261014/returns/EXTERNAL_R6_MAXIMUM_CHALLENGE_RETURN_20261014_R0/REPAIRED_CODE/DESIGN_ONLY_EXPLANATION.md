# REPAIRED_CODE — DESIGN_ONLY_EXPLANATION (V0.1 -> V0.2)

**Status: DESIGNED + STATIC_PROVED. Runtime NOT_EXECUTED in this return (no Python interpreter in the external research environment).** All runtime claims are deferred to the delivered fixtures under an authorized Python/POSIX session. Historical R0 files untouched (order 0.5).

## Before/after delta (source-exact)

1. ROOT INTERMEDIATE SYMLINK (new counterexample S10b, STATIC_PROVED):
   - Before (V0.1): root checked with root.is_symlink() (final component only) and opened by full path; POSIX O_NOFOLLOW applies only to the final path component, so intermediate symlink components of the approved root are followed; the base FD can anchor outside the operator-approved root while target.relative_to(root) passes lexically.
   - After (V0.2): _open_root_fd() opens "/" then every root component with O_NOFOLLOW|O_DIRECTORY anchored to the previous component FD; any symlink component (intermediate or final) raises ELOOP -> Denied("ROOT_UNAVAILABLE_OR_SYMLINK") (message kept compatible with the existing delta test d18). Net-new protective behavior: the anchored base FD is now guaranteed to be the exact operator-approved directory even when ancestors are attacker-writable.
2. ZIP LOCAL DATA REGION BOUND (new gap S26, STATIC_PROVED):
   - Before (V0.1): local header end checked; declared compressed data region never bounded; local CRC/sizes not crosschecked without data descriptor.
   - After (V0.2): data_end = local header end + central compress_size must be <= captured bytes, else Denied("ZIP_LOCAL_DATA_REGION_OUT_OF_BOUNDS"); when flag bit 3 absent, local crc/comp_size/uncomp_size must equal central values (same failure label as existing mismatch tests). Net-new protective behavior: inflated declarations and local/central size divergence are rejected in metadata triage.
3. HARDLINK WITNESS (S09, documented behavior):
   - Before: silent acceptance.
   - After: st_nlink > 1 appends HARDLINK_WITNESS_NLINK_<n> to unresolved; no denial (name-based containment cannot and should not guess link semantics), but the record no longer hides the condition.

## Compatibility with the 42 existing tests (static reasoning)

- Root-symlink denial message preserved ("ROOT_UNAVAILABLE_OR_SYMLINK") so d18 passes.
- All other deny messages and JSON fields preserved; schema string bumped to V0_2.
- Known intentional behavior change: V0.1 accepted roots whose path contains intermediate symlinks; V0.2 denies them. On symlink-free temp roots (Linux /tmp as a real directory) all 42 tests are expected to pass unchanged; on systems where the test temp path contains symlink components (e.g. macOS /tmp -> private/tmp) V0.2 fails closed BY DESIGN; run the suite from a symlink-free base.
- d13 interceptor pattern (os.open with dir_fd and path=='a.bin') is unaffected by the added root-component opens.

## Limitations (explicit)

- No atomic snapshot against hostile in-place writers (order S5): before/after fstat incl. ctime_ns detects concurrent modification on Linux (ctime is not user-settable), but this is detection, not atomicity; immutable blob or filesystem snapshot semantics remain required for stronger claims.
- POSIX/Linux research candidate only; no Windows native handle validation (S3 fixtures NOT_EXECUTED).
- V0.2 runtime execution, including the 22 compat + 20 delta + 11 new fixtures, is pending an authorized Python >= 3.10 POSIX session; nothing here claims a PASS that was not run.
