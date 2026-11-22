"""R39 independent analytic checks: synthetic fixture only, no hardware or body claims."""
import json
from math import sin, cos, radians, hypot

G = 9.80665
T = 60.0
L = 45.0  # per leg, NOT 90 degrees per leg
BIAS_DPS = 0.05
SCALE = 0.01


def two_leg_observations(leg_deg, bias_dps, scale, total_seconds):
    plus = leg_deg * (1.0 + scale) + bias_dps * total_seconds / 2
    minus = -leg_deg * (1.0 + scale) + bias_dps * total_seconds / 2
    return plus, minus


def solve_two_leg(plus, minus, leg_deg, total_seconds):
    return (plus + minus) / total_seconds, (plus - minus) / (2 * leg_deg) - 1.0


def pure_roll_atan2_gradient_norm(angle_deg):
    ay = G * sin(radians(angle_deg))
    az = -G * cos(radians(angle_deg))
    denom = ay * ay + az * az
    return hypot(-az / denom, ay / denom)


def main():
    plus, minus = two_leg_observations(L, BIAS_DPS, SCALE, T)
    b, s = solve_two_leg(plus, minus, L, T)
    assert abs(plus - 46.95) < 1e-11
    assert abs(minus + 43.95) < 1e-11
    assert abs(b - BIAS_DPS) < 1e-12
    assert abs(s - SCALE) < 1e-12
    wrong_scale = (plus - minus) / L - 1.0  # legacy narrative denominator error
    assert abs(wrong_scale - 1.02) < 1e-12
    gradients = {str(a): pure_roll_atan2_gradient_norm(a) for a in (0, 45, 90)}
    assert all(abs(v - 1.0 / G) < 1e-13 for v in gradients.values())
    # After subtracting a correct static bias, a second estimate is RESIDUAL bias.
    residual_bias = (BIAS_DPS - BIAS_DPS)
    assert abs(residual_bias) < 1e-14
    # Correct half-window integration in synthetic sampled rate, no cumsum slicing loss.
    fs, n = 100, 6000
    omega = [L / (T / 2) * (1 + SCALE) + BIAS_DPS] * (n // 2)
    omega += [-L / (T / 2) * (1 + SCALE) + BIAS_DPS] * (n // 2)
    a1 = sum(omega[: n // 2]) / fs
    a2 = sum(omega[n // 2 :]) / fs
    assert abs(a1 - plus) < 1e-9 and abs(a2 - minus) < 1e-9
    print(json.dumps({"status": "PASS_SYNTHETIC_ANALYTIC_ONLY", "leg_angle_deg": L,
                      "A_plus_deg": plus, "A_minus_deg": minus,
                      "bias_dps": b, "scale": s, "wrong_narrative_scale": wrong_scale,
                      "atan2_gradient_norm_per_deg": gradients,
                      "residual_bias_dps": residual_bias,
                      "equal_half_window_integration_deg": [a1, a2],
                      "body_measured": False, "device_run": False}, sort_keys=True))


if __name__ == "__main__":
    main()
