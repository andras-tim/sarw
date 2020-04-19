#!/bin/bash
set -eufo pipefail

BASEDIR="$(dirname "$0")"
OUTDIR="${HOME}/Pictures/wallpapers/random"

LEFT_SUFFIX='_a-left.jpg'
RIGHT_SUFFIX='_b-right.jpg'
CENTER_SUFFIX='_c-center.jpg'
NAME_PREFIX="$(date +%Y-%V)"

OUTFILE_PREFIX="${OUTDIR}/${NAME_PREFIX}"
DOUBLE_PATH="${OUTFILE_PREFIX}.jpg"
LEFT_PATH="${OUTFILE_PREFIX}${LEFT_SUFFIX}"
RIGHT_PATH="${OUTFILE_PREFIX}${RIGHT_SUFFIX}"
CENTER_PATH="${OUTFILE_PREFIX}${CENTER_SUFFIX}"


function remove_current()
{
    local path="$1"

    if [ -e "${path}" ]; then
        echo "Removing current wallpapers... ${path}"
        rm "${path}"
    fi
}


# Main
if (( $# >= 1 )) && [ "$1" == '--new' ]; then
    remove_current "${DOUBLE_PATH}"
    remove_current "${LEFT_PATH}"
    remove_current "${RIGHT_PATH}"
    remove_current "${CENTER_PATH}"
    echo
    shift
fi

standalone_monitor_resolution='1920,1080'
if (( $# >= 1 )); then
    standalone_monitor_resolution="$1"
    shift
fi

left_of_multi_monitors_resolution='1920,1080'
if (( $# >= 1 )); then
    left_of_multi_monitors_resolution="$1"
    shift
fi

right_of_multi_monitors_resolution='1920,1080'
if (( $# >= 1 )); then
    right_of_multi_monitors_resolution="$1"
    shift
fi

padding_between_multi_monitors='0'
if (( $# >= 1 )); then
    padding_between_multi_monitors="$1"
    shift
fi

if [ ! -e "${LEFT_PATH}" ] || [ ! -e "${RIGHT_PATH}" ] || [ ! -e "${CENTER_PATH}" ]; then
    if [ ! -e "${DOUBLE_PATH}" ]; then
        mkdir -p "${OUTDIR}"

        python "${BASEDIR}/download-double-wide-wallpaper-from-wallpaperswide.py" "${DOUBLE_PATH}"
        echo
    fi

    python "${BASEDIR}/crop-wallpaper-for-multi-monitors.py" "${DOUBLE_PATH}" "${OUTFILE_PREFIX}" \
        "${LEFT_SUFFIX},auto,${left_of_multi_monitors_resolution}" \
        "${RIGHT_SUFFIX},${padding_between_multi_monitors},${right_of_multi_monitors_resolution}"

    python "${BASEDIR}/crop-wallpaper-for-multi-monitors.py" "${DOUBLE_PATH}" "${OUTFILE_PREFIX}" \
        "${CENTER_SUFFIX},auto,${standalone_monitor_resolution}"

    rm "${OUTFILE_PREFIX}.jpg"
    echo
fi

ln -sf "${NAME_PREFIX}${LEFT_SUFFIX}" "${OUTDIR}/last${LEFT_SUFFIX}"
ln -sf "${NAME_PREFIX}${RIGHT_SUFFIX}" "${OUTDIR}/last${RIGHT_SUFFIX}"
ln -sf "${NAME_PREFIX}${CENTER_SUFFIX}" "${OUTDIR}/last${CENTER_SUFFIX}"

python "${BASEDIR}/set-multi-xfce4-wallpapers.py" "${CENTER_PATH}" "${LEFT_PATH}" "${RIGHT_PATH}"
xfdesktop --reload

echo -e '\nAll done'
