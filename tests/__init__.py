# -*- coding: utf-8 -*-

import pprint

from unittest import TestCase
from nose.tools import assert_equal, assert_true

import icontact

__all__ = ['TestCase', 'assert_equal', 'assert_true', 'icontact',
           'ICONTACT_SETTINGS', 'get_ic_client', 'nprint']

ICONTACT_SETTINGS = {
    'user_name': '<user name>',
    'app_id': '<app id>',
    'app_password': '<app password>',
    'version': '2.2',
    'base_url': 'https://app.sandbox.icontact.com/icp',
    'account_id': '<account id>',
    'clientfolder_id': '<client folder id>'
}

def get_ic_client():
    return icontact.IContactClient(
            user_name=ICONTACT_SETTINGS['user_name'],
            app_id=ICONTACT_SETTINGS['app_id'],
            app_password=ICONTACT_SETTINGS['app_password'],
            version=ICONTACT_SETTINGS['version'],
            base_url=ICONTACT_SETTINGS['base_url'],
            account_id=ICONTACT_SETTINGS['account_id'],
            clientfolder_id=ICONTACT_SETTINGS['clientfolder_id'])

def nprint(data):
    print '\n>>>'
    pprint.pprint(data)
    print '>>>'

