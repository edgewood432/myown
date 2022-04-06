#!/usr/bin/python3

import sys
import inotify.adapters

from lib import Kuba


myname = sys.argv[0].split('/')[-1]
log = Kuba.MyLogger('inotify.log')
i = inotify.adapters.InotifyTree('/vol1/income')

for event in i.event_gen(yield_nones=False):
    (header, type_names, path, filename) = event

    if 'IN_CLOSE_WRITE' in type_names:
        log.writeLog(1, f'{myname} - found new file: {filename} in {path}')

        kwargs = {'file': filename, 'path': path}

        Kuba.Kuba(**kwargs).start_work()
