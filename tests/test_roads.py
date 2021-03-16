#!/usr/bin/env python
# * coding: utf8 *
'''
test_facility.py
A module that tests the facility attribute rules
'''

import os

import arcpy
import pytest
from arcgisscripting import ExecuteError  # pylint: disable=no-name-in-module

table_name = 'Roads_Edit'
sde = os.path.join(os.path.dirname(__file__), '..', 'pro-project', 'localhost@utrans.sde')
TABLE = os.path.join(sde, table_name)
TEST_ATTRIBUTE = 'UTRANS_NOTES'

# pragma pylint: disable=no-member

rules = [
    'FULLNAME',
]


def cleanup():
    print('deleting test data')
    #arcpy.management.TruncateTable(TABLE)


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


#: name   posttype   postdir   expected_value
#: 100                 S         100 S
#: 100      RD         S         100 RD S
#: MAIN     ST                   MAIN ST
#: MAIN                          MAIN
#:          ST         S         (empty)

#: run test with all fields empty.
def test_fullname_empty():
    disabled_rule_value = 'rule disabled'
    calculated_attribute = 'FULLNAME'
    fields = ['NAME', 'POSTTYPE', 'POSTDIR', TEST_ATTRIBUTE]
    values = [
        [None, None, None, disabled_rule_value],
        ['', '', '', disabled_rule_value],
        [' ', ' ', ' ', disabled_rule_value]
    ]

    #: run the test with rules disabled - setup_function run by pytest disables the rules each time
    with arcpy.da.InsertCursor(TABLE, fields) as cursor:
        for value in values:
            cursor.insertRow(value)

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause=f"{TEST_ATTRIBUTE}='{disabled_rule_value}'") as cursor:
        for name, in cursor:
            assert name is None

    #: run the test with rules enabled - also enables the rules
    for rule in rules:
        arcpy.management.EnableAttributeRules(TABLE, rule)

    enabled_rule_value = 'rule enabled'
    values = [
    [None, None, None, enabled_rule_value],
    ['', '', '', enabled_rule_value],
    [' ', ' ', ' ', enabled_rule_value]
    ]

    with arcpy.da.InsertCursor(TABLE, fields) as cursor:
        for value in values:
            cursor.insertRow(value)

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause=f"{TEST_ATTRIBUTE}='{enabled_rule_value}'") as cursor:
        for name, in cursor:
            assert name is None



def test_fullname_missing_posttype():
    assert True == False

def test_fullname_missing_postdir():
    assert True == False

def test_fullname_missing_name():
    assert True == False

def test_fullname_has_all_required_fields():
    assert True == False




# def test_fullname_empty_calculation():
#     test_attribute = 'FacilityName'
#     calculated_attribute = 'GUID'
#     disabled_rule_value = '0'
#     enabled_rule_value = '1'

#     rule_name = 'Constant.Facility.Guid'

#     with arcpy.da.InsertCursor(TABLE, [test_attribute]) as cursor:
#         cursor.insertRow([disabled_rule_value])

#     with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, disabled_rule_value)) as cursor:
#         for name, in cursor:
#             assert name is None

#     arcpy.management.EnableAttributeRules(TABLE, rule_name)

#     with arcpy.da.InsertCursor(TABLE, [test_attribute]) as cursor:
#         cursor.insertRow([enabled_rule_value])

#     with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, enabled_rule_value)) as cursor:
#         for name, in cursor:
#             assert name is not None



# def test_domain_constraint():
#     test_attribute = 'FacilityName'
#     constraint_attribute = 'CountyFIPS'
#     disabled_rule_value = '0'
#     enabled_rule_value = '1'

#     rule_name = 'Constraint.Facility.FIPS'

#     with arcpy.da.InsertCursor(TABLE, [constraint_attribute, test_attribute]) as cursor:
#         cursor.insertRow([123, disabled_rule_value])

#     with arcpy.da.SearchCursor(TABLE, [constraint_attribute], where_clause="{}='{}'".format(test_attribute, disabled_rule_value)) as cursor:
#         print('searching for inserted value')
#         value, = next(cursor)
#         print('disabled value: {}'.format(value))
#         assert value == 123

#     arcpy.management.EnableAttributeRules(TABLE, rule_name)

#     with arcpy.da.InsertCursor(TABLE, [constraint_attribute, test_attribute]) as cursor:
#         print('inserting into table with enabled rule')
#         with pytest.raises(Exception):
#             #: too small
#             cursor.insertRow((49000, enabled_rule_value))

#     with arcpy.da.InsertCursor(TABLE, [constraint_attribute, test_attribute]) as cursor:
#         with pytest.raises(Exception):
#             #: too even
#             cursor.insertRow((49002, enabled_rule_value))

#     with arcpy.da.InsertCursor(TABLE, [constraint_attribute, test_attribute]) as cursor:
#         with pytest.raises(Exception):
#             #: too big
#             cursor.insertRow((49059, enabled_rule_value))

#     with arcpy.da.InsertCursor(TABLE, [constraint_attribute, test_attribute]) as cursor:
#         cursor.insertRow((49003, enabled_rule_value))

#     with arcpy.da.SearchCursor(TABLE, [constraint_attribute], where_clause="{}='{}'".format(test_attribute, enabled_rule_value)) as cursor:
#         print('searching for inserted value')
#         value, = next(cursor)
#         assert value == 49003
