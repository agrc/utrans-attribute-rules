#!/usr/bin/env python
# * coding: utf8 *
'''
ar

Usage:
    ar update [--env=<env>]
    ar delete [--env=<env>]
    ar --version
    ar (-h | --help)

Options:
    --env=<env>     local, dev, prod
    -h --help       Shows this screen
    -v --version    Shows the version
'''

import os
from datetime import datetime

from arcgisscripting import ExecuteError  # pylint: disable=no-name-in-module
from docopt import docopt

import arcpy
from config.config import get_sde_path_for
from models.rule import RuleGroup
from rules import roads

VERSION = '1.0.0'

def get_rules(sde):
    roads_rules = RuleGroup(sde, roads.TABLE, roads.RULES)

    rules = {
        'roads': roads_rules,
    }

    return [rules]


def update_version(sde, version):
    with arcpy.da.InsertCursor(in_table=os.path.join(sde, 'Version_Information'), field_names=['name', 'version', 'date']) as cursor:
        date = datetime.datetime.now()
        date_string = str(date).split(' ')[0]
        cursor.insertRow(('attribute rules', version, date_string))


if __name__ == '__main__':
    '''Main entry point for program. Parse arguments and pass to engine module
    '''
    args = docopt(__doc__, version=VERSION)

    sde = get_sde_path_for(args['--env'])
    print('acting on {}'.format(sde))

    if not arcpy.TestSchemaLock(os.path.join(sde, roads.TABLE)):
        print('Unable to reach the database or acquire the necessary schema lock to add rules')
        exit(0)

    if args['update']:
        for rule in get_rules(sde):
            rule.execute()

        update_version(sde, VERSION)
    elif args['delete']:
        for rule in get_rules(sde):
            rule.delete()

    arcpy.management.ClearWorkspaceCache(sde)
