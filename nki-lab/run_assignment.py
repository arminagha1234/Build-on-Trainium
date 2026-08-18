#!/usr/bin/env python3
"""
Harness for the NKI class assignment.

Runs the student's kernel and checks numerics against a plain-numpy reference:
  - CPU simulation (nki.simulate)  -- always run
  - on-device (Trainium)           -- run with --device

Exit code is 0 iff every requested check passes, so this doubles as a grader /
CI gate.

Examples:
  python run_assignment.py                                   # sim only
  NEURON_PLATFORM_TARGET_OVERRIDE=trn2 python run_assignment.py --device
  python run_assignment.py --rows 128 --cols 1024 --scale 3.0 --device
"""
import argparse
import sys

import numpy as np
import nki

from nki_kernels import student_kernel, reference


def main() -> int:
    p = argparse.ArgumentParser(description="Run + check the NKI assignment kernel.")
    p.add_argument("--rows", type=int, default=128, help="partition dim (<= 128)")
    p.add_argument("--cols", type=int, default=512, help="free dim")
    p.add_argument("--scale", type=float, default=2.5, help="scalar passed to the kernel")
    p.add_argument("--atol", type=float, default=1e-4, help="absolute tolerance")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--device", action="store_true", help="also run on the Trainium device")
    args = p.parse_args()

    if args.rows > 128:
        print(f"WARNING: rows={args.rows} > 128; a single NKI tile's partition dim must be <= 128.")

    rng = np.random.default_rng(args.seed)
    a = rng.standard_normal((args.rows, args.cols)).astype(np.float32)
    b = rng.standard_normal((args.rows, args.cols)).astype(np.float32)
    ref = reference(a, b, args.scale)

    checks = []

    # 1) CPU simulation -- fast, no device, great for correctness iteration.
    sim = np.asarray(nki.simulate(student_kernel)(a, b, args.scale))
    checks.append(("simulate", bool(np.allclose(sim, ref, atol=args.atol)),
                   float(np.max(np.abs(sim - ref)))))

    # 2) On-device -- the real thing on Trainium.
    if args.device:
        dev = np.asarray(student_kernel(a, b, args.scale))
        checks.append(("device", bool(np.allclose(dev, ref, atol=args.atol)),
                       float(np.max(np.abs(dev - ref)))))

    print(f"\nshape=[{args.rows}, {args.cols}]  scale={args.scale}  atol={args.atol}")
    print(f"{'check':10} {'result':6} {'max_abs_err':>12}")
    print("-" * 30)
    all_ok = True
    for name, ok, err in checks:
        all_ok = all_ok and ok
        print(f"{name:10} {'PASS' if ok else 'FAIL':6} {err:12.3e}")
    print("-" * 30)
    print("OVERALL:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
