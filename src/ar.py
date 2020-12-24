#!/usr/bin/env python
# * coding: utf8 *
"""
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
"""

import os
from datetime import datetime
from pathlib import Path

import arcpy
from arcgisscripting import ExecuteError  # pylint: disable=no-name-in-module
from docopt import docopt

from config.config import get_sde_path_for
from models.rule import RuleGroup
from rules import roads

VERSION = '1.0.0'


def get_rules(connection, specific_rule=None):
    if specific_rule == 'ALL':
        tables = [
            roads.TABLE,
        ]

        for table in tables:
            table = str(Path(connection) / table)
            attribute_rules = arcpy.Describe(table).attributeRules

            calculation_rules = ';'.join([ar.name for ar in attribute_rules if 'Calculation' in ar.type])
            constraint_rules = ';'.join([ar.name for ar in attribute_rules if 'Constraint' in ar.type])

            if calculation_rules:
                print('  deleting calculation rules: {}'.format(calculation_rules))
                try:
                    arcpy.management.DeleteAttributeRule(
                        in_table=table,
                        names=calculation_rules,
                        type='CALCULATION',
                    )
                    print('    deleted')
                except ExecuteError as error:
                    message, = error.args

                    if message.startswith('ERROR 002556'):
                        print('    rule already deleted, skipping...')
                    else:
                        raise error

            if constraint_rules:
                print('  deleting constraint rules {}'.format(constraint_rules))
                try:
                    arcpy.management.DeleteAttributeRule(
                        in_table=table,
                        names=constraint_rules,
                        type='CONSTRAINT',
                    )
                    print('    deleted')
                except ExecuteError as error:
                    message, = error.args

                    if message.startswith('ERROR 002556'):
                        print('    rule already deleted, skipping...')
                    else:
                        raise error

        return []

    roads_rules = RuleGroup(sde, roads.TABLE, roads.RULES)

    if specific_rule is None:
        return [roads_rules]

    rules = {'roads': roads_rules}

    return [rules[specific_rule]]


        date = datetime.datetime.now()
        date_string = str(date).split(' ')[0]
        cursor.insertRow(('attribute rules', version, date_string))


if __name__ == '__main__':
    '''Main entry point for program. Parse arguments and pass to engine module'''
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
