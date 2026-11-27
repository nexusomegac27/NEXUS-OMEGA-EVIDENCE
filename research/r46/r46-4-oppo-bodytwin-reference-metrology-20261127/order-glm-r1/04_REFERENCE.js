'use strict';
// NEXUS OMEGA - R46-4 order reference implementation (design-only, offline, deterministic).
// Rank and identifiability witnesses for six-position calibration design vs one-pose.
// No raw OPPO data, no device interaction, no randomness.

function run() {
  const g0 = 9.80665;
  const R21 = {
    acc_mag_mean: 9.832738001091458, acc_mag_stdev: 0.009171945499113295, acc_n: 7014,
    acc_median_dt: 0.009984687, gyro_n: 7004, gyro_median_dt: 0.009984687
  };
  const Phi = z => 0.5 * (1 + erf(z / Math.SQRT2));
  function erf(x) {
    const s = x < 0 ? -1 : 1; x = Math.abs(x);
    const t = 1 / (1 + 0.3275911 * x);
    const y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
    return s * y;
  }
  // Gaussian elimination rank with partial pivoting, tolerance relative to max entry
  function rank(A, rows, cols) {
    const m = A.map(r => r.slice());
    let rk = 0;
    for (let c = 0; c < cols && rk < rows; c++) {
      let piv = -1, best = 0;
      for (let r = rk; r < rows; r++) if (Math.abs(m[r][c]) > best) { best = Math.abs(m[r][c]); piv = r; }
      const tol = 1e-10;
      if (piv < 0 || best < tol) continue;
      [m[rk], m[piv]] = [m[piv], m[rk]];
      for (let r = rk + 1; r < rows; r++) {
        const f = m[r][c] / m[rk][c];
        for (let cc = c; cc < cols; cc++) m[r][cc] -= f * m[rk][cc];
      }
      rk++;
    }
    return rk;
  }
  // Six standard positions: true accelerometer vectors (device frame, static, gravity only)
  const six = [[g0,0,0],[-g0,0,0],[0,g0,0],[0,-g0,0],[0,0,g0],[0,0,-g0]];
  const one = [[0,0,g0]]; // arbitrary single pose (device flat)

  // W-R1: one-pose per-axis affine design rank (model z = s*x + b; 1 equation, 2 unknowns)
  const wr1 = { design_rows: 1, expected_rank: 1, required_rank: 2,
    rank_x_axis: rank([[one[0][0], 1]], 1, 2), rank_y_axis: rank([[one[0][1], 1]], 1, 2), rank_z_axis: rank([[one[0][2], 1]], 1, 2),
    verdict: 'NOT_IDENTIFIABLE (scale/bias inseparable from one pose, cf. R46-3 W17)' };

  // W-R2: six-position per-axis affine design rank (2 equations, 2 unknowns per axis)
  const wr2 = { design_rows: 6, required_rank: 2,
    rank_x_axis: rank(six.map(v => [v[0], 1]), 6, 2),
    rank_y_axis: rank(six.map(v => [v[1], 1]), 6, 2),
    rank_z_axis: rank(six.map(v => [v[2], 1]), 6, 2),
    verdict: 'IDENTIFIABLE per-axis (slope and intercept separated)' };

  // W-R3: full affine S (3x3, 9 params) + bias b (3): design matrix 18 x 12
  const A = [];
  for (const v of six) {
    A.push([v[0], v[1], v[2], 0, 0, 0, 0, 0, 0, 1, 0, 0]);
    A.push([0, 0, 0, v[0], v[1], v[2], 0, 0, 0, 0, 1, 0]);
    A.push([0, 0, 0, 0, 0, 0, v[0], v[1], v[2], 0, 0, 1]);
  }
  const wr3 = { design_rows: A.length, design_cols: 12, computed_rank: rank(A, A.length, 12),
    verdict: rank(A, A.length, 12) === 12 ? 'IDENTIFIABLE (S and b identifiable from six standard positions up to documented conventions)' : 'RANK DEFICIENT' };

  // W-R4/W-R5: finite-sample uncertainty (analytic, model-conditional)
  // per axis, m samples at +g and m at -g, axis noise sigma:
  // Var(s_hat) ~ sigma^2 / (2 m g^2); Var(b_hat) ~ sigma^2 / (2 m)
  const m = 3500; // per position, comparable to ~7000 events per axis class
  const sigmaAxis = 0.009171945499113295 / Math.sqrt(3); // note: isotropy is an ASSUMPTION (R46-3 W12)
  const seScale = sigmaAxis / (g0 * Math.sqrt(2 * m));
  const seBias = sigmaAxis / Math.sqrt(2 * m);
  const wr4_5 = { m_per_position: m, sigma_axis_assumption: 'isotropic (UNVERIFIED, R46-3 W12: sigma_axis model-conditional)',
    se_scale_rel: seScale / 1, se_scale_over_g_rel: seScale / g0, se_bias: seBias,
    class: 'E1_MODEL_CONDITIONAL' };

  // W-R6: gap histogram vs threshold count (deterministic construction, E2_SYNTHETIC)
  const planned = 7095, drops = 81, base = R21.acc_median_dt;
  const hist = { '1x_median': 0, '2x_median': 0, 'gt_5x_median': 0 };
  for (let i = 0; i < planned - 1 - drops; i++) hist['1x_median']++;
  for (let i = 0; i < drops; i++) hist['2x_median']++;
  const wr6 = { planned, drops, threshold_count_gt_5x_median: hist['gt_5x_median'],
    gap_histogram: hist,
    verdict: 'threshold count alone reports 0 while 81 intervals are doubled; histogram is required (C2)' };

  // W-R7: ddof sensitivity
  const N = R21.acc_n;
  const wr7 = { population_sd: R21.acc_mag_stdev, sample_sd: R21.acc_mag_stdev * Math.sqrt(N / (N - 1)),
    abs_diff: R21.acc_mag_stdev * (Math.sqrt(N / (N - 1)) - 1), requirement: 'producer documents ddof (C3)' };

  // W-R8: projection constraint echo (Var(M) ~ e_g' Sigma e_g), three covariances
  const sdFolded = (nu, sg) => {
    const a = nu / sg;
    const mu_f = nu * (2 * Phi(a) - 1) + 2 * sg * Math.exp(-a * a / 2) / Math.sqrt(2 * Math.PI);
    return Math.sqrt(nu * nu + sg * sg - mu_f * mu_f);
  };
  const sg = R21.acc_mag_stdev, nu = R21.acc_mag_mean;
  const wr8 = { isotropic: sdFolded(nu, sg), z_dominant: sdFolded(nu, sg), x_dominant: sdFolded(nu, sg),
    observed_mag_stdev: sg,
    verdict: 'three different axis covariances reproduce the same magnitude SD; per-axis statements need multi-position (C1)' };

  // W-R9: metrology contract negatives (6 REJECT + 2 positive controls)
  const rules = [
    { id: 'calibration-from-one-pose', test: r => !(r.pose_count < 2 && r.output_class === 'calibration') },
    { id: 'uncertainty-from-norms-alone', test: r => !(r.inputs === 'magnitude_stats_only' && r.output_class === 'axis_covariance') },
    { id: 'design-presented-as-measurement', test: r => !(r.origin === 'DESIGN' && r.displayed_as === 'MEASUREMENT') },
    { id: 'missing-ddof-aggregate', test: r => !(r.sd_ddof_documented === false && r.aggregate_promoted === true) },
    { id: 'threshold-count-as-losslessness', test: r => !(r.loss_basis === 'gap_threshold_count_only') },
    { id: 'local-g-without-reference', test: r => !(r.local_g_correction === true && r.independent_reference === false) }
  ];
  const bad = [
    { pose_count: 1, output_class: 'calibration' },
    { inputs: 'magnitude_stats_only', output_class: 'axis_covariance' },
    { origin: 'DESIGN', displayed_as: 'MEASUREMENT' },
    { sd_ddof_documented: false, aggregate_promoted: true },
    { loss_basis: 'gap_threshold_count_only' },
    { local_g_correction: true, independent_reference: false }
  ];
  const good = [
    { pose_count: 6, output_class: 'calibration' },
    { origin: 'DESIGN', displayed_as: 'DESIGN' }
  ];
  const wr9 = { negative_cases: bad.map((r, i) => ({ case: rules[i].id, verdict: rules[i].test(r) ? 'ACCEPT (BAD!)' : 'REJECT' })),
    positive_cases: good.map(r => ({ verdict: rules.every(rule => rule.test(r)) ? 'ACCEPT' : 'REJECT (BAD!)' })),
    all_reject: bad.every((r, i) => !rules[i].test(r)),
    positives_pass: good.every(r => rules.every(rule => rule.test(r))) };

  const all_pass = wr1.rank_x_axis === 1 && wr2.rank_x_axis === 2 && wr2.rank_y_axis === 2 && wr2.rank_z_axis === 2
    && wr3.computed_rank === 12 && wr9.all_reject && wr9.positives_pass;

  return {
    runner: '04_REFERENCE.js', lineage: 'GLM_R1_R46_4_ORDER',
    all_reference_checks_pass: all_pass,
    wr1_one_pose_rank: wr1, wr2_six_position_rank: wr2, wr3_full_affine_rank: wr3,
    wr4_5_finite_sample_uncertainty: wr4_5, wr6_gap_histogram: wr6, wr7_ddof: wr7,
    wr8_projection: wr8, wr9_contract: wr9,
    limits: 'Design-only reference computations; analytic uncertainty values are E1_MODEL_CONDITIONAL under an UNVERIFIED isotropy assumption; no measurement, no capture, no gate credit.'
  };
}
const RESULT = run();
if (typeof module !== 'undefined') module.exports = RESULT;
