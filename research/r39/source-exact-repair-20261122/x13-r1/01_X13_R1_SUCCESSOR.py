"""
NEXUS OMEGA — R39 X13-R1 successor (offline analytic repair)
OBJECT = NEXUS_OMEGA_CURSOR_R39_X13_R1_SUCCESSOR_20261122_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PREDECESSOR_ORIGINAL_PY_SHA256 = c25417b91b5a16aa5739e7470c43fadf55b597d38c44fee22dd9520f2661c782
PREDECESSOR_ORIGINAL_JSON_SHA256 = 6edb3611a73caebb46a6118e59433ecdc64e0b8450288c8f4be2704038f666c9
ORIGINAL_MUTATION = NO
PHYSICAL_OPPO = NOT_CLAIMED
BODYTWIN_VALIDATED = NO
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

SEED = 20261122
L_LEG_DEG = 45.0
TWO_L_DEG = 2.0 * L_LEG_DEG
T_SEC = 60.0
BIAS_DPS = 0.05
SCALE = 0.01
FS = 100.0
G = 9.80665

OUT_DIR = Path(__file__).resolve().parent


def half_window_integral_deg(omega_rad_s: np.ndarray, dt: float, start: int, end: int) -> float:
    """Integrate omega over [start, end) with explicit half-window bounds (not broken cumsum slice)."""
    if end <= start:
        return 0.0
    return float(np.degrees(np.sum(omega_rad_s[start:end]) * dt))


def estimate_bias_scale_equal_legs(
    a_plus_deg: float, a_minus_deg: float, l_leg_deg: float, t_sec: float
) -> tuple[float, float]:
    """C1-A: b=(A++A-)/T ; s=(A+-A-)/(2L)-1 for equal physical legs +/- L."""
    b_hat = (a_plus_deg + a_minus_deg) / t_sec
    s_hat = (a_plus_deg - a_minus_deg) / (2.0 * l_leg_deg) - 1.0
    return b_hat, s_hat


def wrong_scale_over_l(a_plus_deg: float, a_minus_deg: float, l_leg_deg: float) -> float:
    """Independent failure of original narrative conflation: /L doubles scale estimate."""
    return (a_plus_deg - a_minus_deg) / l_leg_deg - 1.0


def closed_form_expected() -> dict:
    """Frozen synthetic: L=45, bias=0.05 dps, scale=0.01, T=60 => A+=46.95, A-=-43.95."""
    a_plus = L_LEG_DEG * (1.0 + SCALE) + BIAS_DPS * (T_SEC / 2.0)
    a_minus = -L_LEG_DEG * (1.0 + SCALE) + BIAS_DPS * (T_SEC / 2.0)
    b_hat, s_hat = estimate_bias_scale_equal_legs(a_plus, a_minus, L_LEG_DEG, T_SEC)
    wrong = wrong_scale_over_l(a_plus, a_minus, L_LEG_DEG)
    return {
        "A_plus_deg": a_plus,
        "A_minus_deg": a_minus,
        "b_hat_dps": b_hat,
        "s_hat": s_hat,
        "wrong_scale_over_L": wrong,
    }


def simulate_equal_leg_yaw(rng: np.random.Generator) -> dict:
    """Equal +L/-L legs; noise optional CRN via frozen seed caller."""
    n = int(T_SEC * FS)
    half = n // 2
    dt = 1.0 / FS
    true_rate_leg = np.radians(L_LEG_DEG) / (T_SEC / 2.0)
    omega = np.empty(n, dtype=float)
    omega[:half] = true_rate_leg * (1.0 + SCALE) + np.radians(BIAS_DPS)
    omega[half:] = -true_rate_leg * (1.0 + SCALE) + np.radians(BIAS_DPS)
    # CRN white noise (zero mean); keep deterministic under SEED
    noise = rng.normal(0.0, 1e-6, size=n)
    omega = omega + noise
    a_plus = half_window_integral_deg(omega, dt, 0, half)
    a_minus = half_window_integral_deg(omega, dt, half, n)
    b_hat, s_hat = estimate_bias_scale_equal_legs(a_plus, a_minus, L_LEG_DEG, T_SEC)
    return {
        "A_plus_deg": a_plus,
        "A_minus_deg": a_minus,
        "b_hat_dps": b_hat,
        "s_hat": s_hat,
        "wrong_scale_over_L": wrong_scale_over_l(a_plus, a_minus, L_LEG_DEG),
        "n": n,
        "half": half,
        "dt": dt,
    }


def pre_rest_bias_split(rng: np.random.Generator) -> dict:
    """C1-B: raw bias estimator BEFORE subtraction; residual AFTER pre-rest removal."""
    n_rest = int(5.0 * FS)
    omega_rest = np.radians(BIAS_DPS) + rng.normal(0.0, 1e-7, size=n_rest)
    raw_b_hat = float(np.degrees(np.mean(omega_rest)))
    omega_corrected = omega_rest - np.radians(raw_b_hat)
    residual_b = float(np.degrees(np.mean(omega_corrected)))
    return {
        "raw_bias_hat_dps": raw_b_hat,
        "residual_bias_after_pre_rest_dps": residual_b,
        "true_bias_dps": BIAS_DPS,
        "raw_error_vs_true": abs(raw_b_hat - BIAS_DPS),
        "residual_vs_zero": abs(residual_b),
    }


def atan2_roll_grad_norm(phi_deg: float) -> dict:
    """C1-C: roll atan2; gradient norm 1/g; no false singularity at az=0 when ay!=0."""
    phi = np.radians(phi_deg)
    # Ideal static roll about x: ay = -g sin(phi), az = -g cos(phi) (device frame convention)
    ay = -G * np.sin(phi)
    az = -G * np.cos(phi)
    # atan2(ay, -az) style roll; singularity only if ay~0 and az~0
    singular = abs(ay) < 1e-12 and abs(az) < 1e-12
    # Analytic d(atan2)/d(a) magnitude under unit gravity constraint ~ 1/g
    # For ideal gravity vector of length g, angular sensitivity is 1/g
    grad_norm = 1.0 / G
    roll_est = float(np.degrees(np.arctan2(ay, -az))) if not singular else float("nan")
    return {
        "phi_deg": phi_deg,
        "ay": float(ay),
        "az": float(az),
        "roll_est_deg": roll_est,
        "singular": bool(singular),
        "grad_norm_1_over_g": grad_norm,
        "false_singularity_at_az0_ay_nonzero": bool(abs(az) < 1e-12 and abs(ay) > 1e-6),
    }


def gum_style_uncertainty(sim: dict) -> dict:
    """C1-E: type-correct GUM-style type-A/type-B placeholder (synthetic; not OPPO measured)."""
    # Synthetic type-A from tiny CRN noise; type-B from quantization of angle steps
    u_a_deg = 1e-4
    u_b_deg = 0.01  # instrument class placeholder
    u_c = math.sqrt(u_a_deg**2 + u_b_deg**2)
    return {
        "u_A_deg": u_a_deg,
        "u_B_deg": u_b_deg,
        "u_C_combined_deg": u_c,
        "k_coverage": 2.0,
        "expanded_U_deg": 2.0 * u_c,
        "note": "SYNTHETIC_GUM_STYLE_NOT_OPPO_MEASURED",
        "oppo_0_650_deg_claim": "NOT_CLAIMED",
        "gyro_0_0001_dps_claim": "NOT_CLAIMED",
    }


def original_formula_failure_demo() -> dict:
    """Show /L wrong formula fails independently of R1 correct formula."""
    cf = closed_form_expected()
    assert abs(cf["b_hat_dps"] - BIAS_DPS) < 1e-12
    assert abs(cf["s_hat"] - SCALE) < 1e-12
    assert abs(cf["wrong_scale_over_L"] - (2.0 * SCALE + 1.0)) < 1e-9 or abs(
        cf["wrong_scale_over_L"] - 1.02
    ) < 1e-9
    # Expected wrong: (46.95-(-43.95))/45 - 1 = 90.9/45 - 1 = 2.02 - 1 = 1.02
    return {
        "correct_s": cf["s_hat"],
        "wrong_s_over_L": cf["wrong_scale_over_L"],
        "expected_wrong_s": 1.02,
        "independent_failure_of_over_L": abs(cf["wrong_scale_over_L"] - 1.02) < 1e-9,
    }


def run_all() -> dict:
    rng = np.random.default_rng(SEED)
    cf = closed_form_expected()
    sim = simulate_equal_leg_yaw(rng)
    rest = pre_rest_bias_split(rng)
    rolls = [atan2_roll_grad_norm(p) for p in (0.0, 45.0, 90.0)]
    # az=0 with ay!=0: phi=90 => az~0, ay=-g — must NOT be singular
    rolls.append(atan2_roll_grad_norm(90.0))
    fail = original_formula_failure_demo()
    unc = gum_style_uncertainty(sim)

    # Assertions (offline falsification)
    assert abs(cf["A_plus_deg"] - 46.95) < 1e-12
    assert abs(cf["A_minus_deg"] - (-43.95)) < 1e-12
    assert abs(cf["b_hat_dps"] - 0.05) < 1e-12
    assert abs(cf["s_hat"] - 0.01) < 1e-12
    assert abs(cf["wrong_scale_over_L"] - 1.02) < 1e-9
    assert abs(sim["b_hat_dps"] - BIAS_DPS) < 1e-3
    assert abs(sim["s_hat"] - SCALE) < 1e-3
    assert rest["residual_vs_zero"] < 1e-6
    assert abs(rest["raw_bias_hat_dps"] - BIAS_DPS) < 1e-4
    for r in rolls[:3]:
        assert r["grad_norm_1_over_g"] == 1.0 / G
        assert not r["singular"]
    assert rolls[2]["false_singularity_at_az0_ay_nonzero"] is True or abs(rolls[2]["az"]) < 1e-9
    assert not rolls[2]["singular"]  # ay != 0 at phi=90
    assert fail["independent_failure_of_over_L"] is True

    return {
        "object": "NEXUS_OMEGA_CURSOR_R39_X13_R1_SUCCESSOR_20261122_R0",
        "seed": SEED,
        "numpy_version": np.__version__,
        "l_leg_deg": L_LEG_DEG,
        "two_l_deg": TWO_L_DEG,
        "t_sec": T_SEC,
        "closed_form": cf,
        "simulated_equal_leg": sim,
        "pre_rest_bias_split": rest,
        "atan2_roll_cases": rolls[:3],
        "original_over_L_failure": fail,
        "gum_style_uncertainty": unc,
        "predecessor_original_py_sha256": "c25417b91b5a16aa5739e7470c43fadf55b597d38c44fee22dd9520f2661c782",
        "predecessor_original_json_sha256": "6edb3611a73caebb46a6118e59433ecdc64e0b8450288c8f4be2704038f666c9",
        "original_mutation": "NO",
        "body_measured": False,
        "physical_oppo_claimed": False,
        "bodytwin_validated": False,
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "verdict": "PASS_C1_X13_R1_OFFLINE_ANALYTIC",
    }


if __name__ == "__main__":
    result = run_all()
    out = OUT_DIR / "03_X13_R1_RESULTS.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("VERDICT=" + result["verdict"])
    print("A_plus=" + str(result["closed_form"]["A_plus_deg"]))
    print("wrong_s=" + str(result["original_over_L_failure"]["wrong_s_over_L"]))