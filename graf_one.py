# -*- coding: utf-8 -*-

import sys
import os
import datetime

#from numpy import exp, linspace
import matplotlib.pyplot as plt
import matplotlib.figure as fig


#решение проблемы с выводом на график русских шрифтов
from matplotlib import rcParams
rcParams['text.usetex']=False
rcParams['font.sans-serif'] = ['Liberation Sans']
rcParams['font.serif'] = ['Liberation Serif']


class Create_of_Graf():
    """docstring for Create_of_Graf
    График скорости передачи 1 скана
    Example:
    >>> python graf_one.py target_file out_name.png
    >>>

    """
    def __init__(self, name_file, out_name):
        self.name_file=name_file
        self.out_name = out_name

    def chenge_time(self, data):
        """ коныертируем время в виде
        %H:%M:%S,ms -> sec
        """
        arr=data.split(':')
        result = (float(arr[0])*3600) + (float(arr[1])*60) + (float(arr[2]))
        return int(result)

    def create_dict(self, data_dict, line):
        """docstring for create_dict
        работает в генераторе
        Заполняю словарь передавая функции строку из генератора
        """
        data_dict['time'].append(self.chenge_time(line[0]))
        data_dict['rate'].append( int(float(line[3].strip('Mbps'))))
        data_dict['error'].append(line[13])

    def parser_tsuc(self, name_file):
        """docstring for parser_tsuc
        Открываем переданный файл парсим скорость(4 столбец)
        и выдаем список на выходе
        """
        data_dict={'time':[], 'rate':[], 'error':[]}
        arr = [ self.create_dict(data_dict, line.split()) for line in open(name_file) if len(line.split()) > 12 ]
        return data_dict

    def spec_arr(self, data):
        """docstring for spec_arr
        выборка 15 значений из массива
        """
        data=data[::-(len(data)/15)]
        data.sort()
        return data

    def my_plot(self, rate, time, name_file='name_of_plot.png'):
        """docstring for my_plot
        создаем график по входным данным данным
        и записываем в файл
        """
        fig1 = plt.figure(num = 0, figsize=(11, 4), linewidth = 1.0, frameon = True ,
                subplotpars=fig.SubplotParams(left=0.05, bottom=0.15, right=0.97, top=0.9))
        ax=fig1.add_subplot(111, autoscale_on=True)
        ax.plot(rate, 'b-', linewidth = 1.5)
        ax.set_xticks((range(0, len(time), (len(time)/15))))
        x_labels = ax.set_xticklabels((self.spec_arr(time)))
        plt.axis([0, len(time), min(rate)*4/5, max(rate)*5/4])  # задание [xmin, xmax, ymin, ymax]
        #plt.axis('tight')
        plt.xlabel(u'Время, с')    # обозначение оси абсцисс
        plt.ylabel(u'Скорость, Мбит/с')    # обозначение оси ординат
        aver = sum(rate, 0.0) / len(rate)
        end_time = str((datetime.timedelta(seconds=int(max(time))))).split(':')
        plt.text(max(time)*0.07,
                max(rate)*1.1,
                u'Средняя скорость передачи данных: %sМб/с\nВремя передачи данных: %sч %sм %sс'%(str(aver)[0:5],
                                                                end_time[0],
                                                                end_time[1],
                                                                end_time[2],),
                                                                horizontalalignment='left',
                                                                verticalalignment='center')
        plt.savefig(name_file, dpi=200)

    def main(self):
        """docstring for main
        центр программы - вызов методов
        """
        data=self.parser_tsuc(self.name_file)
        f1=name_file.split('/')
        #file_name=f1[-1].split('.')[0] + '_' + f1[-2] + '_' + f1[-3] + '.png'
        file_name = self.out_name
        if not os.path.isfile(file_name):
            self.my_plot(data['rate'], data['time'], name_file=file_name)
        else:
            file_name=file_name.split('.')[0] + '(1)'
            self.my_plot(data['rate'], data['time'], name_file=file_name)


if __name__ == '__main__':
    name_file=sys.argv[1]
    out_name=sys.argv[2]
    cls=Create_of_Graf(name_file, out_name)
    cls.main()
