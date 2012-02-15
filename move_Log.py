#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil


thedir='/opt/m5data/'
old_dir='/opt/m5data/Log'
logdir=os.path.join(thedir, 'auto_Log2')


def create_dir( name_dir):
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)


def get_list_obs(thedir, pattern=['bd', 'zc', 'sv']):
    return [ os.path.join(thedir, name) for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) and name in pattern ]

def get_list_obs2(thedir, pattern=['bd', 'zc', 'sv']):
    return [ os.path.join(thedir, name) for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) and name in pattern ]


def get_list_seance(obs):
    return [ os.path.join(obs, x) for x in os.listdir(obs) if os.path.isdir(os.path.join(obs, x)) ]


def get_list_seance2(work_dir=old_dir):
    return [ os.path.join(work_dir, x) for x in os.listdir(work_dir) if os.path.isdir(os.path.join(work_dir, x)) ]

def cope_data_in_log(name_seance, obs):
    """
    Copy *.tsuc in Log/name_seance
    """
    _dir = os.path.join(obs.split('/')[-1], name_seance.split('/')[-1])
    work_dir = os.path.join(logdir, _dir)
    if not os.path.exists(work_dir):
        create_dir(work_dir)
    [ shutil.copy2(os.path.join(name_seance, x), os.path.join(work_dir, x) ) for x in os.listdir(name_seance) if os.path.isfile(os.path.join(name_seance, x)) and '.tsuc' in x ]

def move_data_to_log(name_seance, obs):
    """docstring for move_data_to_log"""
    _dir = os.path.join(obs.split('/')[-1], name_seance.split('/')[-1])
    work_dir = os.path.join(logdir, _dir)
    print 'work_dir = ', work_dir
    print 'name_seance = ', name_seance
    print 'obs = ', obs
    if not os.path.exists(work_dir):
        create_dir(work_dir)
    [ shutil.copy2(os.path.join(obs, x), os.path.join(work_dir, x) ) for x in os.listdir(obs) if os.path.isfile(os.path.join(obs, x)) and '.tsuc' in x ]


if __name__ == "__main__":
    create_dir(logdir)
    for name_seance in get_list_seance2():
        for obs in get_list_obs2(name_seance):
            move_data_to_log(name_seance, obs)

