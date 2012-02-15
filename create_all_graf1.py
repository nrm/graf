#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys

from optparse import OptionParser

def main(s_dir):
    """docstring for main
    Создаем графики "скорость скана в сеансе" для всех файлов в дирктории /path/to/dir/obs
    """
    for w_dir in [ os.path.join(s_dir, x) for x in os.listdir(s_dir) if 'ruu' in x ]:
        for scan in [ os.path.join(w_dir, x) for x in os.listdir(w_dir) if '.tsuc' in x ]:
            print 'create graf %s'%scan
            os.chdir(w_dir)
            print os.getcwd()
            os.system('python /home/bezrukov/Envs/ersdb/graf_one.py %s'%scan)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = OptionParser()
        parser.add_option("--source", dest="s_dir",
                         help="source dir")

        #parser.add_option("--dest", dest="d_dir",
        #                 help="destination dir")

        (options, args) = parser.parse_args()
        if args:
            print 'try again, for help start with key: -h, --help '
            sys.exit()
        if options.s_dir:
            main(options.s_dir)
        else:
            print 'try again, for help start with key: -h, --help '
            sys.exit()
    else:
        print 'try again, for help start with key: -h, --help '


