#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os , re
import datetime
import sys
import cPickle

from optparse import OptionParser
"""
Подготовка файла (словарь и xls), из директорий сеансов вида '/path/to/dir/%s/%s'%(obs, pattern=[ruu, rue, *])
файлы сохраняются в той директории в которой запускаются
"""

def D(path):
#def D(path, pattern):
    dd = {}
    for dir in [x for x in os.listdir(path)]:
    #for dir in [x for x in os.listdir(path) if '.' not in x and 'e-vlbi' not in x and re.search(pattern, x) and 'bad' not in x]:
        dd[dir]= [ datetime.datetime.strptime(z, "%Y-%m-%d-%H-%M-%S") for z in [ x.split('.')[0] for x in os.listdir('%s/%s'%(path, dir)) if re.search('tsuc', x) ]]
        [ dd.pop(x) for x in dd.keys() if dd[x] == [] ]
    return dd

def my_print(result_dict):
    print sorted(result_dict.keys()), '\n'
    for el in sorted(result_dict):
        q=sorted(result_dict[el])
        print q[-1]-q[0], '\t', len(q)

def record(dict, out_name):
    with open('%s.xls'%(out_name), 'w') as f:
        for el in sorted(dict):
            q=sorted(dict[el])
            date=q[0].date().strftime("%d/%m/%y")
            delta=abs((q[-1] - q[0]).days*24*3600) + (q[-1]-q[0]).seconds
            y = q[0].timetuple()
            oposdanie = (q[0] - datetime.datetime(y.tm_year , y.tm_mon , y.tm_mday , y.tm_hour )).seconds
            #if oposdanie > 2400: oposdanie = 0
            #if delta < 20000:
            f.write('%s\t%s\t%s\t%s\n'%(el, date, delta+oposdanie, len(q)))

def record2(dict, out_name):
    with open('%s_Dict'%(out_name), 'w') as f:
        cPickle.dump(dict, f)


if __name__ == "__main__":
    if len(sys.argv) > 0:
        parser = OptionParser()
        parser.add_option("--path", dest="path", default="/opt/m5data/",
                         help="set path to the list seance dir, default is /opt/m5data/")

        #parser.add_option("--obs", dest="obs",
        #                 help="set mask for recognize seance dir, equal to [bd, zc, sv, ...]")

        #parser.add_option("--pattern", dest="pattern",
        #                 help="set pattern/ for seance, equal to [ruu, rue, ruf, ...]")

        parser.add_option("--name", dest="name",
                         help="name out file")

        (options, args) = parser.parse_args()
        if options:
            x = D(path=options.path)
            #x = D( path=os.path.join(options.path,options.obs), pattern=options.pattern)
            my_print(x)
            record(x, options.name)
            record2(x, options.name)

        else:
            print 'try again, for help start with key: -h, --help '
            sys.exit()
    else:
        print 'try again, for help start with key: -h, --help '
