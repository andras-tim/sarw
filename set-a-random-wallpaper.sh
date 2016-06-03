#!/bin/bash
set -e

BASEDIR="$(dirname "$0")"
OUTDIR="${HOME}/Pictures/wallpapers/random"
NAME_PREFIX="$(date +%Y-%V)"
OUTFILE_PREFIX="${OUTDIR}/${NAME_PREFIX}"

# Main
mkdir -p "${OUTDIR}"

python "${BASEDIR}/download-random-double-wide-wallpaper.py" "${OUTFILE_PREFIX}.jpg" "$@"
echo

python "${BASEDIR}/crop-wallpaper-for-multi-monitors.py" "${OUTFILE_PREFIX}.jpg" "${OUTFILE_PREFIX}"
rm "${OUTFILE_PREFIX}.jpg"
ln -sf "${NAME_PREFIX}_a-left.jpg" "${OUTDIR}/last_a-left.jpg"
ln -sf "${NAME_PREFIX}_b-right.jpg" "${OUTDIR}/last_b-right.jpg"
ln -sf "${NAME_PREFIX}_c-center.jpg" "${OUTDIR}/last_c-center.jpg"
echo

python "${BASEDIR}/set-multi-xfce4-wallpapers.py" "${OUTFILE_PREFIX}_c-center.jpg" "${OUTFILE_PREFIX}_a-left.jpg" "${OUTFILE_PREFIX}_b-right.jpg"
xfdesktop --reload

echo -e '\nAll done'
