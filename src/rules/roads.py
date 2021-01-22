#!/usr/bin/env python
# * coding: utf8 *
'''
well.py
A module that holds the rules for the roads
'''

from config import config
from models.ruletypes import Calculation, Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = 'Roads_Edit'
FOLDER = 'roads'

fullname_calculation = Calculation('Full Name', 'FULLNAME', load_rule_for(FOLDER, 'fullNameCalculation'))
fullname_calculation.triggers = [config.triggers.insert, config.triggers.update]

fromaddress_left_calculation = Calculation('From Address Left', 'FROMADDR_L', common.set_null_as_zero('FROMADDR_L'))
fromaddress_left_calculation.triggers = [config.triggers.insert, config.triggers.update]

fromaddress_right_calculation = Calculation('From Address Right', 'FROMADDR_R', common.set_null_as_zero('FROMADDR_R'))
fromaddress_right_calculation.triggers = [config.triggers.insert, config.triggers.update]

toaddress_left_calculation = Calculation('From Address Left', 'TOADDR_L', common.set_null_as_zero('TOADDR_L'))
toaddress_left_calculation.triggers = [config.triggers.insert, config.triggers.update]

toaddress_right_calculation = Calculation('From Address Right', 'TOADDR_R', common.set_null_as_zero('TOADDR_R'))
toaddress_right_calculation.triggers = [config.triggers.insert, config.triggers.update]

name_calculation = Calculation('Name', 'NAME', 'Upper(\'NAME\')')
alias_name_calculation = Calculation('Alias Name', 'A1_NAME', 'Upper(\'A1_NAME\')')
alias_alternate_name_calculation = Calculation('Alternate Alias Name', 'A2_NAME', 'Upper(\'A2_NAME\')')

predir_domain_constraint = Constraint('Prefix direction', 'PREDIR', common.constrain_to_domain('PREDIR', allow_null=True, domain='PreDirDomainName'))

RULES = [
    fullname_calculation,
    fromaddress_left_calculation,
    fromaddress_right_calculation,
    toaddress_left_calculation,
    toaddress_right_calculation,
    name_calculation,
    alias_name_calculation,
    alias_alternate_name_calculation,
    predir_domain_constraint
]
