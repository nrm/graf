#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import numpy as np
import sys
import datetime
#import cPickle
import os

#from numpy import exp, linspace
import matplotlib.pyplot as plt
import matplotlib.figure as fig


#решение проблемы с выводом на график русских шрифтов
from matplotlib import rcParams
rcParams['text.usetex']=False
rcParams['font.sans-serif'] = ['Liberation Sans']
rcParams['font.serif'] = ['Liberation Serif']


#размер легенды в графике
from matplotlib.font_manager import fontManager, FontProperties
#font= FontProperties(size='x-small');
font= FontProperties(size='small');

from optparse import OptionParser

"""
Рисует график средней скорости каждого скана сеанса
и создает xls файл для ручной правки
Example:
    python ../../../graf/src/graf_session.py --path1=../rue150/ --name=rue150_session.png
"""

def get_list_file(path, pattern='.tsuc'):
    """docstring for get_list_file
    Возвращаем список файлов в дирректории *.pattern
    """
    #print 'def get_list_file path = %s'%path
    return [x for x in os.listdir(path) if pattern in x]

def chenge_time(data):
    """ коныертируем время в виде
    %H:%M:%S,ms -> sec
    """
    try:
        arr=data.split(':')
        result = (float(arr[0])*3600) + (float(arr[1])*60) + (float(arr[2]))
    except:
        result = 0
    return result

def get_average_rate(log_file):
    """docstring for get_average_rate
    Вычисляем среднее значение скорости из файла и возвращаем его
    """
    #print 'def get_average_rate log_file = %s'%log_file
    with open(log_file, 'r') as F:
        for line in F:
            if 'throughput' in line:
                #return line.split()[-1] #TODO: выдергивание значения считаемого тсунами не точно
                time = [ chenge_time(line.split()[0]) for line in open(log_file) if len(line.split()) > 12 ]
                arr = [ float(line.split()[3].strip('Mbps')) for line in open(log_file) if len(line.split()) > 12 ]
                #return sum(arr)/len(arr)
                try:
                    return sum(arr)/len(arr), max(time)
                except:
                    print 'error'
                    return 0
        return 0 # bad file

def get_average_rate_session(w_dir, name_file):
    """docstring for get_average_rate_session"""
    aver_rate = []
    print w_dir
    count_scans=0
    for (count_scans, log_file) in enumerate( sorted(get_list_file(w_dir))):
        #[ aver_rate.append(x) for x in get_average_rate(os.path.join(w_dir, log_file)) if x==True ]
        result, time = get_average_rate(os.path.join(w_dir, log_file))
        if result:
            count_scans+=1
            print '\n time is %s\n'%time
            aver_rate.append(result)
        record_to_file(w_dir.split('/')[-3] + ' ' + log_file, result, count_scans, name_file)
    return aver_rate, count_scans

def record_to_file(log_file, rate, time,count_scans, name_file):
    """docstring for record_to_file
    Запись данных в файл для ручого построения в exele
    """
    with open('%s.xls'%name_file, 'a') as F: F.write('%s\t%s\t%s\t%s\n'%(log_file, rate, time, count_scans))

#основная функция для построения графика одной станции
def main(name_file='default.png', path='qwe'):
    """docstring for main
    Управление всем
    """
    fig1 = plt.figure(num = 0, figsize=(11, 4), linewidth = 1.0, frameon = True ,
            subplotpars=fig.SubplotParams(left=0.05, bottom=0.15, right=0.97, top=0.9))
    ax=fig1.add_subplot(111, autoscale_on=False)
    color=['r2-', 'g^-', 'bv-']
    x=0
    cur_path = path
    aver_rate=[]
    aver_time=[]
    count_scans=0
    for log_file in sorted(get_list_file(cur_path)):
        try:
            result, time = get_average_rate(os.path.join(cur_path, log_file))
        except:
            result=0
        if result:
            aver_rate.append(result)
            aver_time.append(time)
            count_scans+=1
            record_to_file(cur_path.split('/')[-3] + log_file, result, time, count_scans, name_file)
    ax.plot(aver_rate, color[x])
    x+=1

    plt.axis([1, count_scans-1, min(aver_rate)*0.9, max(aver_rate)*1.1]) # задание [xmin, xmax, ymin, ymax]
    sum_time = str((datetime.timedelta(seconds=int(sum(aver_time))))).split(':')
    plt.text(count_scans*0.07,
            max(aver_rate)*1.03,
            u'Общее время передачи данных сеанса: %sч %sм %sс\nСредняя скорость передачи данных: %sМб/с'%(sum_time[0],
                                                                sum_time[1],
                                                                sum_time[2],
                                                                int(sum(aver_rate)/len(aver_rate))),
                                                                horizontalalignment='left',
                                                                verticalalignment='center')
    #plt.axis('tight')

    plt.xlabel(u'Количество сканов сеанса - %s'%(count_scans))    # обозначение оси абсцисс
    plt.ylabel(u'Ср. скорость, Мбит/с')    # обозначение оси ординат
    plt.savefig(name_file, dpi=200)

def main2(name_file='default.png', path=[]):
    """docstring for main
    Управление всем
    """
    fig1 = plt.figure(num = 0, figsize=(11, 4), linewidth = 1.0, frameon = True ,
            subplotpars=fig.SubplotParams(left=0.05, bottom=0.15, right=0.97, top=0.9))
    ax=fig1.add_subplot(111, autoscale_on=True)
    #ax=fig1.add_subplot(111, autoscale_on=False)
    color=['ro-', 'g^-', 'bv-']
    x=0
    res_count_scans=[] # получим максимальное количество сканов
    for cur_path in path:
        print '\n\n path = %s'%cur_path
        aver_rate=[]
        aver_time=[]
        #count_scans=0
        for (count_scans, log_file) in enumerate( sorted(get_list_file(cur_path))):
            try:
                result, time = get_average_rate(os.path.join(cur_path, log_file))
            except:
                result=0
            if result:
                aver_rate.append(result)
                count_scans+=1
                aver_time.append(time)
                record_to_file(cur_path.split('/')[-3] + log_file, result, aver_time, count_scans, name_file)
        print type(count_scans), type(min(aver_rate)), type(max(aver_rate))
        print min(aver_rate), max(aver_rate)
        print count_scans
        ax.plot(aver_rate, color[x])
        x+=1
        res_count_scans.append(count_scans)


    count_scans=max(res_count_scans)
    ax.set_xticks((range(0, count_scans)))
    #plt.axis([1, count_scans, float(min(aver_rate)), (float(max(aver_rate)) + 5)])  # задание [xmin, xmax, ymin, ymax]
    #TODO: меняя число xmax добиваемся смещения правой границы!!!
    #plt.axis([1, count_scans-1, min(aver_rate)-30, (max(aver_rate) + 5)+5])  # задание [xmin, xmax, ymin, ymax]
    plt.xlim(1, count_scans-1)
    #plt.axis('tight')

    plt.xlabel(u'Номер скана')    # обозначение оси абсцисс
    plt.ylabel(u'Ср. скорость, Мбит/с')    # обозначение оси ординат

    if len(path)==2:
        plt.legend(['%s_%s'%(path[0].split('/')[-3], path[0].split('/')[-2]),
                    '%s_%s'%(path[1].split('/')[-3], path[1].split('/')[-2])],
                    loc='best')

    plt.savefig(name_file, dpi=200)

def main3(path1, path2, path3, name_file='default.png'):
    """docstring for main
    Управление всем
    """
    fig1 = plt.figure(num = 0, figsize=(11, 4), linewidth = 1.0, frameon = True ,
            subplotpars=fig.SubplotParams(left=0.05, bottom=0.15, right=0.97, top=0.9))
    ax=fig1.add_subplot(111, autoscale_on=True)

    color=['ro-', 'g^-', 'bv-']
    aver1,count_scans1=get_average_rate_session(path1, name_file)
    aver2,count_scans2=get_average_rate_session(path2, name_file)
    aver3,count_scans3=get_average_rate_session(path3, name_file)
    ax.plot(aver1, color[0])
    ax.plot(aver2, color[1])
    ax.plot(aver3, color[2])


    plt.xlabel(u'Номер скана')    # обозначение оси абсцисс
    plt.ylabel(u'Ср. скорость, Мбит/с')    # обозначение оси ординат

    plt.legend(['%s_%s'%(path1.split('/')[-3], path1.split('/')[-2]),
                '%s_%s'%(path2.split('/')[-3], path2.split('/')[-2]),
                '%s_%s'%(path3.split('/')[-3], path3.split('/')[-2])],    # список легенды
                loc='best',
                prop=font)

    print count_scans1, count_scans2, count_scans3
    count_scans=max( count_scans1, count_scans2, count_scans3)
    ax.set_xticks((range(1, count_scans)))
    plt.axis([1, count_scans-1, (min(min(aver1), min(aver2), min(aver3)) - 5), (max(max(aver1), max(aver2), max(aver3)) + 5)])  # задание [xmin, xmax, ymin, ymax]
    plt.savefig(name_file, dpi=200)



if __name__ == "__main__":
    if len(sys.argv) > 0:
        usage = "usage: %prog [options] arg1 arg2"
        parser = OptionParser(usage=usage)

        parser.add_option("--path1", dest="path1",
                         help="set full path to the session dir, for example /path/to/<session>")
        parser.add_option("--path2", dest="path2",
                         help="set full path to the session dir, for example /path/to/<session>")
        parser.add_option("--path3", dest="path3",
                         help="set full path to the session dir, for example /path/to/<session>")

        parser.add_option("--name", dest="name",
                         help="name graf file")

        (options, args) = parser.parse_args()
        if options:
            if options.path3:
                #main2(name_file=options.name, path=[options.path1, options.path2, options.path3])
                main3(path1=options.path1, path2=options.path2, path3=options.path3, name_file=options.name)
            elif options.path2 and not options.path3:
                main2(name_file=options.name, path=[options.path1, options.path2])
                #main_test(path=[options.path1, options.path2])
            else:
                main(name_file=options.name, path=options.path1)
        else:
            print 'try again, for help start with key: -h, --help '
            sys.exit()
    else:
        print 'try again, for help start with key: -h, --help '
