# -*- coding: utf-8 -*-

import logging
import time
import StringIO
import urllib
import pycurl
try:
    import json
except ImportError:
    import simplejson as json

from exceptions import *


__all__ = ['IContactClient']

class IContactClient(object):
    """
    iContact API Client
    ===================
    Client for iContact API
    """

    def __init__(self, user_name=None, app_id=None, app_password=None, version='2.2',
                 base_url=None, account_id=None, clientfolder_id=None):
        """Initialize client

        @type user_name: str
        @keyword user_name: Username for logging into iContact, or sandbox environment username,
                            if sandbox account is used.

        @type app_id: str
        @keyword app_id: iContact API Application ID. Obtained during registration of the API application.

        @type app_password: str
        @keyword app_password: iContact API Application password. Set during registration of the API application.

        @type version: str
        @keyword version: (optional) iContact API version (2.0, 2.1, or 2.2). Default is '2.2'

        @type base_url: str
        @keyword base_url: (optional) iContact API base URL. Default is 'https://app.icontact.com/icp'.
                           For sandbox account 'https://app.sandbox.icontact.com/icp' URL should be used.

        @type account_id: str
        @keyword account_id: iContact account ID

        @type clientfolder_id: str
        @keyword clientfolder_id: iContact account client folder ID
        """

        self._request_headers = dict()

        self._request_headers['API-Username'] = user_name
        self._request_headers['API-AppId'] = app_id
        self._request_headers['API-Password'] = app_password
        self._request_headers['API-Version'] = version

        # Only JSON is supported
        self._request_headers['Accept'] = 'application/json'
        self._request_headers['Content-Type'] = 'application/json'

        if base_url != None:
            self._api_base_url = base_url.rstrip('/')
        else:
            self._api_base_url = 'https://app.icontact.com/icp'

        self._account_id = str(account_id)
        self._clientfolder_id = str(clientfolder_id)

    def get(self, resource, resource_ids=None, params=dict(), verbose=False):
        """Executes API call using HTTP GET method

        @type resource: str
        @keyword resource: iContact API resource name. See L{IContactClient._request} method
                           for the list of available resources.

        @type resource_ids: list
        @keyword resource_ids: (optional) List of resource IDs that should be used in resource URL.

        @type params: dict
        @keyword params: (optional) Dictionary of the resource query parameters.

        @type verbose: bool
        @keyword verbose: (optional) Specifies if cURL verbose mode should be used.
                          Allowed values:
                          - True : cURL verbose mode is enabled
                          - False : cURL verbose mode is disabled
                          Default is False.

        @rtype: dict or list
        @return: Call response
        """
        return self._request('GET', resource, resource_ids, params, verbose)

    def post(self, resource, resource_ids=None, params=dict(), verbose=False):
        """Executes API call using HTTP POST method

        @type resource: str
        @keyword resource: iContact API resource name. See L{IContactClient._request} method
                           for the list of available resources.

        @type resource_ids: list
        @keyword resource_ids: (optional) List of resource IDs that should be used in resource URL.

        @type params: dict
        @keyword params: (optional) Dictionary of the resource query parameters.

        @type verbose: bool
        @keyword verbose: (optional) Specifies if cURL verbose mode should be used.
                          Allowed values:
                          - True : cURL verbose mode is enabled
                          - False : cURL verbose mode is disabled
                          Default is False.

        @rtype: dict or list
        @return: Call response
        """
        return self._request('POST', resource, resource_ids, params, verbose)

    def put(self, resource, resource_ids=None, params=dict(), verbose=False):
        """Executes API call using HTTP PUT method

        @type resource: str
        @keyword resource: iContact API resource name. See L{IContactClient._request} method
                           for the list of available resources.

        @type resource_ids: list
        @keyword resource_ids: (optional) List of resource IDs that should be used in resource URL.

        @type params: dict
        @keyword params: (optional) Dictionary of the resource query parameters.

        @type verbose: bool
        @keyword verbose: (optional) Specifies if cURL verbose mode should be used.
                          Allowed values:
                          - True : cURL verbose mode is enabled
                          - False : cURL verbose mode is disabled
                          Default is False.

        @rtype: dict or list
        @return: Call response
        """
        return self._request('PUT', resource, resource_ids, params, verbose)

    def delete(self, resource, resource_ids=None, params=dict(), verbose=False):
        """Executes API call using HTTP DELETE method

        @type resource: str
        @keyword resource: iContact API resource name. See L{IContactClient._request} method
                           for the list of available resources.

        @type resource_ids: list
        @keyword resource_ids: (optional) List of resource IDs that should be used in resource URL.

        @type params: dict
        @keyword params: (optional) Dictionary of the resource query parameters.

        @type verbose: bool
        @keyword verbose: (optional) Specifies if cURL verbose mode should be used.
                          Allowed values:
                          - True : cURL verbose mode is enabled
                          - False : cURL verbose mode is disabled
                          Default is False.

        @rtype: dict or list
        @return: Call response
        """
        return self._request('DELETE', resource, resource_ids, params, verbose)

    def _request(self, http_method, resource, resource_ids=None, params=dict(), verbose=False):
        """Executes API call using

        @type http_method: str
        @keyword http_method: HTTP method. One of: GET, POST, PUT or DELETE

        @type resource: str
        @keyword resource: iContact API resource name. Supported resources:
                           - accounts
                           - users
                           - permissions
                           - client-folders
                           - contacts
                           - contact-history
                           - lists
                           - subscriptions
                           - messages
                           - message-bounces
                           - message-clicks
                           - message-opens
                           - statistics
                           - unsubscribes
                           - segments
                           - segment-criteria
                           - sends
                           - campaigns
                           - customfields
                           - uploads
                           - time

        @type resource_ids: list
        @keyword resource_ids: (optional) List of resource IDs that should be used in resource URL.

        @type params: dict
        @keyword params: (optional) Dictionary of the resource query parameters.

        @type verbose: bool
        @keyword verbose: (optional) Specifies if cURL verbose mode should be used.
                          Allowed values:
                          - True : cURL verbose mode is enabled
                          - False : cURL verbose mode is disabled
                          Default is False.

        @rtype: dict or list
        @return: Call response
        """
        curl = pycurl.Curl()

        if verbose != None:
            # Set verbose output mode
            curl.setopt(curl.VERBOSE, verbose)

        url = self._get_resource_url(resource, resource_ids)

        # Set HTTP request method and method specific options
        if http_method == 'GET':
            curl.setopt(pycurl.HTTPGET, True)
            if params and (type(params) == type(dict())):
                try:
                    query = urllib.urlencode(params.copy())
                except UnicodeError, exc:
                    logging.exception(u"Failed to URL-encode parameters: %s. Error message: %s" \
                            % (unicode(params), unicode(exc)))
                    raise UnknownError(message=u"Failed to URL-encode parameters: %s. Error message: %s" \
                            % (unicode(params), unicode(exc)))
                url += '?' + query
        elif http_method == 'POST':
            curl.setopt(pycurl.POST, True)
            if params and (type(params) == type(dict())):
                curl.setopt(pycurl.POSTFIELDS, json.dumps(params.copy()))
        elif http_method == 'PUT':
            request_body = json.dumps(params.copy())
            curl.setopt(pycurl.PUT, True)
            curl.setopt(pycurl.HTTPHEADER, ['Content-Length: %d' % len(request_body)])
            request_buffer = StringIO.StringIO(request_body)
            curl.setopt(pycurl.READFUNCTION, request_buffer.read)
        elif http_method == 'DELETE':
            curl.setopt(pycurl.CUSTOMREQUEST, 'DELETE')

        # Set required HTTP headers
        curl.setopt(pycurl.HTTPHEADER,
                ["%s: %s" % (k, v) for k, v in self._request_headers.items()])

        # Set API resource URL
        curl.setopt(pycurl.URL, str(url))

        # Write response to a string
        response_buffer = StringIO.StringIO()
        curl.setopt(pycurl.WRITEFUNCTION, response_buffer.write)

        http_code = 503
        retry_counter = 0

        # Retry a number of times if server returns "503 Service Unavailable" status code.
        # We probably hit the request limit (6000 requests in a 24 hour period,
        # with a maximum of 60 requests per 60 seconds).
        while (http_code == 503) and (retry_counter <= 3):
            time.sleep(retry_counter)
            retry_counter += 1

            response_buffer.truncate(0)
            curl.perform()

            http_code = curl.getinfo(curl.HTTP_CODE)

        response = response_buffer.getvalue()

        curl.close()
        response_buffer.close()

        return self._process_response(http_method, url, resource, resource_ids, http_code, response)

    def _get_resource_url(self, resource, resource_ids=None):
        """Helper method for constructing API resource URL

        @type resource: str
        @keyword resource: iContact API resource name.

        @type resource_ids: list
        @keyword resource_ids: (optional) List of resource IDs that should be used in resource URL.

        @rtype: str
        @return: Resource URL
        """
        MAX_IDS = 2
        ids = ['' for i in range(MAX_IDS)]

        if resource_ids:
            for (i, id) in enumerate(resource_ids):
                if (id != None):
                    ids[i] = id

        account_folder_path = "/a/%s/c/%s" % (self._account_id, self._clientfolder_id)

        resources = {
            'accounts': '/a/%s' % ids[0],
            'users': '/a/%s/users/%s' % (self._account_id, ids[0]),
            'permissions': '/a/%s/users/%s/permissions' % (self._account_id, ids[0]),
            'client-folders': '/a/%s/c/%s' % (self._account_id, ids[0]),
            'contacts': '%s/contacts/%s' % (account_folder_path, ids[0]),
            'contact-history': '%s/contacts/%s/actions' % (account_folder_path, ids[0]),
            'lists': '%s/lists/%s' % (account_folder_path, ids[0]),
            'subscriptions': '%s/subscriptions/%s' % (account_folder_path, ids[0]),
            'messages': '%s/messages/%s' % (account_folder_path, ids[0]),
            'message-bounces': '%s/messages/%s/bounces' % (account_folder_path, ids[0]),
            'message-clicks': '%s/messages/%s/clicks' % (account_folder_path, ids[0]),
            'message-opens': '%s/messages/%s/opens' % (account_folder_path, ids[0]),
            'statistics': '%s/messages/%s/statistics' % (account_folder_path, ids[0]),
            'unsubscribes': '%s/messages/%s/unsubscribes' % (account_folder_path, ids[0]),
            'segments': '%s/segments/%s' % (account_folder_path, ids[0]),
            'segment-criteria': '%s/segments/%s/criteria/%s' % (account_folder_path, ids[0], ids[1]),
            'sends': '%s/sends/%s' % (account_folder_path, ids[0]),
            'campaigns': '%s/campaigns/%s' % (account_folder_path, ids[0]),
            'customfields': '%s/customfields/%s' % (account_folder_path, ids[0]),
            'uploads': '%s/uploads/%s' % (account_folder_path, ids[0]),
            'time': '/time',
        }

        url = self._api_base_url

        try:
            url += resources[resource]
        except KeyError:
            url += '/' + resource

        return url

    def _process_response(self, http_method, url, resource, resource_ids, http_code, http_response):
        """Helper method for processing API response and converting it from JSON format to dict or list.

        @type http_method: str
        @keyword http_method: HTTP method. One of: GET, POST, PUT or DELETE

        @type url: str
        @keyword url: resource URL

        @type resource: str
        @keyword resource: iContact API resource name.

        @type resource_ids: list
        @keyword resource_ids: (optional) List of resource IDs used in resource URL.

        @type http_code: int
        @keyword http_code: HTTP response code.

        @type http_response: str
        @keyword http_response: HTTP response body in JSON format.

        @raise IContactException: Raises IContactException if http_code != 200, or
                                  no (expected) data has been found in http_response.

        @rtype: dict or list
        @return: Converted API response
        """

        if resource_ids != None:
            nr_of_ids = len(resource_ids)
        else:
            nr_of_ids = 0

        expected_response_keys = {
            'accounts': None if (http_method not in ['GET', 'POST']) else \
                        ('accounts' if (nr_of_ids == 0) else 'account'),
            'users': 'users' if (nr_of_ids == 0) else 'user',
            'permissions': 'permissions' if (nr_of_ids == 0) else 'permission',
            'client-folders': 'clientfolders' if (nr_of_ids == 0) else 'clientfolder',
            'contacts': None if (http_method not in ['GET', 'POST']) else \
                        ('contacts' if (nr_of_ids == 0) else 'contact'),
            'contact-history': 'actions' if (nr_of_ids == 0) else 'action',
            'lists': None if (http_method not in ['GET', 'POST']) else \
                     ('lists' if (nr_of_ids == 0) else 'list'),
            'subscriptions': 'subscriptions' if (nr_of_ids == 0) else 'subscription',
            'messages': 'messages' if (nr_of_ids == 0) else 'message',
            'message-bounces': 'bounces' if (nr_of_ids == 0) else 'bounce',
            'message-clicks': 'clicks' if (nr_of_ids == 0) else 'click',
            'message-opens': 'opens' if (nr_of_ids == 0) else 'open',
            'statistics': 'statistics',
            'unsubscribes': 'unsubscribes',
            'segments': 'segments' if (nr_of_ids == 0) else 'segment',
            'segment-criteria': 'criteria' if (nr_of_ids == 0) else 'criterion',
            'sends': 'sends' if (nr_of_ids == 0) else 'send',
            'campaigns': 'campaigns' if (nr_of_ids == 0) else 'campaign',
            'customfields': None if (http_method not in ['GET', 'POST']) else \
                            ('customfields' if (nr_of_ids == 0) else 'customfield'),
            'uploads': 'uploads' if (nr_of_ids == 0) else 'upload',
            'time': 'time',
        }

        try:
            response = json.loads(http_response)
        except Exception, e:
            logging.exception(e.message)
            raise NoData("Error parsing JSON response")

        if (http_code == 200):
            expected_key = expected_response_keys[resource]
            if expected_key and (expected_key not in response):
                raise NoData(http_method, url,
                        response, "No '%s' data in response" % expected_key)
        elif (http_code == 400):
            raise BadRequest(http_method, url, response)
        elif (http_code == 401):
            raise NotAuthorized(http_method, url, response)
        elif (http_code == 402):
            raise PaymentRequired(http_method, url, response)
        elif (http_code == 403):
            raise Forbidden(http_method, url, response)
        elif (http_code == 404):
            raise NotFound(http_method, url, response)
        elif (http_code == 405):
            raise MethodNotAllowed(http_method, url, response)
        elif (http_code == 406):
            raise NotAcceptable(http_method, url, response)
        elif (http_code == 415):
            raise UnsupportedMediaType(http_method, url, response)
        elif (http_code == 500):
            raise InternalServerError(http_method, url, response)
        elif (http_code == 501):
            raise NotImplemented(http_method, url, response)
        elif (http_code == 503):
            raise ServiceUnavailable(http_method, url, response)
        elif (http_code == 507):
            raise InsufficientSpace(http_method, url, response)
        else:
            raise UnknownError(http_method, url, response)

        return response
