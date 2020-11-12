#!/usr/bin/env python
# * coding: utf8 *
'''
test_facility.py
A module that tests the facility attribute rules
'''

import os

import pytest
from arcgisscripting import ExecuteError  # pylint: disable=no-name-in-module

import arcpy

table_name = 'Roads_Edit'
sde = os.path.join(os.path.dirname(__file__), '..', 'pro-project', 'localhost.sde')
TABLE = os.path.join(sde, table_name)

# pragma pylint: disable=no-member

wkt = (
    'POLYGON ((419771.30999999959 4476140.9299999997, 421271.66000000015 4474303, 425713.20999999996 4477928.7599999998, 424212.86000000034 '
    '4479766.6799999997, 419771.30999999959 4476140.9299999997)), 26912)'
)

rules = [
    'rule.names',
]


def cleanup():
    print('deleting test data')
    with arcpy.da.UpdateCursor(TABLE, ['OID@'], where_clause="FacilityName IN ('0', '1')") as cursor:
        for _ in cursor:
            cursor.deleteRow()


def disable_rules(rules):
    print('disabling rules')
    for rule in rules:
        try:
            arcpy.management.DisableAttributeRules(TABLE, rule)
        except ExecuteError as e:
            print(e)
            message, = e.args

            if message.startswith('ERROR 002541'):
                print('rule does not exist {}'.format(rule))
                pass

    arcpy.management.ClearWorkspaceCache(sde)


def setup_function():
    '''function setup'''
    cleanup()
    disable_rules(rules)


def teardown_function():
    '''function teardown'''
    cleanup()


def test_guid_calculation():
    test_attribute = 'FacilityName'
    calculated_attribute = 'GUID'
    disabled_rule_value = '0'
    enabled_rule_value = '1'

    rule_name = 'Constant.Facility.Guid'

    with arcpy.da.InsertCursor(TABLE, [test_attribute]) as cursor:
        cursor.insertRow([disabled_rule_value])

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, disabled_rule_value)) as cursor:
        for name, in cursor:
            assert name is None

    arcpy.management.EnableAttributeRules(TABLE, rule_name)

    with arcpy.da.InsertCursor(TABLE, [test_attribute]) as cursor:
        cursor.insertRow([enabled_rule_value])

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, enabled_rule_value)) as cursor:
        for name, in cursor:
            assert name is not None


def test_calculation():
    test_attribute = 'FacilityName'
    calculated_attribute = 'FacilityState'
    disabled_rule_value = '0'
    enabled_rule_value = '1'

    rule_name = 'Constant.Facility.State'

    with arcpy.da.InsertCursor(TABLE, [test_attribute, 'SHAPE@WKT']) as cursor:
        cursor.insertRow([disabled_rule_value, wkt])

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, disabled_rule_value)) as cursor:
        for value, in cursor:
            print('disabled value: {}'.format(value))
            assert value is None

    arcpy.management.EnableAttributeRules(TABLE, rule_name)

    with arcpy.da.InsertCursor(TABLE, [test_attribute]) as cursor:
        cursor.insertRow([enabled_rule_value])

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, enabled_rule_value)) as cursor:
        for value, in cursor:
            assert value == 'UT'


def test_domain_constraint():
    test_attribute = 'FacilityName'
    constraint_attribute = 'CountyFIPS'
    disabled_rule_value = '0'
    enabled_rule_value = '1'

    rule_name = 'Constraint.Facility.FIPS'

    with arcpy.da.InsertCursor(TABLE, [constraint_attribute, test_attribute]) as cursor:
        cursor.insertRow([123, disabled_rule_value])

    with arcpy.da.SearchCursor(TABLE, [constraint_attribute], where_clause="{}='{}'".format(test_attribute, disabled_rule_value)) as cursor:
        print('searching for inserted value')
        value, = next(cursor)
        print('disabled value: {}'.format(value))
        assert value == 123

    arcpy.management.EnableAttributeRules(TABLE, rule_name)

    with arcpy.da.InsertCursor(TABLE, [constraint_attribute, test_attribute]) as cursor:
        print('inserting into table with enabled rule')
        with pytest.raises(Exception):
            #: too small
            cursor.insertRow((49000, enabled_rule_value))

    with arcpy.da.InsertCursor(TABLE, [constraint_attribute, test_attribute]) as cursor:
        with pytest.raises(Exception):
            #: too even
            cursor.insertRow((49002, enabled_rule_value))

    with arcpy.da.InsertCursor(TABLE, [constraint_attribute, test_attribute]) as cursor:
        with pytest.raises(Exception):
            #: too big
            cursor.insertRow((49059, enabled_rule_value))

    with arcpy.da.InsertCursor(TABLE, [constraint_attribute, test_attribute]) as cursor:
        cursor.insertRow((49003, enabled_rule_value))

    with arcpy.da.SearchCursor(TABLE, [constraint_attribute], where_clause="{}='{}'".format(test_attribute, enabled_rule_value)) as cursor:
        print('searching for inserted value')
        value, = next(cursor)
        assert value == 49003
