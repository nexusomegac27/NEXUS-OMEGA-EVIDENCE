#!/usr/bin/env python3
"""R41 P3 offline metrology: reference angles, mount error, clock map, GUM, MC, common-mode.

Claim ceiling: C1_DESCRIPTIVE_ONLY. No physical device I/O.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent


@dataclass
class MountError:
    roll_deg: float
    pitch_deg: float
    yaw_deg: float

    def as_rotation_matrix(self) -> list[list[float]]:
        # ZYX intrinsic (yaw-pitch-roll) small-angle capable exact form
        r = math.radians(self.roll_deg)
        p = math.radians(self.pitch_deg)
        y = math.radians(self.yaw_deg)
        cr, sr = math.cos(r), math.sin(r)
        cp, sp = math.cos(p), math.sin(p)
        cy, sy = math.cos(y), math.sin(y)
        return [
            [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
            [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
            [-sp, cp * sr, cp * cr],
        ]


def rotate(v: tuple[float, float, float], R: list[list[float]]) -> tuple[float, float, float]:
    return (
        R[0][0] * v[0] + R[0][1] * v[1] + R[0][2] * v[2],
        R[1][0] * v[0] + R[1][1] * v[1] + R[1][2] * v[2],
        R[2][0] * v[0] + R[2][1] * v[1] + R[2][2] * v[2],
    )


def reference_gravity_body(mount: MountError) -> tuple[float, float, float]:
    """Ideal static gravity in body frame after mount misalignment (g=9.80665)."""
    g = (0.0, 0.0, 9.80665)
    return rotate(g, mount.as_rotation_matrix())


def clock_map_elapsed_to_wall(elapsed_ns: int, boot_wall_ns: int) -> int:
    """Map elapsedRealtimeNanos to approximate wall clock ns (offline model)."""
    return boot_wall_ns + elapsed_ns


def gum_combined_std(components: list[tuple[float, float]]) -> float:
    """GUM-style combined standard uncertainty: u_c = sqrt(sum (c_i * u_i)^2)."""
    return math.sqrt(sum((c * u) ** 2 for c, u in components))


def monte_carlo_angle_uncertainty(
    true_deg: float,
    noise_std_deg: float,
    n: int = 5000,
    seed: int = 41,
) -> dict:
    rng = random.Random(seed)
    samples = [true_deg + rng.gauss(0.0, noise_std_deg) for _ in range(n)]
    mean = sum(samples) / n
    var = sum((x - mean) ** 2 for x in samples) / (n - 1)
    return {
        "n": n,
        "seed": seed,
        "true_deg": true_deg,
        "noise_std_deg": noise_std_deg,
        "mean_deg": mean,
        "std_deg": math.sqrt(var),
        "bias_deg": mean - true_deg,
    }


def common_mode_falsifier(
    a: list[float],
    b: list[float],
    corr_threshold: float = 0.98,
) -> dict:
    """Detect excessive common-mode correlation between two channels (falsifier)."""
    if len(a) != len(b) or len(a) < 2:
        return {"status": "INSUFFICIENT", "pearson": None, "flag": False}
    ma = sum(a) / len(a)
    mb = sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    if da == 0.0 or db == 0.0:
        return {"status": "ZERO_VARIANCE", "pearson": None, "flag": True}
    r = num / (da * db)
    return {
        "status": "OK",
        "pearson": r,
        "threshold": corr_threshold,
        "flag": abs(r) >= corr_threshold,
        "interpretation": "COMMON_MODE_SUSPECT" if abs(r) >= corr_threshold else "OK",
    }


def run_suite() -> dict:
    mount = MountError(roll_deg=2.0, pitch_deg=-1.5, yaw_deg=0.5)
    g_body = reference_gravity_body(mount)
    u_c = gum_combined_std([(1.0, 0.05), (1.0, 0.02), (0.5, 0.1)])  # deg components
    mc = monte_carlo_angle_uncertainty(45.0, 0.3, n=2000, seed=41)
    # synthetic common-mode vs independent
    t = list(range(200))
    common = [math.sin(0.1 * i) for i in t]
    noise = [0.01 * math.sin(3.1 * i + 1.0) for i in t]
    a = [c + n for c, n in zip(common, noise)]
    b = [c + 0.005 * math.cos(2.7 * i) for i, c in enumerate(common)]
    indep = [math.cos(0.17 * i) for i in t]
    cm = common_mode_falsifier(a, b)
    cm_ok = common_mode_falsifier(a, indep)

    checks = {
        "mount_rotation_norm_ok": abs(math.sqrt(sum(x * x for x in g_body)) - 9.80665) < 1e-9,
        "gum_positive": u_c > 0,
        "mc_std_near_noise": abs(mc["std_deg"] - 0.3) < 0.05,
        "common_mode_flagged": cm["flag"] is True,
        "independent_not_flagged": cm_ok["flag"] is False,
        "clock_map_monotonic": clock_map_elapsed_to_wall(10, 100) > clock_map_elapsed_to_wall(5, 100),
    }
    hard_fails = [k for k, v in checks.items() if not v]
    return {
        "object": "NEXUS_OMEGA_CURSOR_R41_METROLOGY_OFFLINE_SUITE_20261122_R0",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "physical": "ALT_D_DO_NOT_RUN_ACTIVE",
        "utc": datetime.now(timezone.utc).isoformat(),
        "mount": asdict(mount),
        "gravity_body": {"x": g_body[0], "y": g_body[1], "z": g_body[2]},
        "gum_combined_std_deg": u_c,
        "monte_carlo": mc,
        "common_mode_suspect": cm,
        "common_mode_control": cm_ok,
        "checks": checks,
        "hard_fails": hard_fails,
        "verdict": "PASS" if not hard_fails else "FAIL",
        "epistemic_walls": [
            "OFFLINE_METROLOGY_PASS != PHYSICAL_CALIBRATION",
            "MC_SYNTHETIC != OPPO_SENSOR_CERTIFICATE",
            "GUM_MODEL != EMPIRICAL_UNCERTAINTY",
        ],
    }


def main() -> int:
    receipt = run_suite()
    out = HERE / "METROLOGY_OFFLINE_RECEIPT.json"
    out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    h = hashlib.sha256(out.read_bytes()).hexdigest()
    print(json.dumps({"verdict": receipt["verdict"], "receipt": str(out), "sha256": h}))
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
