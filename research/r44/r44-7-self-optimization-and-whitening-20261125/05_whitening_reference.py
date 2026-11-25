"""New AXIOM reference, not original model5.py. No external IO."""
import numpy as np

def corrected_residual(W, r):
    return np.linalg.cholesky(W).T @ r

def main():
    r = np.array([1., 2., -1., .5, 0.])
    for rho in (.3, .8):
        i = np.arange(5)
        S = rho ** np.abs(i[:, None] - i[None, :])
        W = np.linalg.inv(S)
        L = np.linalg.cholesky(W)
        target = float(r @ W @ r)
        old = float(np.linalg.norm(L @ r)**2)
        fixed = float(np.linalg.norm(corrected_residual(W, r))**2)
        if not np.isclose(target, fixed, rtol=1e-12, atol=1e-12):
            raise RuntimeError("corrected objective mismatch")
        if np.isclose(old, target, rtol=1e-12, atol=1e-12):
            raise RuntimeError("negative control not discriminating")
        print(rho, target, old, fixed)
if __name__ == "__main__":
    main()
