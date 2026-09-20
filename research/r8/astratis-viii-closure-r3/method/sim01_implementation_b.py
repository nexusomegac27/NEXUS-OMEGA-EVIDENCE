"""
sim01_implementation_b.py — NDVI Monte-Carlo Fehlerfortpflanzung, Implementation B

Unabhaengige zweite Implementierung: nutzt Pythons Standardbibliothek
(random.gauss) statt NumPy/PCG64, um einen echten Implementierungs-Unterschied
(nicht nur RNG-Seed) zu haben.

GLEICHE SPEZIFIKATION wie Implementation A (sim01_implementation_a.py):
  SAMPLING_ORDER = RED_FIRST_BLOCK
  N              = 100000 pro Seed
  SEEDS          = gleiche 20 Seeds
  NOISE_MODEL    = absolut, sigma_Red = sigma_NIR = 0.02

RNG_ALGORITHM unterscheidet sich bewusst: stdlib `random` (Mersenne-Twister-
Kern, Gauss ueber eigenen Code-Pfad, nicht PCG64). Ziel: pruefen, ob MC_MEAN
und Taylor-Referenz implementierungsunabhaengig konvergieren.
"""
import json
import random
import statistics

RED, NIR = 0.08, 0.25
SIGMA_RED, SIGMA_NIR = 0.02, 0.02
N = 100_000
SEEDS = [42] + list(range(0, 19))


def run_seed(seed: int) -> float:
    random.seed(seed)
    red_s = [random.gauss(RED, SIGMA_RED) for _ in range(N)]   # RED zuerst
    nir_s = [random.gauss(NIR, SIGMA_NIR) for _ in range(N)]   # danach NIR
    ndvi_s = [(n - r) / (n + r) for n, r in zip(nir_s, red_s)]
    return statistics.pstdev(ndvi_s)


def main() -> dict:
    per_seed = {seed: run_seed(seed) for seed in SEEDS}
    values = list(per_seed.values())

    dN = 2 * RED / (NIR + RED) ** 2
    dR = -2 * NIR / (NIR + RED) ** 2
    taylor_sigma = (dN * SIGMA_NIR) ** 2 + (dR * SIGMA_RED) ** 2
    taylor_sigma = taylor_sigma ** 0.5

    mc_mean = statistics.mean(values)
    out = {
        "implementation": "B_stdlib_random_gauss",
        "rng_algorithm": "python stdlib random.gauss (Mersenne-Twister-Kern, eigener Gauss-Codepfad)",
        "sampling_order": "RED_FIRST_BLOCK",
        "n_per_seed": N,
        "seeds": SEEDS,
        "per_seed_sigma_ndvi": per_seed,
        "mc_mean": mc_mean,
        "between_seed_std": statistics.stdev(values),
        "monte_carlo_error": statistics.stdev(values) / (len(values) ** 0.5),
        "taylor_reference": taylor_sigma,
        "mc_vs_taylor_rel_diff_pct": (mc_mean - taylor_sigma) / taylor_sigma * 100,
    }
    return out


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
    with open("sim01_runs_b.json", "w") as f:
        json.dump(result, f, indent=2)
