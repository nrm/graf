#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

#from numpy import exp, linspace
import matplotlib.pyplot as plt
import matplotlib.figure as fig


#решение проблемы с выводом на график русских шрифтов
from matplotlib import rcParams
rcParams['text.usetex']=False
rcParams['font.sans-serif'] = ['Liberation Sans']
rcParams['font.serif'] = ['Liberation Serif']


import numpy as np

from optparse import OptionParser

import datetime
import matplotlib
import cPickle

def get_data(work_file):
    with open(work_file, 'r') as f:
        my_dict =  cPickle.load(f)
        my_list = [(min(my_dict[x]), max(my_dict[x])) for x in sorted(my_dict) ]
        my={}
        for el in my_dict:
            if (max(my_dict[el]) - min(my_dict[el])).seconds < 21600:
                my[el]=( max(my_dict[el]).date()).strftime("%d/%m/%y"), ((max(my_dict[el]) - min(my_dict[el])).seconds)/60, len(my_dict[el])
    return my


#-----------------------------GRAF___________________-------------#
def graf(data, graf_file):
    """docstring for graf"""
    fig1 = plt.figure(num = 0, figsize=(10, 4), linewidth = 1.0, frameon = True ,
                subplotpars=fig.SubplotParams(left=0.07, bottom=0.2, right=0.97, top=0.9))
    ax=fig1.add_subplot(111)

    N = len(data)
    menMeans = [ data[x][1] for x in sorted(data) ]
    menStd = [data[x][2] for x in sorted(data)]
#    print 'N = ', N
#    print 'count = ',len(menStd)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.55       # the width of the bars

    rects1 = ax.bar(ind+width, menMeans, width)

    ax.set_ylabel('Time, min')
    ax.set_xlabel('Date')
    ax.set_title('Scores by group and gender', fontstyle='italic')
    ax.set_xticks(ind+width)
    group_labels =[ data[x][0] for x in sorted(data) ]
    ax.set_xticklabels(group_labels, rotation = 90, horizontalalignment='center', size='small')
#    fig1.autofmt_xdate()

    def autolabel(rects, values, name_seance):
    # attach text labels - counts scans
        x = 0
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%d'%( values[x]),
                    ha='center', va='bottom', rotation='0', size='small', style='italic', color='g')
            x=x+1

    autolabel(rects1, menStd, sorted(data))

    plt.savefig(graf_file, dpi=200)



if __name__ == "__main__":
    if len(sys.argv) > 0:
        parser = OptionParser()
        parser.add_option("--file", dest="file",
                         help="set work file")

        (options, args) = parser.parse_args()
        if options:
            data=get_data(options.file)
#            for el in sorted(data):
#                print 'data[%s] = (data = %s, timedelta = %s, count = %s)'%(el, data[el][0], data[el][1], data[el][2] )
            graf(data, graf_file=options.file)

        else:
            print 'try again, for help start with key: -h, --help '
            sys.exit()
    else:
        print 'try again, for help start with key: -h, --help '
