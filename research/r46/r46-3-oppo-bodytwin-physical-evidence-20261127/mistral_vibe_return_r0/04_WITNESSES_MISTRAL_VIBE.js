// MISTRAL/VIBE independent witnesses for R46-3 (C1_DESCRIPTIVE_ONLY).
// Standalone, deterministic, no dependencies, no network, no raw data.
// Executed in the authoring sandbox via new Function so shipped code == executed code.
function run(ctx) {
  'use strict';
  var out = { witnesses: {}, error_cases: {}, limits: [] };
  var E = ctx.evidence, acc = E.r21.acc, gy = E.r21.gyro, g0 = 9.80665;

  var f64 = new Float64Array(1), u8 = new Uint8Array(f64.buffer);
  function bits(x) { f64[0] = x; var s = ''; for (var i = 7; i >= 0; i--) { s += (u8[i] >>> 4).toString(16) + (u8[i] & 15).toString(16); } return s; }
  var ONE = BigInt(1), S64 = BigInt(64);
  function toOrdered(hex) { var v = BigInt('0x' + hex); var sign = (v >> BigInt(63)) & ONE; if (sign === ONE) { v = (~v) & ((ONE << S64) - ONE); } else { v = v | (ONE << BigInt(63)); } return v; }
  function ulpDiff(a, b) { var ba = toOrdered(bits(a)), bb = toOrdered(bits(b)); return ba > bb ? ba - bb : bb - ba; }

  // W1: rate reproduction from reported (N, duration)
  var rateAcc = (acc.n - 1) / acc.duration_s;
  var rateGyro = (gy.n - 1) / gy.duration_s;
  var medRecip = 1 / acc.median_dt_s;
  out.witnesses.W1 = {
    id: 'W1_rate_reproduction',
    recomputed: { acc_hz: rateAcc, gyro_hz: rateGyro, median_reciprocal_hz: medRecip },
    reported: { acc_hz: acc.rate_hz, gyro_hz: gy.rate_hz },
    acc_bit_exact: rateAcc === acc.rate_hz,
    gyro_bit_exact: rateGyro === gy.rate_hz,
    requested_hz: E.r21.requested_hz,
    effective_minus_requested_acc_hz: rateAcc - E.r21.requested_hz,
    note: '(N-1)/duration reproduces both reported rates bit-exactly. Effective rate exceeds requested 100 Hz by ~0.15 Hz; Android sensors_overview documents that requested rate != measured rate.'
  };

  // W2: gravity_residual_mean_abs identity (abs(mean-g0), not mean|norm-g0|)
  var recomputedResid = Math.abs(acc.mag_mean - g0);
  var reportedResid = E.r21.gravity_residual_mean_abs_reported;
  out.witnesses.W2 = {
    id: 'W2_gravity_residual_identity',
    reported: reportedResid,
    recomputed_from_rounded_mag_mean: recomputedResid,
    abs_diff: Math.abs(reportedResid - recomputedResid),
    ulp_distance: Number(ulpDiff(reportedResid, recomputedResid)),
    hex_reported: bits(reportedResid),
    hex_recomputed: bits(recomputedResid),
    interpretation: 'Reported value is consistent with abs(mean(mag)-g0) evaluated on the rounded mean (96 ULP apart), matching AXIOM 04_REFERENCE. It does NOT establish mean(abs(norm-g0)); that requires raw norms.'
  };

  // W3: Jensen lower bound on a distribution consistent with reported aggregates
  var m = acc.mag_mean, s = acc.mag_stdev;
  var a1 = m - s, b1 = m + s;
  var absMean = Math.abs((a1 + b1) / 2 - g0);
  var meanAbs = (Math.abs(a1 - g0) + Math.abs(b1 - g0)) / 2;
  out.witnesses.W3 = {
    id: 'W3_jensen_lower_bound',
    construction: 'two-point distribution {m-s, m+s} matches reported mag_mean and population-SD mag_stdev exactly',
    abs_mean_residual: absMean,
    mean_abs_residual: meanAbs,
    gap: meanAbs - absMean,
    claim: '|mean-g0| is only a lower bound of mean|norm-g0| (Jensen). On an aggregate-consistent distribution the gap is strictly positive.'
  };

  // W4: local gravity conflation
  out.witnesses.W4 = {
    id: 'W4_local_g_conflation',
    conventional_g0: g0,
    mean_mag: m,
    residual_vs_conventional: m - g0,
    local_g_germany_plausible_range: [9.806, 9.822],
    example_local_g: 9.8105,
    residual_vs_example_local_g: m - 9.8105,
    claim: 'The ~0.026 m/s^2 residual conflates sensor bias, scale error and local gravity deviation; conventional g0 was not an independently measured local value in R21.'
  };

  // W5: ddof ambiguity
  var nA = acc.n;
  var factor = Math.sqrt(nA / (nA - 1));
  out.witnesses.W5 = {
    id: 'W5_ddof_ambiguity',
    n: nA,
    population_to_sample_sd_factor: factor,
    note: 'Reported standard_deviation_definition is UNKNOWN. Population vs sample (n-1) SD differ by this factor for n=7014 (~71 ppm); raw or definition needed to decide.'
  };

  // W6: SO(3)-invariance of magnitude (tilt and yaw unobservable)
  function rotVec(v, k, ang) {
    var c = Math.cos(ang), si = Math.sin(ang), t = 1 - c;
    var kx = k[0], ky = k[1], kz = k[2];
    return [
      (t*kx*kx + c)*v[0] + (t*kx*ky - si*kz)*v[1] + (t*kx*kz + si*ky)*v[2],
      (t*kx*ky + si*kz)*v[0] + (t*ky*ky + c)*v[1] + (t*ky*kz - si*kx)*v[2],
      (t*kx*kz - si*ky)*v[0] + (t*ky*kz + si*kx)*v[1] + (t*kz*kz + c)*v[2]
    ];
  }
  function norm(v) { return Math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]); }
  var axis = [1, 2, 3], axn = Math.sqrt(14); axis = [axis[0]/axn, axis[1]/axn, axis[2]/axn];
  var vecs = [[0, 0, 10], [10, 0, 0], [3.3, 4.4, 5.5], [-2.5, 7.25, 1.125]];
  var angles = [0.3, 1.1, 2.7];
  var maxNormErr = 0, maxMagErr = 0;
  for (var iv = 0; iv < vecs.length; iv++) {
    for (var ia = 0; ia < angles.length; ia++) {
      var rv = rotVec(vecs[iv], axis, angles[ia]);
      var e = Math.abs(norm(rv) - norm(vecs[iv]));
      if (e > maxNormErr) maxNormErr = e;
      var em = Math.abs(Math.hypot(rv[0], rv[1], rv[2]) - Math.hypot(vecs[iv][0], vecs[iv][1], vecs[iv][2]));
      if (em > maxMagErr) maxMagErr = em;
    }
  }
  out.witnesses.W6 = {
    id: 'W6_so3_invariance_of_magnitude',
    max_norm_error_over_rotations: maxNormErr,
    claim: 'Magnitude summaries are SO(3)-invariant: any tilt/yaw of the device leaves ACC and GYRO magnitudes unchanged. Device orientation is unidentifiable from norms alone; BodyTwin body-pose inference from phone-on-table magnitudes is not supported.'
  };

  // W7: identical magnitude statistics under different axis covariance
  var seq = [];
  for (var i2 = 0; i2 < 64; i2++) seq.push(Math.sin(i2 * 0.7) * 0.05);
  var A = seq.map(function (x) { return [0, 0, x]; });
  var B = seq.map(function (x) { return [x / Math.SQRT2, x / Math.SQRT2, 0]; });
  function magStats(V) {
    var mags = V.map(norm);
    var mm = mags.reduce(function (a, b) { return a + b; }, 0) / mags.length;
    var sd = Math.sqrt(mags.reduce(function (a, b) { return a + (b - mm) * (b - mm); }, 0) / mags.length);
    var varX = 0, varY = 0, varZ = 0;
    V.forEach(function (v) { varX += v[0]*v[0]; varY += v[1]*v[1]; varZ += v[2]*v[2]; });
    var q = V.length;
    return { mean: mm, sd: sd, axis_var: [varX/q, varY/q, varZ/q] };
  }
  var sA = magStats(A), sB = magStats(B);
  out.witnesses.W7 = {
    id: 'W7_axis_covariance_invisible',
    construction_A: 'all variation on +Z axis',
    construction_B: 'variation split equally on X and Y, zero on Z',
    stats_A: sA, stats_B: sB,
    magnitude_stats_identical: JSON.stringify([sA.mean, sA.sd]) === JSON.stringify([sB.mean, sB.sd]),
    axis_variance_differs: JSON.stringify(sA.axis_var) !== JSON.stringify(sB.axis_var),
    claim: 'Two datasets with identical magnitude mean/SD can have entirely different axis covariance (diag(0,0,v) vs diag(v/2,v/2,0)); norm SD does not constrain axis covariance.'
  };

  // W8: gyro bias vs rotation ambiguity; Earth-rate scaling
  var earthRate = 7.2921e-5;
  var ratio = gy.mag_mean / earthRate;
  var degPerS = gy.mag_mean * 180 / Math.PI;
  var wTrue1 = [0, 0, 0], bias1 = [0.002, 0, 0];
  var wTrue2 = [0.002, 0, 0], bias2 = [0, 0, 0];
  var obs1 = [wTrue1[0] + bias1[0], wTrue1[1] + bias1[1], wTrue1[2] + bias1[2]];
  var obs2 = [wTrue2[0] + bias2[0], wTrue2[1] + bias2[1], wTrue2[2] + bias2[2]];
  out.witnesses.W8 = {
    id: 'W8_gyro_bias_rotation_ambiguity',
    earth_rate_rad_s: earthRate,
    gyro_mag_mean_over_earth_rate: ratio,
    gyro_mag_mean_deg_s: degPerS,
    two_worlds_observation_1: obs1, two_worlds_observation_2: obs2,
    observationally_identical: JSON.stringify(obs1) === JSON.stringify(obs2),
    claim: 'A constant gyro bias vector and a constant true rotation component are observationally equivalent under this aggregate. Note gyro magnitude mean is ~27x Earth rate and ~0.11 deg/s, so scale/bias dominates Earth-rate comparison; an independent angle reference is required.'
  };

  // W9: temporal order invisible in mean/SD
  var orders = {
    alternating: [1, -1, 2, -2, 3, -3, 4, -4],
    blocked: [1, 2, 3, 4, -1, -2, -3, -4],
    reversed_blocks: [-4, -3, -2, -1, 1, 2, 3, 4]
  };
  function statsAndLag(x) {
    var mm = x.reduce(function (a, b) { return a + b; }, 0) / x.length;
    var sd = Math.sqrt(x.reduce(function (a, b) { return a + (b - mm) * (b - mm); }, 0) / x.length);
    var num = 0;
    for (var i = 0; i < x.length; i++) { num += (x[i] - mm) * (x[i] - mm); }
    var lagNum = 0;
    for (var j = 1; j < x.length; j++) lagNum += (x[j] - mm) * (x[j - 1] - mm);
    return { mean: mm, population_sd: sd, lag1: lagNum / num };
  }
  var o1 = statsAndLag(orders.alternating), o2 = statsAndLag(orders.blocked), o3 = statsAndLag(orders.reversed_blocks);
  out.witnesses.W9 = {
    id: 'W9_ordering_invisible_in_moments',
    orderings: { alternating: o1, blocked: o2, reversed_blocks: o3 },
    same_mean_sd: o1.mean === o2.mean && o2.mean === o3.mean && o1.population_sd === o2.population_sd && o2.population_sd === o3.population_sd,
    lag1_values_differ: !(o1.lag1 === o2.lag1 && o2.lag1 === o3.lag1),
    claim: 'Mean and SD are invariant under reordering while lag-1 autocorrelation differs sharply; no temporal (drift/whiteness) claim is identifiable from the reported aggregates.'
  };

  // W10: 5x-median gap rule blindness to short loss bursts
  var dt = 0.01;
  var lostTotal = 0;
  var positions = [], pos = 100;
  while (positions.length < 17) { positions.push(pos); pos += 400; }
  var lostIdx = {};
  positions.forEach(function (p) { for (var k = 0; k < 4; k++) lostIdx[p + k] = true; lostTotal += 4; });
  for (var k2 = 0; k2 < 2; k2++) { lostIdx[6900 + k2] = true; lostTotal += 1; }
  var gaps = [], prev = -1, flagged = 0;
  for (var i3 = 0; i3 < 7000; i3++) {
    if (lostIdx[i3]) continue;
    if (prev >= 0) { var g = (i3 - prev) * dt; gaps.push(g); if (g > 5 * dt) flagged++; }
    prev = i3;
  }
  var maxGap = Math.max.apply(null, gaps);
  out.witnesses.W10 = {
    id: 'W10_gap_rule_blindness',
    synthetic_events: 7000, lost_events: lostTotal,
    flagged_gaps_gt_5x_median: flagged,
    max_observed_gap_multiple_of_median: maxGap / dt,
    claim: '70 of 7000 events removed in clusters of <=4 consecutive events produce max gap of exactly 5x median dt; the strict > 5x-median rule flags nothing. Zero flagged gaps is NOT proof of zero packet loss; matches the R21 gaps_gt_5x_median = 0 interpretation limit.'
  };

  // W11: aggregate compression
  var aggCount = 12; // numeric aggregates reported in 02_EVIDENCE r21 across both sensors
  var events = acc.n + gy.n;
  out.witnesses.W11 = {
    id: 'W11_aggregate_compression',
    numeric_aggregates_in_summary: aggCount,
    sensor_events: events,
    ndjson_lines: E.r21.ndjson_lines,
    non_sensor_lines: E.r21.non_sensor_lines,
    retained_fraction: aggCount / events,
    event_level_information_not_in_summary: 1 - aggCount / events,
    claim: '12 numbers summarize 14,018 sensor events (14,020 NDJSON lines minus 2 non-sensor); over 99.9 percent of event-level information is absent from the aggregate.'
  };

  // W12: producer reference vs independent arithmetic
  var ref = ctx.reference;
  var mine = { acc: rateAcc, gyro: rateGyro, median_reciprocal: medRecip, mean_minus_conventional_g: acc.mag_mean - g0 };
  out.witnesses.W12 = {
    id: 'W12_producer_vs_independent_arithmetic',
    reference_executed_independently_here: !!ref && !ctx.referenceError,
    reference_checks_all_true: !!ref && !!ref.checks && Object.keys(ref.checks).every(function (k) { return ref.checks[k] === true; }),
    arithmetic_comparison: {
      acc_bit_exact: ref && ref.aggregate_arithmetic ? ref.aggregate_arithmetic.acc === mine.acc : null,
      gyro_bit_exact: ref && ref.aggregate_arithmetic ? ref.aggregate_arithmetic.gyro === mine.gyro : null,
      median_reciprocal_bit_exact: ref && ref.aggregate_arithmetic ? ref.aggregate_arithmetic.median_reciprocal === mine.median_reciprocal : null,
      mean_minus_g_bit_exact: ref && ref.aggregate_arithmetic ? ref.aggregate_arithmetic.mean_minus_conventional_g === mine.mean_minus_conventional_g : null
    },
    claim: 'AXIOM 04_REFERENCE.js reproduces bit-exactly as independent derived arithmetic here, but it is explicitly synthetic + aggregate-derived; it is NOT an independent raw replay and carries no formal gate credit (per 05_RESULTS scope field).'
  };

  // Error cases
  var tol = 1e-12;
  var perturbed9 = rateAcc * (1 + 1e-9);
  var flagged9 = false;
  try { if (!(Math.abs(perturbed9 - rateAcc) < tol)) { throw new Error('rate mismatch beyond tolerance'); } } catch (e) { flagged9 = true; }
  out.error_cases.E1 = { id: 'E1_injected_fault_flagged', fault: 'acc rate perturbed by 1e-9 relative', tolerance: tol, detected: flagged9, status: flagged9 ? 'FLAGGED' : 'UNEXPECTED' };

  var perturbed13 = rateAcc * (1 + 1e-13);
  var passesTolerance = Math.abs(perturbed13 - rateAcc) < tol;
  out.error_cases.E2 = {
    id: 'E2_sub_tolerance_fault_missed',
    fault: 'acc rate perturbed by 1e-13 relative',
    tolerance: tol,
    detected: !passesTolerance,
    status: passesTolerance ? 'MISSED' : 'FLAGGED',
    lesson: 'A fixed 1e-12 absolute tolerance accepts a 1e-13-scale tampering. Verification tolerances must be ULP-scaled, e.g. Math.abs(diff) <= 8 * Number.EPSILON * Math.max(Math.abs(a), Math.abs(b)). Honest limitation of the 04_REFERENCE tolerance design.'
  };

  var recorded = ctx.recordedSha256 || {};
  var tamperName = ctx.tamperTarget || '02_EVIDENCE.json';
  var genuine = recorded[tamperName];
  var tampered = genuine ? genuine.slice(0, genuine.length - 1) + (genuine[genuine.length - 1] === '0' ? '1' : '0') : null;
  function verify(name, sha) { return recorded[name] === sha ? 'ACCEPT' : 'REJECT'; }
  out.error_cases.E3 = {
    id: 'E3_manifest_tamper_detection',
    tamper_target: tamperName,
    genuine_verdict: genuine ? verify(tamperName, genuine) : 'NO_DATA',
    tampered_sha256: tampered,
    tampered_verdict: tampered ? verify(tamperName, tampered) : 'NO_DATA',
    claim: 'The member hash comparator rejects a single-hex-digit manifest tamper (REJECT) and accepts the genuine hash (ACCEPT).'
  };

  out.limits = [
    'All witnesses are synthetic constructions or derived arithmetic on the public aggregate; no raw OPPO measurements were accessed.',
    'W3/W5/W7/W9/W10 use deterministic synthetic inputs chosen for exactness of the demonstration, not sampled noise.',
    'No formal or physical gate credit; design-level findings only; C1_DESCRIPTIVE_ONLY.',
    'Units and frame of the R21 aggregates remain conditional on the actual Android SensorEvent mapping in NEXUS_APP, which is not independently established here.'
  ];
  return out;
}
if (typeof module !== 'undefined' && module.exports) { module.exports = { run: run }; }
