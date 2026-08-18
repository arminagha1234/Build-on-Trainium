#!/usr/bin/env bash
# Capture a neuron-explorer hardware profile of the on-device kernel run and
# print a text summary.
#
# Prereq: the class venv is active  ->  source ~/nki-class-venv/bin/activate
# Usage:  bash profile_kernel.sh [OUTDIR]   (default: ./profile_out)
#
# Note: neuron-profile has been deprecated/removed in this SDK; the current tool
# is `neuron-explorer` (same capture/view subcommands).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTDIR="${1:-$HERE/profile_out}"
CACHE="/var/tmp/neuron-compile-cache"
mkdir -p "$OUTDIR"

MARKER="$(mktemp)"
echo "[profile] running kernel on device (compiles + populates NEFF cache) ..."
NEURON_PLATFORM_TARGET_OVERRIDE=trn2 python "$HERE/run_assignment.py" --device >/dev/null

echo "[profile] locating freshly-compiled NEFF in $CACHE ..."
NEFF="$(find "$CACHE" -name '*.neff' -newer "$MARKER" 2>/dev/null | head -1)"
if [ -z "$NEFF" ]; then
    # Cache hit (no recompile): fall back to the most recently modified NEFF.
    NEFF="$(find "$CACHE" -name '*.neff' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)"
fi
rm -f "$MARKER"
if [ -z "$NEFF" ]; then
    echo "[profile] ERROR: no NEFF found under $CACHE" >&2
    exit 1
fi
echo "[profile] NEFF: $NEFF"

NTFF="$OUTDIR/profile.ntff"
echo "[profile] capturing device profile -> $NTFF"
neuron-explorer capture -n "$NEFF" -s "$NTFF"

echo "[profile] ===================== summary ====================="
neuron-explorer view -n "$NEFF" -s "$NTFF" --output-format summary-text --disable-ui

echo "[profile] artifacts in: $OUTDIR"
echo "[profile] tip: for the interactive UI run:"
echo "    neuron-explorer view -n \"$NEFF\" -s \"$NTFF\""
