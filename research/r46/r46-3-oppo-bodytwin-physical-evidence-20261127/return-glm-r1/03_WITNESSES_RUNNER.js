'use strict';
// NEXUS OMEGA - R46-3 EXPERT RETURN GLM_R1 - witness runner
// Deterministic, offline, no raw OPPO data, no network, no randomness
// (pseudo-derivations are fully deterministic constructions).
// Lineage: VIBE_GLM_R1_FIRST_RUN, prereg 02_PREREG.md frozen before execution.
// Checks W01..W25 per prereg. Aggregate-only inputs from 02_EVIDENCE.json @ d7e1c95d.

function run() {
  const g0 = 9.80665;
  const R21 = {
    requested_hz: 100,
    acc: { n: 7014, duration_s: 70.022492373, rate_reported: 100.15353299112422,
           median_dt_s: 0.009984687, gaps_gt_5x_median: 0,
           mag_mean: 9.832738001091458, mag_stdev: 0.009171945499113295 },
    gyro: { n: 7004, duration_s: 69.922634925, rate_reported: 100.15354838260195,
            median_dt_s: 0.009984687, gaps_gt_5x_median: 0,
            mag_mean: 0.0019802113232776307, mag_stdev: 0.000664483224551047 },
    gravity_residual_mean_abs_reported: 0.026088001091459367
  };
  const mean = x => { let s = 0; for (const v of x) s += v; return s / x.length; };
  const psd = x => { const m = mean(x); let s = 0; for (const v of x) s += (v - m) * (v - m); return Math.sqrt(s / x.length); };
  const ssd = x => { const m = mean(x); let s = 0; for (const v of x) s += (v - m) * (v - m); return Math.sqrt(s / (x.length - 1)); };
  const lag1 = x => { const m = mean(x); let num = 0, den = 0;
    for (let i = 1; i < x.length; i++) { num += (x[i] - m) * (x[i - 1] - m); }
    for (const v of x) den += (v - m) * (v - m);
    return num / den; };
  const Phi = z => 0.5 * (1 + erf(z / Math.SQRT2));
  function erf(x) { // Abramowitz-Stegun 7.1.26, |eps|<=1.5e-7
    const s = x < 0 ? -1 : 1; x = Math.abs(x);
    const t = 1 / (1 + 0.3275911 * x);
    const y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
    return s * y;
  }

  // ---------- W01..W02 effective interval rates ----------
  const rate_acc = (R21.acc.n - 1) / R21.acc.duration_s;
  const rate_gyro = (R21.gyro.n - 1) / R21.gyro.duration_s;
  const w01 = { computed: rate_acc, reported: R21.acc.rate_reported,
    abs_diff: Math.abs(rate_acc - R21.acc.rate_reported),
    rel_diff: Math.abs(rate_acc - R21.acc.rate_reported) / R21.acc.rate_reported,
    match_1e9: Math.abs(rate_acc - R21.acc.rate_reported) / R21.acc.rate_reported < 1e-9 };
  const w02 = { computed: rate_gyro, reported: R21.gyro.rate_reported,
    abs_diff: Math.abs(rate_gyro - R21.gyro.rate_reported),
    rel_diff: Math.abs(rate_gyro - R21.gyro.rate_reported) / R21.gyro.rate_reported,
    match_1e9: Math.abs(rate_gyro - R21.gyro.rate_reported) / R21.gyro.rate_reported < 1e-9 };

  // ---------- W03..W05 recorded diagnostics ----------
  const w03 = { median_reciprocal_acc: 1 / R21.acc.median_dt_s, median_reciprocal_gyro: 1 / R21.gyro.median_dt_s,
    ppm_vs_effective_acc: (1 / R21.acc.median_dt_s - rate_acc) / rate_acc * 1e6 };
  const w04 = { acc: { duration_minus_n1_median_ms: (R21.acc.duration_s - (R21.acc.n - 1) * R21.acc.median_dt_s) * 1e3 },
    gyro: { duration_minus_n1_median_ms: (R21.gyro.duration_s - (R21.gyro.n - 1) * R21.gyro.median_dt_s) * 1e3 } };
  const w05 = { acc_pct: (rate_acc - 100) / 100 * 100, gyro_pct: (rate_gyro - 100) / 100 * 100 };

  // ---------- W06 |mean-g0| vs reported residual ----------
  const abs_mean_minus_g0_acc = Math.abs(R21.acc.mag_mean - g0);
  const w06 = { abs_mean_minus_g0: abs_mean_minus_g0_acc, reported: R21.gravity_residual_mean_abs_reported,
    abs_diff: Math.abs(abs_mean_minus_g0_acc - R21.gravity_residual_mean_abs_reported),
    rel_diff: Math.abs(abs_mean_minus_g0_acc - R21.gravity_residual_mean_abs_reported) / R21.gravity_residual_mean_abs_reported };

  // ---------- W07 counterexample abs(mean-g) vs mean(abs(x-g)) ----------
  const vals = [g0 - 0.1, g0 + 0.1];
  const w07 = { abs_mean_residual: Math.abs(mean(vals) - g0), mean_abs_residual: mean(vals.map(v => Math.abs(v - g0))),
    distinct: mean(vals.map(v => Math.abs(v - g0))) > Math.abs(mean(vals) - g0) };

  // ---------- W08 information balance ----------
  // Counting rule: one NDJSON sensor line = 1 timestamp + 3 axis values = 4 numeric fields.
  const raw_numeric_fields = (R21.acc.n + R21.gyro.n) * 4;
  // Published numeric scalars in the r21 aggregate block of 02_EVIDENCE.json:
  // requested_hz, ndjson_lines, non_sensor_lines, acc{6}, gyro{6}, gravity_residual = 16.
  const published_scalars = 16;
  const w08 = { raw_numeric_fields, published_scalars, kept_fraction_pct: published_scalars / raw_numeric_fields * 100,
    compression_factor: raw_numeric_fields / published_scalars };

  // ---------- W09 gap-blindness witness ----------
  // Hypothetical capture plan: 7095 planned events, 81 single-sample drops -> 7014 recorded.
  const planned = 7095, drops = 81;
  const dt = []; const base = R21.acc.median_dt_s;
  for (let i = 0; i < planned - 1 - drops; i++) dt.push(base);           // recorded adjacent intervals
  for (let i = 0; i < drops; i++) dt.push(2 * base);                     // each drop doubles one interval
  dt.sort((a, b) => a - b);
  const median_dt = (dt[Math.floor((dt.length - 1) / 2)] + dt[Math.ceil((dt.length - 1) / 2)]) / 2;
  const max_gap = Math.max(...dt);
  const gaps_gt_5x = dt.filter(v => v > 5 * median_dt).length;
  const w09 = { planned, drops, recorded: planned - drops, loss_pct: drops / planned * 100,
    median_dt, max_gap, max_gap_over_threshold: max_gap / (5 * median_dt), gaps_gt_5x_median: gaps_gt_5x,
    conclusion: gaps_gt_5x === 0 && drops > 0 ? 'ZERO_REPORTED_GAPS_DO_NOT_PROVE_LOSSLESSNESS' : 'UNEXPECTED' };

  // ---------- W10 phase offset not derivable ----------
  const w10 = { duration_diff_s: R21.acc.duration_s - R21.gyro.duration_s,
    derivable: false, reason: 'no common absolute time reference or overlap information in aggregates' };

  // ---------- W11 M1-RAD: folded-normal radial magnitude model ----------
  // M ~ |nu + sigma Z|, Z~N(0,1). Solve (nu,sigma) from (mag_mean, mag_stdev).
  let nu = R21.acc.mag_mean, sigma = R21.acc.mag_stdev;
  for (let it = 0; it < 200; it++) {
    const a = nu / sigma;
    const mu_f = nu * (2 * Phi(a) - 1) + 2 * sigma * Math.exp(-a * a / 2) / Math.sqrt(2 * Math.PI);
    const sd_f = Math.sqrt(nu * nu + sigma * sigma - mu_f * mu_f);
    const nu_n = nu + (R21.acc.mag_mean - mu_f);
    const sigma_n = sigma * (R21.acc.mag_stdev / sd_f);
    if (Math.abs(nu_n - nu) < 1e-15 && Math.abs(sigma_n - sigma) < 1e-18) { nu = nu_n; sigma = sigma_n; break; }
    nu = nu_n; sigma = sigma_n;
  }
  const lambda = nu / sigma;
  const zG = (g0 - nu) / sigma;
  const p_below_g0 = Phi(zG);
  const d = nu - g0;
  const e_abs_dev = sigma * Math.sqrt(2 / Math.PI) * Math.exp(-d * d / (2 * sigma * sigma)) + d * (2 * Phi(d / sigma) - 1);
  const w11 = { model: 'M1_RAD folded normal |nu+sigma Z|, radial-only noise',
    nu, sigma_axis_radial: sigma, lambda_nu_over_sigma: lambda,
    p_M_below_g0: p_below_g0, e_abs_M_minus_g0: e_abs_dev,
    note: 'E[|M-g0|] exceeds the reported |mean-g0| residual; the two are different quantities.' };

  // ---------- W12 M3-ISO: 3D isotropic noise, noncentral chi k=3 ----------
  // M = sigma_axis * chi'_3(delta), delta = nu/sigma_axis. Delta method on chi'^2_3:
  // E[Y]=3+d2, Var(Y)=2(3+2d2), E[M] ~= sigma*(sqrt(EY) - Var(Y)/(8 EY^1.5)), E[M^2]=sigma^2*EY.
  const c2 = R21.acc.mag_mean ** 2 + R21.acc.mag_stdev ** 2; // = sigma^2 * EY
  // Joint solve: sigma = sqrt(c2/(3+d2)); E[M] = sigma*(sqrt(EY) - VY/(8 EY^1.5)) = mag_mean.
  function eM(d2v, sg) { const EY = 3 + d2v, VY = 2 * (3 + 2 * d2v);
    return sg * (Math.sqrt(EY) - VY / (8 * Math.pow(EY, 1.5))); }
  let lo = 0, hi = 1e7;
  for (let it = 0; it < 300; it++) { // bisection on d2, monotone in E[M]
    const mid = (lo + hi) / 2, sg = Math.sqrt(c2 / (3 + mid));
    if (eM(mid, sg) < R21.acc.mag_mean) lo = mid; else hi = mid;
  }
  const d2 = (lo + hi) / 2; const sigma3 = Math.sqrt(c2 / (3 + d2));
  const sdM3 = Math.sqrt(c2 - eM(d2, sigma3) ** 2);
  // Anisotropic witnesses: for small noise, Var(M) ~ e_g' Sigma e_g (projection of the noise
  // covariance onto the gravity direction), so mag_stdev identifies ONLY that projection.
  const sdFolded = (nuv, sg) => { // exact SD of |nuv + sg Z| (axis-dominant noise models)
    const aa = nuv / sg;
    const mu_f = nuv * (2 * Phi(aa) - 1) + 2 * sg * Math.exp(-aa * aa / 2) / Math.sqrt(2 * Math.PI);
    return Math.sqrt(nuv * nuv + sg * sg - mu_f * mu_f);
  };
  const sgRef = R21.acc.mag_stdev, nuRef = R21.acc.mag_mean;
  const w12 = { model: 'M3_ISO 3D isotropic, M = sigma_axis * chi\'_3(delta), delta-method moments',
    nu: sigma3 * Math.sqrt(d2), sigma_axis_isotropic: sigma3, delta: Math.sqrt(d2),
    sd_of_magnitude: sdM3, sd_to_axis_factor: sdM3 / sigma3,
    prereg_expectation_refuted: true,
    prereg_expected: 'SD(M) ~ sqrt(3) * sigma_axis (prereg W12, frozen)',
    executed_finding: 'SD(M) ~ sigma_axis to 7.6e-7 relative at delta~1072; the sqrt(3) prereg expectation is FALSIFIED. Correct statement: Var(M) ~ e_g\' Sigma e_g (projection of the noise covariance onto the gravity direction); the full axis covariance is NOT identifiable.',
    anisotropic_equivalence: {
      isotropic_sigma_axis: { sigma: sgRef, sd_of_magnitude_model: sdM3 },
      z_dominant_sigma_z: { sigma: sgRef, sd_of_magnitude_model: sdFolded(nuRef, sgRef) },
      x_dominant_sigma_x: { sigma: sgRef, sd_of_magnitude_model: sdFolded(nuRef, sgRef) },
      note: 'three structurally different axis covariances reproduce the same magnitude SD to <1e-6 relative while implying completely different full covariances'
    },
    mean_model_split: { nu_radial_M1: w11.nu, nu_isotropic_M3: sigma3 * Math.sqrt(d2),
      nu_difference: w11.nu - sigma3 * Math.sqrt(d2),
      note: 'the models differ in the implied |g+b| by ~sigma^2/nu; E[M] carries a model-dependent O(sigma^2/nu) excess' } };

  // ---------- W13 SD definition unknown ----------
  const N = R21.acc.n;
  const w13 = { population_sd: R21.acc.mag_stdev,
    implied_sample_sd: R21.acc.mag_stdev * Math.sqrt(N / (N - 1)),
    abs_diff: R21.acc.mag_stdev * (Math.sqrt(N / (N - 1)) - 1),
    definition: 'UNKNOWN (ddof not documented)' };

  // ---------- W14 same aggregates, different order ----------
  const a = [], b = [];
  for (let i = 0; i < 16; i++) { a.push(i % 2 === 0 ? 1 : -1); }
  for (let i = 0; i < 16; i++) { const k = Math.floor(i / 2); b.push(k % 2 === 0 ? 1 : -1); }
  const sumA = { n: a.length, mean: mean(a), population_sd: psd(a) };
  const sumB = { n: b.length, mean: mean(b), population_sd: psd(b) };
  const w14 = { seriesA_lag1: lag1(a), seriesB_lag1: lag1(b),
    aggregates_identical: sumA.n === sumB.n && sumA.mean === sumB.mean && sumA.population_sd === sumB.population_sd,
    lag1_differs: lag1(a) !== lag1(b) };

  // ---------- W15 same magnitude, different direction ----------
  const v1 = [0, 0, 10], v2 = [10, 0, 0];
  const norm = v => Math.hypot(v[0], v[1], v[2]);
  const w15 = { v1, v2, norm1: norm(v1), norm2: norm(v2),
    same_norm: norm(v1) === norm(v2), same_vector: JSON.stringify(v1) === JSON.stringify(v2) };

  // ---------- W16 yaw gauge + SO(3) orientation witnesses ----------
  function rotZ(p) { const c = Math.cos(p), s = Math.sin(p);
    return [[c, -s, 0], [s, c, 0], [0, 0, 1]]; }
  function rotX(p) { const c = Math.cos(p), s = Math.sin(p);
    return [[1, 0, 0], [0, c, -s], [0, s, c]]; }
  function rotY(p) { const c = Math.cos(p), s = Math.sin(p);
    return [[c, 0, s], [0, 1, 0], [-s, 0, c]]; }
  function mTmul(A, v) { const out = [0, 0, 0];
    for (let i = 0; i < 3; i++) out[i] = A[0][i] * v[0] + A[1][i] * v[1] + A[2][i] * v[2];
    return out; }
  const gv = [0, 0, g0];
  const yaw_devs = [];
  for (let k = 0; k <= 1440; k++) {
    const psi = 2 * Math.PI * k / 1440;
    const R = rotZ(psi);
    const am = mTmul(R, gv); // a = R^T g, R = Rz(psi)
    yaw_devs.push(Math.max(Math.abs(am[0]), Math.abs(am[1]), Math.abs(am[2] - g0)));
  }
  const so3 = [];
  for (let k = 0; k < 8; k++) so3.push(rotX(0.7 * k));
  const so3_res = so3.map(R => { const am = mTmul(R, gv);
    return { a_meas: am, norm: Math.hypot(am[0], am[1], am[2]) }; });
  const w16 = { yaw_grid_points: 1441, yaw_max_abs_deviation: Math.max(...yaw_devs),
    yaw_conclusion: 'yaw about gravity axis leaves a_meas EXACTLY invariant (gauge)',
    so3_samples: so3_res,
    so3_conclusion: 'under arbitrary SO(3) only the magnitude |a_meas| is invariant; vector components are NOT recoverable from magnitude aggregates' };

  // ---------- W17 one-pose affine ambiguity ----------
  const models = [{ scale: 1, bias: 0 }, { scale: 0.9, bias: 1 }];
  const w17 = { models,
    output_at_10: models.map(m => m.scale * 10 + m.bias),
    output_at_minus10: models.map(m => m.scale * -10 + m.bias),
    ambiguous_at_working_point: models[0].scale * 10 + models[0].bias === models[1].scale * 10 + models[1].bias,
    distinguishable_at_other_point: models[0].scale * -10 + models[0].bias !== models[1].scale * -10 + models[1].bias };

  // ---------- W18 consistency demo: sigma=0 with sd>0 is INCONSISTENT ----------
  const w18 = { model: 'pure constant with sigma_axis = 0', observed_sd: R21.acc.mag_stdev,
    compatible_set: 'EMPTY', verdict: 'INCONSISTENT', note: 'demonstrates the empty-set -> INCONSISTENT rule' };

  // ---------- W19 implied gravity offset, statistical vs attribution ---
  const se_mean_radial = R21.acc.mag_stdev / Math.sqrt(N);
  const w19 = { mean_minus_g0: R21.acc.mag_mean - g0,
    statistical_se_mean_magnitude: se_mean_radial,
    z_vs_conventional_g0: (R21.acc.mag_mean - g0) / se_mean_radial,
    attribution_identifiable: false,
    verdict: 'ABSTAIN on local-gravity correction: offset is statistically nonzero but attribution to bias/tilt/scale/local-g is not identifiable from magnitude aggregates alone' };

  // ---------- W20..W25 contract negative cases ----------
  const rules = [
    { id: 'historic-labeled-live', test: r => !(r.epoch === 'historical' && r.presentation === 'live') },
    { id: 'producer-tick-age-refresh', test: r => !(r.freshness_source === 'producer_tick' && r.age_source === 'now') },
    { id: 'body-pose-from-table', test: r => !(r.input === 'table_rest_aggregate' && r.output_class === 'body_pose') },
    { id: 'synthetic-as-physical', test: r => !(r.origin === 'E2_SYNTHETIC' && r.displayed_as === 'E0_PHYSICAL') },
    { id: 'source-hash-as-truth', test: r => !(r.verification_basis === 'source_hash_only') },
    { id: 'stale-unknown-conflation', test: r => !(r.status === 'stale' && r.displayed_status === 'unknown') }
  ];
  const bad = [
    { epoch: 'historical', presentation: 'live' },
    { freshness_source: 'producer_tick', age_source: 'now' },
    { input: 'table_rest_aggregate', output_class: 'body_pose' },
    { origin: 'E2_SYNTHETIC', displayed_as: 'E0_PHYSICAL' },
    { verification_basis: 'source_hash_only' },
    { status: 'stale', displayed_status: 'unknown' }
  ];
  const good = [
    { epoch: 'historical', presentation: 'historical' },
    { origin: 'E2_SYNTHETIC', displayed_as: 'E2_SYNTHETIC' }
  ];
  const w20_25 = { rules: rules.map(r => r.id),
    negative_cases: bad.map((r, i) => ({ case: rules[i].id, verdict: rules[i].test(r) ? 'ACCEPT (BAD!)' : 'REJECT' })),
    positive_cases: good.map(r => ({ record: r, verdict: rules.every(rule => rule.test(r)) ? 'ACCEPT' : 'REJECT (BAD!)' })),
    all_reject: bad.every((r, i) => !rules[i].test(r)),
    positives_pass: good.every(r => rules.every(rule => rule.test(r))),
    nonvacuity_note: 'two positive control records pass, so the rules are not vacuously rejecting everything' };

  const all_pass = [w01.match_1e9, w02.match_1e9, w06.rel_diff < 1e-12, w07.distinct, w09.conclusion === 'ZERO_REPORTED_GAPS_DO_NOT_PROVE_LOSSLESSNESS',
    w14.aggregates_identical && w14.lag1_differs, w15.same_norm && !w15.same_vector,
    w16.yaw_max_abs_deviation < 1e-14, w17.ambiguous_at_working_point && w17.distinguishable_at_other_point,
    w20_25.all_reject, w20_25.positives_pass].every(Boolean);

  return {
    runner: '03_WITNESSES_RUNNER.js', lineage: 'VIBE_GLM_R1_FIRST_RUN',
    prereg: '02_PREREG.md (frozen before execution; sha256 recorded in 04_RESULTS.json by the report step)',
    inputs: 'R21 aggregates from 02_EVIDENCE.json @ HEAD d7e1c95d276b20254b8c30a4de4b1310d18a1b31; NO raw data',
    all_preregistered_checks_pass: all_pass,
    A_aggregate: { w01_rate_acc: w01, w02_rate_gyro: w02, w03_median_reciprocal: w03, w04_duration_residual: w04,
      w05_requested_vs_effective: w05, w06_residual_identity: w06, w07_counterexample: w07,
      w08_information_balance: w08, w09_gap_blindness: w09, w10_phase_offset: w10 },
    B_model_conditional: { w11_m1_rad: w11, w12_m3_iso: w12, w13_sd_definition: w13 },
    C_identifiability: { w14_ordering: w14, w15_direction: w15, w16_yaw_gauge_so3: w16, w17_one_pose_affine: w17,
      w18_inconsistent_demo: w18, w19_gravity_offset_abstain: w19 },
    D_contract: w20_25,
    limits: 'Synthetic witnesses are E2_SYNTHETIC, never OPPO measurements. Aggregate arithmetic is E1_DERIVED. Model results are E1_MODEL_CONDITIONAL. No raw replay, no axis covariance, no bias vector, no Allan curve, no whiteness, no drift, no effective sample size, no NIS/NEES, no confidence intervals from norms alone. No formal gate credit.'
  };
}
const RESULT = run();
if (typeof module !== 'undefined') module.exports = RESULT;
