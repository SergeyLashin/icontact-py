# -*- coding: utf-8 -*-
""" Test data for iContact API Client tests """

import random
import string

test_contact_names = [u''.join(random.sample((string.ascii_letters) * 42, 7)) for n in range(3)]
test_lists_names = [u''.join(random.sample((string.ascii_letters) * 42, 12)) for n in range(3)]
test_customfields_names = [u''.join(random.sample((string.ascii_lowercase) * 42, 17))]

test_contacts = [
    {
        'email': u'%s@example.com' % test_contact_names[0],
        'firstName': u'Unit Tester',
        'lastName': u'%s' % test_contact_names[0]
    },
    {
        'email': u'%s@example.com' % test_contact_names[1],
        'firstName': u'Unit Tester',
        'lastName': u'%s' % test_contact_names[1]
    },
    {
        'email': u'%s@example.com' % test_contact_names[2],
        'firstName': u'Unit Tester',
        'lastName': u'%s' % test_contact_names[2]
    },
]

test_lists = [
    {
        'name': u'%s' % test_lists_names[0],
        'description': u'Test List %s' % test_lists_names[0],
        'emailOwnerOnChange': 0,
        'welcomeOnManualAdd': 0,
        'welcomeOnSignupAdd': 1,
        #'welcomeMessageId': 999,
    },
    {
        'name': u'%s' % test_lists_names[1],
        'description': u'Test List %s' % test_lists_names[1],
        'emailOwnerOnChange': 0,
        'welcomeOnManualAdd': 0,
        'welcomeOnSignupAdd': 1,
    },
    {
        'name': u'%s' % test_lists_names[2],
        'description': u'Test List %s' % test_lists_names[2],
        'emailOwnerOnChange': 0,
        'welcomeOnManualAdd': 0,
        'welcomeOnSignupAdd': 1,
    },
]

test_customfields = [
    {
        'privateName': u'%s' % test_customfields_names[0],
        'publicName': u'Field %s' % test_customfields_names[0],
        #'fieldType': u'checkbox',
        'fieldType': u'text',
        'displayToUser': 0,
    },
]

