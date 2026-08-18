"""
NKI kernels for the Trainium class assignments.

Students implement their kernel in the marked TODO region below. Everything else
-- the harness (run_assignment.py) and the profiler (profile_kernel.sh) -- stays
the same, so the dev loop is identical for every assignment:

    1. Edit student_kernel() below using nki.language (nl) ops.
    2. python run_assignment.py                                  # CPU-simulation numerics
    3. NEURON_PLATFORM_TARGET_OVERRIDE=trn2 python run_assignment.py --device
    4. bash profile_kernel.sh                                    # neuron-explorer profile

NKI quick reference (import nki.language as nl):
    nl.load(hbm[...])                              load a tile from HBM into SBUF
    nl.store(hbm[...], value=tile)                 store an SBUF tile back to HBM
    nl.ndarray(shape, dtype, buffer=nl.shared_hbm) allocate an HBM output tensor
    tile math: a + b, a * scalar, nl.add, nl.multiply, nl.maximum, nl.exp, ...

Tiling constraint: the partition (first) dimension of a tile must be <= 128.
For these starter shapes we use a single [P, F] tile with P <= 128.
"""
import nki
import nki.language as nl


@nki.jit
def student_kernel(a, b, scale):
    """Compute  out = scale * a + b  (elementwise) -- a worked reference example.

    Args:
        a, b : 2D HBM input tensors, shape [P, F] with P <= 128.
        scale: python float, compile-time scalar.
    Returns:
        HBM tensor of the same shape/dtype as `a`.

    ======================== TODO(student) ========================
    Replace the body between LOAD and STORE with your own kernel.
    Keep the signature and return an nl HBM tensor (see `out`).
    ===============================================================
    """
    out = nl.ndarray(a.shape, dtype=a.dtype, buffer=nl.shared_hbm)

    # --- LOAD: bring inputs from HBM into on-chip SBUF -------------------
    a_tile = nl.load(a)
    b_tile = nl.load(b)

    # --- COMPUTE (your work goes here) ----------------------------------
    #   out = scale * a + b
    out_tile = nl.add(nl.multiply(a_tile, scale), b_tile)

    # --- STORE: write the result tile back to HBM -----------------------
    nl.store(out, value=out_tile)
    return out


def reference(a, b, scale):
    """Plain-numpy reference the kernel must match (used by run_assignment.py)."""
    return scale * a + b
