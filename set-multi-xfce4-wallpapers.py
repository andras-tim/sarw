#!/usr/bin/env python

import re
import subprocess
import sys

OUTPUT_POSITIONS = {
    'DP2': 'left',
    'DP3': 'right',
}


class Xrandr(object):
    OUTPUT_PATTERN = re.compile('^(?P<name>[^ ]+) (?P<state>[^ ]+) (|(?P<options>[^(]+) )\(.*$')

    @classmethod
    def run_xrandr(cls):
        stdout = subprocess.check_output(['xrandr']).decode("utf-8")
        return stdout.splitlines()

    @classmethod
    def get_outputs(cls):
        lines = cls.run_xrandr()

        outputs = []
        for line in lines:
            matches = Xrandr.OUTPUT_PATTERN.match(str(line))
            if matches:
                outputs.append(matches.groupdict())

        return outputs

    @classmethod
    def get_connected_outputs(cls):
        return [output for output in cls.get_outputs() if output['state'] == 'connected']

    @classmethod
    def get_active_outputs(cls):
        return [output for output in cls.get_connected_outputs() if output['options']]


class Desktop(object):
    @classmethod
    def set_wallpaper(cls, output_name, wallpaper_path):
        print('Set wallpaper of {output_name!r} to {wallpaper_path!r}'.format(
            output_name=output_name,
            wallpaper_path=wallpaper_path,
        ))

        cls._run_set_wallpaper(output_name, None)
        cls._run_set_wallpaper(output_name, wallpaper_path)

    @classmethod
    def _run_set_wallpaper(cls, output_name, wallpaper_path):
        subprocess.check_call([
            'xfconf-query',
            '-c', 'xfce4-desktop',
            '-p', '/backdrop/screen0/monitor{output_name}/workspace0/last-image'.format(output_name=output_name),
            '-n',
            '-t', 'string',
            '-s', '' if wallpaper_path is None else wallpaper_path,
        ])


def main(*args):
    def get_wallpaper_for_output(output_name):
        wallpaper_id = OUTPUT_POSITIONS.get(output_name, 'common')
        return wallpapers[wallpaper_id]

    wallpapers = {
        'common': args[0],
        'left': args[1] if len(args) >= 3 else args[0],
        'right': args[2] if len(args) >= 3 else args[0],
    }

    # outputs = Xrandr.get_active_outputs()
    outputs = Xrandr.get_outputs()
    for output in outputs:
        wallpaper_path = get_wallpaper_for_output(output['name'])
        Desktop.set_wallpaper(output['name'], wallpaper_path)


if __name__ == '__main__':
    main(*sys.argv[1:])
