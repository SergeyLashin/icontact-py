# -*- coding: utf-8 -*-

from icontact.tests import *

from data import *

class ClientTests(TestCase):
    """
        Tests for iContact API Client
        =============================
    """

    def test_get_time_call(self):
        """
            Test time call
        """

        ic_client = get_ic_client()

        response = ic_client.get('time')
        nprint(response)

        assert_true('time' in response)
        assert_true('timestamp' in response)

    def test_get_accounts_call(self):
        """
            Test accounts call
        """
        ic_client = get_ic_client()

        response = ic_client.get('accounts')
        nprint(response)

        assert_equal(response['accounts'][0]['accountId'], ICONTACT_SETTINGS['account_id'])

        response = ic_client.get('accounts', [ICONTACT_SETTINGS['account_id']])
        nprint(response)

        assert_equal(response['account']['accountId'], ICONTACT_SETTINGS['account_id'])

    def test_contacts_call(self):
        """
            Test contacts call
        """

        ic_client = get_ic_client()

        # Test contact data ID
        tc_id = 0

        # Add new contact
        params = {
            'contact': test_contacts[tc_id].copy()
        }
        nprint(params)

        response = ic_client.post('contacts', params=params)
        nprint(response)

        assert_true('contactId' in response['contacts'][0])
        assert_equal(response['contacts'][0]['status'], u'normal')
        for param, test_value in test_contacts[tc_id].iteritems():
            assert_equal(unicode(response['contacts'][0][param]), unicode(test_value))

        contact_id = response['contacts'][0]['contactId']

        # Get all contacts
        response = ic_client.get('contacts')
        #nprint(response)

        assert_true(len(response['contacts']) > 0)

        # Get all contacts filtered by email
        params = {
            'email': test_contacts[tc_id]['email'],
        }
        nprint(params)

        response = ic_client.get('contacts', params=params)
        nprint(response)

        assert_true(len(response['contacts']) == 1)
        assert_true('contactId' in response['contacts'][0])
        assert_equal(response['contacts'][0]['contactId'], contact_id)
        assert_equal(response['contacts'][0]['status'], u'normal')
        for param, test_value in test_contacts[tc_id].iteritems():
            assert_equal(unicode(response['contacts'][0][param]), unicode(test_value))

        # Get new contact
        response = ic_client.get('contacts', [contact_id])
        nprint(response)

        assert_equal(response['contact']['contactId'], contact_id)
        assert_equal(response['contact']['status'], u'normal')
        for param, test_value in test_contacts[tc_id].iteritems():
            assert_equal(unicode(response['contact'][param]), unicode(test_value))

        # Update new contact (post)
        params = {
            'firstName': test_contacts[tc_id]['firstName'] + u' II',
            'city': u'Eindhoven'
        }
        nprint(params)

        response = ic_client.post('contacts', [contact_id], params=params)
        nprint(response)

        assert_equal(response['contact']['contactId'], contact_id)
        assert_equal(response['contact']['status'], u'normal')
        assert_equal(response['contact']['email'], test_contacts[tc_id]['email'])
        assert_equal(response['contact']['firstName'], params['firstName'])
        assert_equal(response['contact']['lastName'], test_contacts[tc_id]['lastName'])
        assert_equal(response['contact']['city'], params['city'])

        # Update new contact (put)
        params = {
            'email': u'%s@example.com' % (test_contact_names[tc_id] + u'_PUT'),
        }
        nprint(params)

        response = ic_client.put('contacts', [contact_id], params=params)
        nprint(response)

        assert_equal(response['contact']['contactId'], contact_id)
        assert_equal(response['contact']['status'], u'normal')
        assert_equal(response['contact']['email'], params['email'])
        assert_equal(response['contact']['firstName'], u'')
        assert_equal(response['contact']['lastName'], u'')
        assert_equal(response['contact']['city'], u'')

        # Delete contact
        response = ic_client.delete('contacts', [contact_id])
        nprint(response)

        assert_true(response == [])

        # Get deleted contact
        response = ic_client.get('contacts', [contact_id])
        nprint(response)

        assert_equal(response['contact']['contactId'], contact_id)
        assert_equal(response['contact']['status'], u'deleted')

    def test_lists_call(self):
        """
            Test lists call
        """

        ic_client = get_ic_client()

        # Test list data ID
        tl_id = 0

        # Get the oldest message and use it as list's welcome message
        params = {
            'orderby': 'createDate:asc,messageId:asc',
            'limit': 1
        }
        nprint(params)

        response = ic_client.get('messages', params=params)

        assert_true('messageId' in response['messages'][0])
        message_id = unicode(response['messages'][0]['messageId'])

        # Add new list
        params = {
            'list': test_lists[tl_id].copy()
        }
        params['list']['welcomeMessageId'] = message_id
        nprint(params)

        response = ic_client.post('lists', params=params)
        nprint(response)

        assert_true('listId' in response['lists'][0])
        assert_equal(unicode(response['lists'][0]['welcomeMessageId']), message_id)
        for param, test_value in test_lists[tl_id].iteritems():
            assert_equal(response['lists'][0][param], test_value)

        list_id = unicode(response['lists'][0]['listId'])

        # Get all lists
        response = ic_client.get('lists')
        #nprint(response)

        assert_true(len(response['lists']) > 0)

        # Get all lists filtered by name
        params = {
            'name': test_lists[tl_id]['name'],
        }
        nprint(params)

        response = ic_client.get('lists', params=params)
        nprint(response)

        assert_true(len(response['lists']) == 1)
        assert_true('listId' in response['lists'][0])
        assert_equal(unicode(response['lists'][0]['listId']), list_id)
        assert_equal(unicode(response['lists'][0]['welcomeMessageId']), message_id)
        for param, test_value in test_lists[tl_id].iteritems():
            assert_equal(unicode(response['lists'][0][param]), unicode(test_value))

        # Get new list
        response = ic_client.get('lists', [list_id])
        nprint(response)

        assert_true('listId' in response['list'])
        assert_equal(unicode(response['list']['listId']), list_id)
        assert_equal(unicode(response['list']['welcomeMessageId']), message_id)
        for param, test_value in test_lists[tl_id].iteritems():
            assert_equal(unicode(response['list'][param]), unicode(test_value))

        # Update new list (post)
        params = {
            'description': test_lists[tl_id]['description'] + u' (POST updated)',
        }
        nprint(params)

        response = ic_client.post('lists', [list_id], params=params)
        nprint(response)

        assert_true('listId' in response['list'])
        assert_equal(unicode(response['list']['listId']), list_id)
        assert_equal(unicode(response['list']['name']), test_lists[tl_id]['name'])
        assert_equal(unicode(response['list']['description']), params['description'])

        # Update new list (put)
        params = {
            'name': test_lists[tl_id]['name'] + u' II',
            'welcomeMessageId': message_id
        }
        nprint(params)

        response = ic_client.put('lists', [list_id], params=params)
        nprint(response)

        assert_true('listId' in response['list'])
        assert_equal(unicode(response['list']['listId']), list_id)
        assert_equal(unicode(response['list']['name']), params['name'])
        assert_equal(unicode(response['list']['welcomeMessageId']), params['welcomeMessageId'])
        assert_equal(unicode(response['list']['emailOwnerOnChange']), u'0')
        assert_equal(unicode(response['list']['welcomeOnManualAdd']), u'0')
        assert_equal(unicode(response['list']['welcomeOnSignupAdd']), u'0')

        # Delete list
        response = ic_client.delete('lists', [list_id])
        nprint(response)

        assert_true(response == [])

        # Get deleted list
        try:
            response = ic_client.get('lists', [list_id])
        except Exception, e:
            assert_true(isinstance(e, icontact.InternalServerError))
            assert_true('errors' in e.response)
            assert_equal(e.response['errors'][0], 'No result for (%s).' % list_id)

    def test_subscriptions_call(self):
        """
            Test subscriptions call
        """

        ic_client = get_ic_client()

        # Test contact data ID
        tc_id = 1

        # Test list A data ID
        tl_a_id = 1

        # Test list B data ID
        tl_b_id = 2

        # Add new contact
        params = {
            'contact': test_contacts[tc_id].copy()
        }
        nprint(params)

        response = ic_client.post('contacts', params=params)
        nprint(response)

        assert_true('contactId' in response['contacts'][0])
        assert_equal(response['contacts'][0]['status'], u'normal')
        for param, test_value in test_contacts[tc_id].iteritems():
            assert_equal(unicode(response['contacts'][0][param]), unicode(test_value))

        contact_id = response['contacts'][0]['contactId']

        # Get the oldest message and use it as list's welcome message
        params = {
            'orderby': 'createDate:asc,messageId:asc',
            'limit': 1
        }
        nprint(params)

        response = ic_client.get('messages', params=params)

        assert_true('messageId' in response['messages'][0])
        message_id = unicode(response['messages'][0]['messageId'])

        # Add new list A
        params = {
            'list': test_lists[tl_a_id].copy()
        }
        params['list']['welcomeMessageId'] = message_id
        nprint(params)

        response = ic_client.post('lists', params=params)
        nprint(response)

        assert_true('listId' in response['lists'][0])
        assert_equal(unicode(response['lists'][0]['welcomeMessageId']), message_id)
        for param, test_value in test_lists[tl_a_id].iteritems():
            assert_equal(response['lists'][0][param], test_value)

        list_a_id = unicode(response['lists'][0]['listId'])

        # Add new list B
        params = {
            'list': test_lists[tl_b_id].copy()
        }
        params['list']['welcomeMessageId'] = message_id
        nprint(params)

        response = ic_client.post('lists', params=params)
        nprint(response)

        assert_true('listId' in response['lists'][0])
        assert_equal(unicode(response['lists'][0]['welcomeMessageId']), message_id)
        for param, test_value in test_lists[tl_b_id].iteritems():
            assert_equal(response['lists'][0][param], test_value)

        list_b_id = unicode(response['lists'][0]['listId'])

        # Create subscription for list A
        params = {
            'subscription': {
                'contactId': contact_id,
                'listId': list_a_id,
                'status': 'normal',
            }
        }
        nprint(params)

        response = ic_client.post('subscriptions', params=params)
        nprint(response)

        assert_true('subscriptionId' in response['subscriptions'][0])
        assert_equal(unicode(response['subscriptions'][0]['subscriptionId']), u'%s_%s' % (list_a_id, contact_id))
        for param, test_value in params['subscription'].iteritems():
            assert_equal(response['subscriptions'][0][param], test_value)

        subscription_a_id = unicode(response['subscriptions'][0]['subscriptionId'])

        # Get all subscriptions
        response = ic_client.get('subscriptions')
        #nprint(response)

        assert_true(len(response['subscriptions']) > 0)

        # Get subscription for list A
        response = ic_client.get('subscriptions', [subscription_a_id])
        nprint(response)

        assert_true('subscriptionId' in response['subscription'])
        assert_equal(unicode(response['subscription']['subscriptionId']), subscription_a_id)
        for param, test_value in params['subscription'].iteritems():
            assert_equal(response['subscription'][param], test_value)

        # Update subscription A (put)
        params = {
            'listId': list_b_id
        }
        nprint(params)

        response = ic_client.put('subscriptions', [subscription_a_id], params=params)
        nprint(response)

        subscription_b_id = u'%s_%s' % (list_b_id, contact_id)

        assert_true('subscriptionId' in response['subscription'])
        assert_equal(unicode(response['subscription']['subscriptionId']), subscription_b_id)
        assert_equal(unicode(response['subscription']['contactId']), contact_id)
        assert_equal(unicode(response['subscription']['listId']), list_b_id)
        assert_equal(unicode(response['subscription']['status']), u'normal')

        # Check that contact's subscription has been moved from list A to list B
        try:
            response = ic_client.get('subscriptions', [subscription_a_id])
        except Exception, e:
            assert_true(isinstance(e, icontact.NotFound))
            assert_true('errors' in e.response)
            assert_equal(e.response['errors'][0], 'Not Found')

        response = ic_client.get('subscriptions', [subscription_b_id])
        nprint(response)

        assert_true('subscriptionId' in response['subscription'])
        assert_equal(unicode(response['subscription']['subscriptionId']), subscription_b_id)
        assert_equal(unicode(response['subscription']['contactId']), contact_id)
        assert_equal(unicode(response['subscription']['listId']), list_b_id)
        assert_equal(unicode(response['subscription']['status']), u'normal')

        # Re-create subscription for list A
        params = {
            'subscription': {
                'contactId': contact_id,
                'listId': list_a_id,
                'status': 'normal',
            }
        }
        nprint(params)

        response = ic_client.post('subscriptions', params=params)
        nprint(response)

        assert_true('subscriptionId' in response['subscriptions'][0])
        assert_equal(unicode(response['subscriptions'][0]['subscriptionId']), u'%s_%s' % (list_a_id, contact_id))
        for param, test_value in params['subscription'].iteritems():
            assert_equal(response['subscriptions'][0][param], test_value)

        subscription_a_id = unicode(response['subscriptions'][0]['subscriptionId'])

        # Get subscription for list A
        response = ic_client.get('subscriptions', [subscription_a_id])
        nprint(response)

        assert_true('subscriptionId' in response['subscription'])
        assert_equal(unicode(response['subscription']['subscriptionId']), subscription_a_id)
        for param, test_value in params['subscription'].iteritems():
            assert_equal(response['subscription'][param], test_value)

        # Update subscription A (post)
        params = {
            'status': 'unsubscribed',
        }
        nprint(params)

        response = ic_client.post('subscriptions', [subscription_a_id], params=params)
        nprint(response)

        assert_true('subscriptionId' in response['subscription'])
        assert_equal(unicode(response['subscription']['subscriptionId']), subscription_a_id)
        assert_equal(unicode(response['subscription']['contactId']), contact_id)
        assert_equal(unicode(response['subscription']['listId']), list_a_id)
        assert_equal(unicode(response['subscription']['status']), u'unsubscribed')

        # Check that contact has been unsubscribed from the list A
        response = ic_client.get('subscriptions', [subscription_a_id])
        nprint(response)

        assert_true('subscriptionId' in response['subscription'])
        assert_equal(unicode(response['subscription']['subscriptionId']), subscription_a_id)
        assert_equal(unicode(response['subscription']['contactId']), contact_id)
        assert_equal(unicode(response['subscription']['listId']), list_a_id)
        assert_equal(unicode(response['subscription']['status']), u'unsubscribed')

        # Update subscription B (post)
        params = {
            'status': 'unsubscribed',
        }
        nprint(params)

        response = ic_client.post('subscriptions', [subscription_b_id], params=params)
        nprint(response)

        assert_true('subscriptionId' in response['subscription'])
        assert_equal(unicode(response['subscription']['subscriptionId']), subscription_b_id)
        assert_equal(unicode(response['subscription']['contactId']), contact_id)
        assert_equal(unicode(response['subscription']['listId']), list_b_id)
        assert_equal(unicode(response['subscription']['status']), u'unsubscribed')

        # Check that contact has been unsubscribed from the list B
        response = ic_client.get('subscriptions', [subscription_b_id])
        nprint(response)

        assert_true('subscriptionId' in response['subscription'])
        assert_equal(unicode(response['subscription']['subscriptionId']), subscription_b_id)
        assert_equal(unicode(response['subscription']['contactId']), contact_id)
        assert_equal(unicode(response['subscription']['listId']), list_b_id)
        assert_equal(unicode(response['subscription']['status']), u'unsubscribed')

        # Delete contact
        response = ic_client.delete('contacts', [contact_id])
        nprint(response)

        assert_true(response == [])

        # Get deleted contact
        response = ic_client.get('contacts', [contact_id])
        nprint(response)

        assert_equal(response['contact']['contactId'], contact_id)
        assert_equal(response['contact']['status'], u'deleted')

        # Delete list A
        response = ic_client.delete('lists', [list_a_id])
        nprint(response)

        assert_true(response == [])

        # Get deleted list A
        try:
            response = ic_client.get('lists', [list_a_id])
        except Exception, e:
            assert_true(isinstance(e, icontact.InternalServerError))
            assert_true('errors' in e.response)
            assert_equal(e.response['errors'][0], 'No result for (%s).' % list_a_id)

        # Delete list B
        response = ic_client.delete('lists', [list_b_id])
        nprint(response)

        assert_true(response == [])

        # Get deleted list B
        try:
            response = ic_client.get('lists', [list_b_id])
        except Exception, e:
            assert_true(isinstance(e, icontact.InternalServerError))
            assert_true('errors' in e.response)
            assert_equal(e.response['errors'][0], 'No result for (%s).' % list_b_id)

    def test_messages_call(self):
        """
            Test messages call
        """

        ic_client = get_ic_client()

        # Get all messages
        response = ic_client.get('messages')
        #nprint(response)

        assert_true(len(response['messages']) > 0)
        assert_true(response['limit'] == 20)

    def test_customfields_call(self):
        """
            Test custom fields call
        """

        ic_client = get_ic_client()

        # Test custom field data ID
        tcf_id = 0

        # Add new custom field
        params = {
            'customfield': test_customfields[tcf_id]
        }
        nprint(params)

        response = ic_client.post('customfields', params=params)
        nprint(response)

        for param, test_value in test_customfields[tcf_id].iteritems():
            assert_equal(unicode(response['customfields'][0][param]), unicode(test_value))

        customfield_id = test_customfields[tcf_id]['privateName']

        # Get all custom fields
        response = ic_client.get('customfields')
        nprint(response)

        assert_true(len(response['customfields']) > 0)

        # Get new custom field
        response = ic_client.get('customfields', [customfield_id])
        nprint(response)

        assert_true('customFieldId' in response['customfield'])
        assert_equal(unicode(response['customfield']['customFieldId']), unicode(customfield_id))
        for param, test_value in test_customfields[tcf_id].iteritems():
            assert_equal(unicode(response['customfield'][param]), unicode(test_value))

        # Create a new contact; set and update custom field in the contact details

        # Test contact data ID
        tc_id = 2

        # Add new contact
        params = {
            'contact': test_contacts[tc_id].copy()
        }
        params['contact'][customfield_id] = u'test'
        nprint(params)

        response = ic_client.post('contacts', params=params)
        nprint(response)

        assert_true('contactId' in response['contacts'][0])
        assert_equal(response['contacts'][0]['status'], u'normal')
        assert_true(customfield_id in response['contacts'][0])
        assert_equal(response['contacts'][0][customfield_id], params['contact'][customfield_id])
        for param, test_value in test_contacts[tc_id].iteritems():
            assert_equal(unicode(response['contacts'][0][param]), unicode(test_value))

        contact_id = response['contacts'][0]['contactId']

        # Get contact
        response = ic_client.get('contacts', [contact_id])
        nprint(response)

        assert_equal(response['contact']['contactId'], contact_id)
        assert_equal(response['contact']['status'], u'normal')
        assert_true(customfield_id in response['contact'])
        assert_equal(response['contact'][customfield_id], params['contact'][customfield_id])
        for param, test_value in test_contacts[tc_id].iteritems():
            assert_equal(unicode(response['contact'][param]), unicode(test_value))

        # Update contact (post)
        params = {
            customfield_id: u'another test',
        }
        nprint(params)

        response = ic_client.post('contacts', [contact_id], params=params)
        nprint(response)

        assert_equal(response['contact']['contactId'], contact_id)
        assert_equal(response['contact']['status'], u'normal')
        assert_true(customfield_id in response['contact'])
        assert_equal(response['contact'][customfield_id], params[customfield_id])
        for param, test_value in test_contacts[tc_id].iteritems():
            assert_equal(unicode(response['contact'][param]), unicode(test_value))

        # Delete contact
        response = ic_client.delete('contacts', [contact_id])
        nprint(response)

        assert_true(response == [])

        # Update new custom field (post)
        params = {
            'publicName': test_customfields[tcf_id]['publicName'] + u' (POST updated)',
        }
        nprint(params)

        response = ic_client.post('customfields', [customfield_id], params=params)
        nprint(response)

        assert_equal(unicode(response['customfield']['privateName']), unicode(test_customfields[tcf_id]['privateName']))
        assert_equal(unicode(response['customfield']['publicName']), unicode(params['publicName']))
        assert_equal(unicode(response['customfield']['fieldType']), unicode(test_customfields[tcf_id]['fieldType']))
        assert_equal(unicode(response['customfield']['displayToUser']), unicode(test_customfields[tcf_id]['displayToUser']))

        # Update new custom field (put)
        params = {
            'privateName': test_customfields[tcf_id]['privateName'],
            'publicName': test_customfields[tcf_id]['publicName'] + u' (PUT updated)',
            'fieldType': u'text',
            'displayToUser': 1,
        }
        nprint(params)

        response = ic_client.put('customfields', [customfield_id], params=params)
        nprint(response)

        assert_equal(unicode(response['customfield']['privateName']), unicode(params['privateName']))
        assert_equal(unicode(response['customfield']['publicName']), unicode(params['publicName']))
        assert_equal(unicode(response['customfield']['fieldType']), unicode(params['fieldType']))
        assert_equal(unicode(response['customfield']['displayToUser']), unicode(params['displayToUser']))

        # Delete custom field
        response = ic_client.delete('customfields', [customfield_id])
        nprint(response)

        assert_true(response == [])

        # Get deleted custom field
        try:
            response = ic_client.get('customfields', [customfield_id])
        except Exception, e:
            assert_true(isinstance(e, icontact.NotFound))
            assert_true('errors' in e.response)
            assert_equal(e.response['errors'][0], 'Not Found')

    def test_request_limit(self):
        """
            Test request limit
        """

        ic_client = get_ic_client()

        response = ic_client.get('contacts')
        for contact in response['contacts'][:300]:
            ic_client.get('contacts', [contact['contactId']])

"""
iContact API calls tests status
===============================

GET POST PUT DELETE single / multiple
- call method not tested
+ call method tested
x call method not supported

+---/+---  accounts
----/----  users
----/----  permissions
----/----  client-folders
++++/++xx  contacts
----/----  contact-history
++++/++xx  lists
+++x/++xx  subscriptions
----/+---  messages
----/----  message-bounces
----/----  message-clicks
----/----  message-opens
----/----  statistics
----/----  unsubscribes
----/----  segments
----/----  segment-criteria
----/----  sends
----/----  campaigns
++++/++xx  customfields
----/----  uploads
+xxx/xxxx  time
"""
