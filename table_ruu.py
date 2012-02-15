#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil


thedir='/opt/m5data'
logdir=os.path.join(thedir, 'auto_Log')


def create_dir( name_dir):
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)


def get_list_obs(thedir, pattern=['bd', 'zc']):
    return [ os.path.join(thedir, name) for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) and name in pattern ]


def get_list_seance(obs, pattert='ruu'):
    #return [ os.path.join(obs, x) for x in os.listdir(obs) if os.path.isdir(os.path.join(obs, x)) and pattert in x.split('/')[-1][:4]]
    return [ os.path.join(obs, x) for x in os.listdir(obs) if os.path.isdir(os.path.join(obs, x)) ]

def table_ruu(name_seance, obs):
    """docstring for table_ruu"""
    _dir = os.path.join(obs.split('/')[-1], name_seance.split('/')[-1])
    work_dir = os.path.join(logdir, _dir)
    print 'work_dir = ',work_dir
    write_file='table_ruu_%s'%obs.split('/')[-1]+'.xls'
    print 'write_file = %s'%write_file
    with open(write_file, 'a') as F:
        try:
            F.write('%s\t%s\n'%(os.listdir(work_dir)[0][:10], name_seance.split('/')[-1]))
        except IndexError:
            print 'list index out of range %s'%name_seance.split('/')[-1]



if __name__ == "__main__":
    #create_dir(logdir)
    for obs in get_list_obs(logdir, pattern=[ 'zc']):
        print 'obs = ', obs
        for name_seance in sorted(get_list_seance(obs)):
            print '\nsession = ',name_seance
            table_ruu(name_seance, obs)

