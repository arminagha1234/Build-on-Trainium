#!/usr/bin/env bash
# Create a pinned, reproducible NKI class virtualenv.
#
# Usage:
#   bash setup_venv.sh [VENV_DIR]
# Default VENV_DIR: ~/nki-class-venv
#
# This is the environment students use for the NKI assignments. It deliberately
# contains ONLY what NKI needs (neuronx-cc + nki + numpy) -- no vLLM, no XLA,
# no framework. Bake the resulting venv (or this script) into the class AMI.
set -euo pipefail

VENV_DIR="${1:-$HOME/nki-class-venv}"
NEURON_PIP_REPO="https://pip.repos.neuron.amazonaws.com"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[nki-lab] creating venv at: $VENV_DIR"
python3 -m venv "$VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "[nki-lab] upgrading pip"
python -m pip install --upgrade pip >/dev/null

echo "[nki-lab] installing pinned Neuron deps from $NEURON_PIP_REPO"
pip install -r "$HERE/requirements-neuron.txt" --extra-index-url "$NEURON_PIP_REPO"

echo "[nki-lab] freezing exact versions -> requirements-lock.txt"
pip freeze > "$HERE/requirements-lock.txt"

echo "[nki-lab] verifying imports + compiler ..."
python - <<'PY'
import numpy, nki, neuronxcc
import nki.language as nl  # noqa: F401
print("  numpy     ", numpy.__version__)
print("  nki       ", getattr(nki, "__version__", "?"))
print("  neuronx-cc", getattr(neuronxcc, "__version__", "?"))
print("  OK: imports succeeded")
PY

echo
echo "[nki-lab] done. Activate with:"
echo "    source $VENV_DIR/bin/activate"
