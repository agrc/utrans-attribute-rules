#!/usr/bin/env python
# * coding: utf8 *
'''
rule.py
A module that acts as the base class for all rules
'''

import os

import arcpy
from arcgisscripting import ExecuteError  # pylint: disable=no-name-in-module


class RuleGroup():

    def __init__(self, sde, table, metas):
        self.name = table
        self.table_path = os.path.join(sde, table)
        self.meta_rules = metas

    def execute(self):
        print('creating rules for {}'.format(self.name))
        for rule in self.meta_rules:
            print('  creating {} rule'.format(rule.rule_name))

            exists = True

            args = {
                'in_table': self.table_path,
                'name': rule.rule_name,
                'script_expression': rule.arcade,
                'triggering_events': rule.triggers,
            }

            if hasattr(rule, 'error_number'):
                args['error_number'] = rule.error_number
                args['error_message'] = rule.error_message

            try:
                arcpy.management.AlterAttributeRule(**args)
                print('    updated')
            except Exception:
                exists = False

            if not exists:
                editable = 'EDITABLE'
                if rule.editable == 'no':
                    editable = 'NONEDITABLE'

                args = {
                    'in_table': self.table_path,
                    'name': rule.rule_name,
                    'type': rule.type,
                    'script_expression': rule.arcade,
                    'is_editable': editable,
                    'triggering_events': rule.triggers,
                    'description': rule.description,
                    'subtype': '',
                    'field': rule.field,
                    'exclude_from_client_evaluation': '',
                    'batch': False,
                    'severity': '',
                    'tags': rule.tag
                }

                if hasattr(rule, 'error_number'):
                    args['error_number'] = rule.error_number
                    args['error_message'] = rule.error_message

                try:
                    arcpy.management.AddAttributeRule(**args)
                    print('    created')
                except ExecuteError as e:
                    message, = e.args

                    if message.startswith('ERROR 002541'):
                        print('    rule already exists, skipping...')
                    else:
                        raise e

    def delete(self):
        for rule in self.meta_rules:
            print('  deleting {} rule'.format(rule.rule_name))
            try:
                arcpy.management.DeleteAttributeRule(
                    in_table=self.table_path,
                    names=rule.rule_name,
                    type=rule.type,
                )
                print('    deleted')
            except ExecuteError as e:
                message, = e.args

                if message.startswith('ERROR 002556'):
                    print('    rule already deleted, skipping...')
                else:
                    raise e
