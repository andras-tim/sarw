#!/bin/bash
set -e

BASEDIR="$(dirname "$0")"
OUTDIR="${HOME}/Pictures/wallpapers/random"
OUTFILE_PREFIX="${OUTDIR}/$(date +%Y-%m-%d)"

# Main
mkdir -p "${OUTDIR}"

python "${BASEDIR}/download-random-double-wide-wallpaper.py" "${OUTFILE_PREFIX}.jpg" "$@"
echo

python "${BASEDIR}/crop-wallpaper-for-multi-monitors.py" "${OUTFILE_PREFIX}.jpg" "${OUTFILE_PREFIX}"
rm "${OUTFILE_PREFIX}.jpg"
echo

python "${BASEDIR}/set-multi-xfce4-wallpapers.py" "${OUTFILE_PREFIX}_c-center.jpg" "${OUTFILE_PREFIX}_a-left.jpg" "${OUTFILE_PREFIX}_b-right.jpg"
xfdesktop --reload

echo -e '\nAll done'
