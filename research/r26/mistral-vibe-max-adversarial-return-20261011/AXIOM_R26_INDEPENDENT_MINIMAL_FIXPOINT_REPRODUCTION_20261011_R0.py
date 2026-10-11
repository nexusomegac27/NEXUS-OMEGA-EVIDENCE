#!/usr/bin/env python3
"""Independent C1 analytical spot-check of the reported NA-1 five-unit active-arc equilibria.

Research only; NO NF05/NF06 confirmatory trials and no authorization of any runtime.
Assumptions: N=32; W_ij=[(1+cos(theta_i-theta_j))/2]^k; k=8;
zero input/noise; ReLU; discrete map r_next=relu(W@r-g*P(r)).
Only locally fixed active-arc Jacobians are computed (valid for strict
inactive inequalities and unique MAX peak). No global basin or noise proof.
Requires Python 3 + numpy. Independently checked using Python 3.13.5, numpy 2.3.5.
"""
import numpy as np

N, K, L = 32, 8, 5
th = 2 * np.pi * np.arange(N) / N
W = ((1 + np.cos(th[:, None] - th[None, :])) / 2) ** K
A = np.array([N - 2, N - 1, 0, 1, 2])
inactive = np.setdiff1d(np.arange(N), A)
WA = W[np.ix_(A, A)]
v = np.linalg.solve(np.eye(L) - WA, np.ones(L))
gains = {"MAX": -1 / v[2], "SUM": -1 / v.sum()}
out = {}

for arm, g in gains.items():
    state = np.zeros(N)
    state[A] = -g * v
    activity = np.max(state) if arm == "MAX" else state.sum()
    drive = W @ state - g * activity
    next_state = np.maximum(drive, 0)
    if arm == "MAX":
        J = WA - g * np.ones((L, 1)) @ np.eye(L)[2:3, :]
    else:
        J = WA - g * np.ones((L, L))
    eigenvalues = np.linalg.eigvals(J)
    # One radial eigenvalue is 1 in each homogeneous case.
    radial_index = np.argmin(np.abs(eigenvalues - 1))
    nonradial = np.delete(eigenvalues, radial_index)
    out[arm] = {
        "g": float(g),
        "residual_inf": float(np.linalg.norm(next_state - state, np.inf)),
        "largest_nonradial_abs_eig": float(np.max(np.abs(nonradial))),
        "radial_abs_eig": float(np.abs(eigenvalues[radial_index])),
        "inactive_drive_max": float(np.max(drive[inactive])),
    }
    assert out[arm]["residual_inf"] < 1e-12
    assert out[arm]["inactive_drive_max"] < -1e-4

uniform_row_sum = float(W.sum(axis=1)[0])
uniform_max_gain_factor = uniform_row_sum - gains["MAX"]
assert np.isclose(out["MAX"]["g"], 1.9807280461434622, atol=1e-10)
assert np.isclose(out["SUM"]["g"], 0.6050068144805235, atol=1e-10)
assert np.isclose(out["MAX"]["largest_nonradial_abs_eig"], 1.0377893000491, atol=1e-9)
assert np.isclose(out["SUM"]["largest_nonradial_abs_eig"], 0.9792479, atol=1e-6)
assert np.isclose(uniform_max_gain_factor, 4.303451641356537, atol=1e-9)
print("Independent exact-model active-arc spot-check: PASS")
for name, data in out.items():
    print(name, data)
print("W row sum:", uniform_row_sum)
print("MAX uniform-state multiplicative factor:", uniform_max_gain_factor)
print("REVIEW LIMIT: no source code or trajectory raw logs for claimed two-peak dynamics")
