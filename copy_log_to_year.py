#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys

from optparse import OptionParser



def main(s_dir, d_dir):
    """docstring for main
    Разбор логов сессий ruu по годам
    """
    for obs in os.listdir(s_dir):
        obs_s_dir=os.path.join(s_dir, obs)
        for session in [ os.path.join(obs_s_dir, x) for x in os.listdir(obs_s_dir) if 'ruu' in x ]:
            #Получаем имя сессии
            year = [ x for x in os.listdir(session) if '.tsuc' in x ][0].split('-')[0]
            y_dir=os.path.join(d_dir, year)
            y_dir=os.path.join(y_dir, obs)
            w_dir=os.path.join(y_dir, session.split('/')[-1])
            if not os.path.exists(w_dir):
                os.makedirs(w_dir)
            for scan in [ os.path.join(session,x) for x in  os.listdir(session) if '.tsuc' in x]:
                #копируем каждый скан
                with open(scan, 'r') as F:
                    for line in F:
                        if 'throughput =' in line:
                            shutil.copy2(scan, w_dir)
                            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = OptionParser()
        parser.add_option("--source", dest="s_dir",
                         help="source dir")

        parser.add_option("--dest", dest="d_dir",
                         help="destination dir")

        (options, args) = parser.parse_args()
        if args:
            print 'try again, for help start with key: -h, --help '
            sys.exit()
        if options.s_dir and options.d_dir:
            main(options.s_dir, options.d_dir)
        else:
            print 'try again, for help start with key: -h, --help '
            sys.exit()
    else:
        print 'try again, for help start with key: -h, --help '


