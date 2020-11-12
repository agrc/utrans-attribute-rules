#!/usr/bin/env python
# * coding: utf8 *
'''
config.py
A module that stores common items for attribute rules
'''
import os
from collections import namedtuple

Triggers = namedtuple('Triggers', 'insert update delete')
triggers = Triggers('INSERT', 'UPDATE', 'DELETE')

Rules = namedtuple('Rules', 'calculation constraint')
rule_types = Rules('CALCULATION', 'CONSTRAINT')

Editable = namedtuple('Editable', 'yes no')
editable = Editable('yes', 'no')


def get_sde_path_for(env=None):
    sde = os.path.join(os.path.dirname(__file__), '..', '..', 'pro-project')

    if env is None:
        return os.path.join(sde, 'the-path-to-your-development-sde-file-inside-the-pro-project-folder.sde')

    if env == 'local':
        return os.path.join(sde, 'localhost@utrans.sde')

    if env == 'dev':
        return os.path.join(sde, 'stage@utrans.sde')

    if env == 'prod':
        return os.path.join(sde, 'prod@utrans.sde')

    raise Exception('{} env not found'.format(env))
