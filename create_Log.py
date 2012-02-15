#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil


thedir='/opt/m5data'
logdir=os.path.join(thedir, 'auto_Log')


def create_dir( name_dir):
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)


def get_list_obs(thedir, pattern=['bd', 'zc', 'sv']):
    return [ os.path.join(thedir, name) for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) and name in pattern ]


def get_list_seance(obs):
    return [ os.path.join(obs, x) for x in os.listdir(obs) if os.path.isdir(os.path.join(obs, x)) ]


def cope_data_in_log(name_seance, obs):
    """
    Copy *.tsuc in Log/name_seance
    """
    _dir = os.path.join(obs.split('/')[-1], name_seance.split('/')[-1])
    work_dir = os.path.join(logdir, _dir)
    if not os.path.exists(work_dir):
        create_dir(work_dir)
    [ shutil.copy2(os.path.join(name_seance, x), os.path.join(work_dir, x) ) for x in os.listdir(name_seance) if os.path.isfile(os.path.join(name_seance, x)) and '.tsuc' in x ]



if __name__ == "__main__":
    create_dir(logdir)
    for obs in get_list_obs(thedir, pattern=['bd', 'zc', 'sv']):
        for name_seance in get_list_seance(obs):
            cope_data_in_log(name_seance, obs)

