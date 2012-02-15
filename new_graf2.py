#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import sys
import datetime
import cPickle
import os

#from numpy import exp, linspace
import matplotlib.pyplot as plt
import matplotlib.figure as fig


#решение проблемы с выводом на график русских шрифтов
from matplotlib import rcParams
rcParams['text.usetex']=False
rcParams['font.sans-serif'] = ['Liberation Sans']
rcParams['font.serif'] = ['Liberation Serif']


from optparse import OptionParser
"""
Рисуем графики из предварительно подготовленого файла-словаря( скриптом table_time.py)

на вход скрипту подается либо 1 файл либо 2
"""

def get_data(work_file):
    with open(work_file, 'r') as f:
        my_dict =  cPickle.load(f)
        print 'len %s = %s'%(work_file, len(my_dict))
        my_list = [(min(my_dict[x]), max(my_dict[x])) for x in sorted(my_dict) ]
        print my_list
        my={}
        for el in sorted(my_dict):
            #if not my_dict[el][0].year == 2009:
            q=sorted(my_dict[el])
            date=q[0].date().strftime("%d/%m/%y")
            delta=abs((q[-1] - q[0]).days*24*3600) + (q[-1]-q[0]).seconds
            y = q[0].timetuple()
            oposdanie = (q[0] - datetime.datetime(y.tm_year , y.tm_mon , y.tm_mday , y.tm_hour )).seconds
            if oposdanie > 2400: oposdanie = 0
            if delta < 15000 and len(q) > 15 and len(q) < 25:
                my[el] = ( date, (delta+oposdanie)/60, len(q) )
    print '\n\nmy = ', my
    return my


#-----------------------------GRAF___________________-------------#
def graf(data1, graf_file, data2=None):
    """docstring for graf"""
    fig1 = plt.figure(num = 0, figsize=(10, 4), linewidth = 1.0, frameon = True ,
                subplotpars=fig.SubplotParams(left=0.07, bottom=0.2, right=0.97, top=0.9))
    ax=fig1.add_subplot(111)

    N = len(data1)
    menMeans = [ data1[x][1] for x in sorted(data1) ]
    menStd = [data1[x][2] for x in sorted(data1)]

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    rects1 = ax.bar(ind+width, menMeans, width)

    if data2:
        N2 = len(data2)
        menMeans2 = [ data2[x][1] for x in sorted(data2) ]
        menStd2 = [data2[x][2] for x in sorted(data2)]
        ind2 = np.arange(N2)  # the x locations for the groups

        rects2 = ax.bar(ind2+width+width, menMeans2, width, color='r')

    ax.set_ylabel(u'Время, мин')
    ax.set_xlabel(u'Дата')
    #ax.set_title('Scores by group and gender', fontstyle='italic')
    ax.set_xticks(ind+width+width/2)
    group_labels =[ data1[x][0] for x in sorted(data1) ]
    ax.set_xticklabels(group_labels, rotation = 90, horizontalalignment='center', size='small')
    ###ax.set_axis([0, N, min(menMeans), max(menMeans) + 5])  # задание [xmin, xmax, ymin, ymax]
    ax.set_xlim(xmax=N)


    def autolabel(rects, values):
    # attach text labels - counts scans
        x = 0
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%d'%( values[x]),
                    ha='center', va='bottom', rotation='0', size='small', style='italic', color='black')
            x=x+1

    autolabel(rects1, menStd)

    if data2: autolabel(rects2, menStd2)

    plt.savefig(graf_file, dpi=200)



if __name__ == "__main__":
    if len(sys.argv) > 0:
        parser = OptionParser()
        parser.add_option("--file1", dest="file1",
                         help="set work file1")

        parser.add_option("--file2", dest="file2",
                         help="set work file")

        parser.add_option("--name", dest="name",
                         help="set name for graf file")

        (options, args) = parser.parse_args()
        if options:
            data=get_data(options.file1)
            if options.file2:
                data2=get_data(options.file2)
                data_1 = dict((k, v) for (k, v) in data.iteritems() if k in filter( lambda x: x  in data, data2 ))
                data_2 = dict((k, v) for (k, v) in data2.iteritems() if k in filter( lambda x: x  in data, data2 ))
                for key in sorted(data_1):
                    print 'data=%s\tvalue1=%s\tvalue2=%s'%(key, data_1[key], data_2[key])
                print len(data_1), len(data_2)
                graf(data_1, data2=data_2, graf_file=options.name)
            else:
                graf(data, graf_file=options.name)
        else:
            print 'try again, for help start with key: -h, --help '
            sys.exit()
    else:
        print 'try again, for help start with key: -h, --help '
