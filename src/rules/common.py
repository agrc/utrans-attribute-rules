#!/usr/bin/env python
# * coding: utf8 *
'''
common.py
A module that holds common arcade expressions
'''

ALLOW_EMPTY = '''if (!haskey($feature, '{0}') || isempty($feature.{0})) {{
    return true;
}}

return iif (isempty(domainname($feature, '{0}', $feature.{0})), {{
    'errorMessage': '{0} may not be empty; select the appropriate value from the{1} (dropdown menu). Input: ' + $feature.{0}
}}, true);'''

NO_EMPTY = '''if (!haskey($feature, '{0}')) {{
    return true;
}}

return iif (isempty(domainname($feature, '{0}', $feature.{0})), {{
    'errorMessage': '{0} may not be empty; select the appropriate value from the{1} (dropdown menu). Input: ' + $feature.{0}
}}, true);'''

REQUIRED = '''if (!haskey($feature, '{0}')) {{
    return true;
}}

return iif(isempty($feature.{0}) || lower($feature.{0}) == '<null>', {{
    'errorMessage': '{0} must not be empty.'
}}, true);'''

CONVERT_NULL_TO_ZERO = '''
IIf(isempty($feature.{0}) || $feature.{0} == <null>, '0', true);
'''


def constrain_to_domain(field, allow_null=True, domain=None):
    if domain is None:
        domain = ' '
    else:
        domain = ' ' + domain

    if allow_null:
        return ALLOW_EMPTY.format(field, domain)

    return NO_EMPTY.format(field, domain)


def constrain_to_required(field):
    return REQUIRED.format(field)


def set_null_as_zero(field):
    return CONVERT_NULL_TO_ZERO.format(field)
