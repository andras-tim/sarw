#!/usr/bin/env python

import os
import re
import subprocess
import sys

"""
Get current settings from the system:

``` sh
xfconf-query --channel xfce4-desktop --list \
    | grep last-image \
        | while read -r a; do
            echo -e "$a\t$(xfconf-query --channel xfce4-desktop --property "$a")"
        done
```
"""

MONITOR_POSITIONS = {
    'monitor0': 'left',
    'monitor1': 'right',
    # 'monitor2': 'right',
}


class Desktop(object):
    WORKSPACE_PATH_TEMPLATE = re.compile(
        r'^/backdrop/(?P<screen>screen[^/]*)/(?P<monitor>monitor[^/]*)/(?P<workspace>workspace[^/]*)/.*$'
    )

    @classmethod
    def get_workspaces(cls):
        paths = cls._xfconf_query_desktop(
            '--property', '/backdrop',
            '--list',
        )

        workspaces = {}
        for path in paths:
            matches = cls.WORKSPACE_PATH_TEMPLATE.match(path)
            if matches is not None:
                matches_dict = matches.groupdict()
                workspaces[','.join(matches_dict.values())] = matches_dict

        return sorted(workspaces.values())

    @classmethod
    def set_wallpaper(cls, wallpaper_path, **workspace):
        print('Set wallpaper of {screen}/{monitor}/{workspace} to {wallpaper_path!r}'.format(
            wallpaper_path=wallpaper_path,
            **workspace
        ))

        cls._run_set_wallpaper(wallpaper_path=None, **workspace)
        cls._run_set_wallpaper(wallpaper_path=wallpaper_path, **workspace)

    @classmethod
    def _run_set_wallpaper(cls, screen, monitor, workspace, wallpaper_path):
        path = '/backdrop/{screen}/{monitor}/{workspace}/last-image'.format(
            screen=screen, monitor=monitor, workspace=workspace)

        cls._xfconf_query_desktop(
            '--create',
            '--property', path,
            '--type', 'string',
            '--set', '' if wallpaper_path is None else wallpaper_path,
        )

    @classmethod
    def _xfconf_query_desktop(cls, *arguments):
        command = ['xfconf-query', '--channel', 'xfce4-desktop']
        command.extend(arguments)

        raw_output = subprocess.check_output(command)
        return raw_output.decode("utf-8").splitlines()


def main(*args):
    def get_wallpaper_for_output(output_name):
        wallpaper_id = MONITOR_POSITIONS.get(output_name, 'common')
        return wallpapers[wallpaper_id]

    wallpapers = {
        'common': os.path.abspath(args[0]),
        'left': os.path.abspath(args[1] if len(args) >= 3 else args[0]),
        'right': os.path.abspath(args[2] if len(args) >= 3 else args[0]),
    }

    workspaces = Desktop.get_workspaces()
    for workspace in workspaces:
        wallpaper_path = get_wallpaper_for_output(workspace['monitor'])
        Desktop.set_wallpaper(wallpaper_path=wallpaper_path, **workspace)


if __name__ == '__main__':
    main(*sys.argv[1:])
