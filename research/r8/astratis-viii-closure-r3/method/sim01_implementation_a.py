"""
sim01_implementation_a.py — NDVI Monte-Carlo Fehlerfortpflanzung, Implementation A

FESTGESCHRIEBENE SPEZIFIKATION (nicht ohne neuen Commit aendern):
  RNG_ALGORITHM  = numpy.random.default_rng (PCG64)
  SAMPLING_ORDER = RED_FIRST_BLOCK: pro Seed zuerst N Red-Samples ziehen,
                   danach N NIR-Samples, als zwei getrennte .normal()-Aufrufe.
  N              = 100000 Samples pro Seed
  SEEDS          = fixe Liste unten, 20 Seeds
  NOISE_MODEL    = absolut, sigma_Red = sigma_NIR = 0.02
  STD_ESTIMATOR  = Populations-Standardabweichung (ddof=0)

Diese Datei ist die einzige kanonische Quelle fuer SIM-01 Implementation A.
Keine weitere Tabelle, kein weiteres Validierungsdokument ersetzt das
tatsaechliche Ausfuehren dieses Skripts.
"""
import json
import numpy as np

RED, NIR = 0.08, 0.25
SIGMA_RED, SIGMA_NIR = 0.02, 0.02
N = 100_000
SEEDS = [42] + list(range(0, 19))  # 20 Seeds total, seed=42 zuerst fuer Vergleichbarkeit


def run_seed(seed: int) -> float:
    rng = np.random.default_rng(seed)
    red_s = rng.normal(RED, SIGMA_RED, N)   # RED zuerst
    nir_s = rng.normal(NIR, SIGMA_NIR, N)   # danach NIR
    ndvi_s = (nir_s - red_s) / (nir_s + red_s)
    return float(ndvi_s.std(ddof=0))


def main() -> dict:
    per_seed = {seed: run_seed(seed) for seed in SEEDS}
    values = np.array(list(per_seed.values()))

    dN = 2 * RED / (NIR + RED) ** 2
    dR = -2 * NIR / (NIR + RED) ** 2
    taylor_sigma = float(np.sqrt((dN * SIGMA_NIR) ** 2 + (dR * SIGMA_RED) ** 2))

    out = {
        "implementation": "A_numpy_default_rng_PCG64",
        "rng_algorithm": "numpy.random.default_rng (PCG64)",
        "numpy_version": np.__version__,
        "sampling_order": "RED_FIRST_BLOCK",
        "n_per_seed": N,
        "seeds": SEEDS,
        "per_seed_sigma_ndvi": per_seed,
        "mc_mean": float(values.mean()),
        "between_seed_std": float(values.std(ddof=1)),
        "monte_carlo_error": float(values.std(ddof=1) / np.sqrt(len(values))),
        "taylor_reference": taylor_sigma,
        "mc_vs_taylor_rel_diff_pct": float((values.mean() - taylor_sigma) / taylor_sigma * 100),
    }
    return out


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
    with open("sim01_runs_a.json", "w") as f:
        json.dump(result, f, indent=2)
