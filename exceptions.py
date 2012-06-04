# -*- coding: utf-8 -*-

"""
iContact API Client Exceptions
==============================
Exceptions raised by iContact API Client
"""

class IContactException(Exception):
    def __init__(self, http_method=None, url=None, response=None, message=None):
        self.http_method = http_method.upper() \
                if (type(http_method) is type(str())) else \
                http_method
        self.url = url
        self.response = response

        if url:
            self.message = u"%s call to: '%s' failed." % (self.http_method, url)
        else:
            self.message = u""

        if (message == None) and (response != None):
            if ('errors' in response) and response['errors']:
                self.message += u" Error: %s" % response['errors'][0]
            else:
                self.message += u" Error: Unknown"
        elif (message != None):
            self.message = unicode(message)

class NoData(IContactException):
    """
    HTTP status code: 200 OK
    Description: No (expected) data
    """
    pass

class BadRequest(IContactException):
    """
    HTTP status code: 400 Bad Request
    Description: Your data could not be parsed or your request contained invalid data
    """
    pass

class NotAuthorized(IContactException):
    """
    HTTP status code: 401 Not Authorized
    Description: You are not logged in
    """
    pass

class PaymentRequired(IContactException):
    """
    HTTP status code: 402 Payment Required
    Description: You must pay your iContact bill before we can process your request
    """
    pass

class Forbidden(IContactException):
    """
    HTTP status code: 403 Forbidden
    Description: You are logged in, but do not have permission to perform that action
    """
    pass

class NotFound(IContactException):
    """
    HTTP status code: 404 Not Found
    Description: You have requested a resource that cannot be found
    """
    pass

class MethodNotAllowed(IContactException):
    """
    HTTP status code: 405 Method Not Allowed
    Description: You cannot perform that method on the requested resource
    """
    pass

class NotAcceptable(IContactException):
    """
    HTTP status code: 406 Not Acceptable
    Description: You have requested that iContact generate data in an unsupported
                 format. The iContact API can only return data in XML or JSON
    """
    pass

class UnsupportedMediaType(IContactException):
    """
    HTTP status code: 415 Unsupported Media Type
    Description: Your request was not in a supported format. You can make
                 requests in XML or JSON.
    """
    pass

class InternalServerError(IContactException):
    """
    HTTP status code: 500 Internal Server Error
    Description: An error occurred in iContact's code
    """
    pass

class NotImplemented(IContactException):
    """
    HTTP status code: 501 Not Implemented
    Description: You have requested a resource that has not been implemented or
                 you have specified an incorrect version of the iContact API
    """
    pass

class ServiceUnavailable(IContactException):
    """
    HTTP status code: 503 Service Unavailable
    Description: You cannot perform the action because the system is experiencing
                 extremely high traffic or you cannot perform the action because
                 the system is down for maintenance
    """
    pass

class InsufficientSpace(IContactException):
    """
    HTTP status code: 507 Insufficient Space
    Description: You have used up all of your allotted storage
                 (for example, in the image library)
    """
    pass

class UnknownError(IContactException):
    """
    HTTP status code: any, except listed above
    Description: This is a catch-all exception that should be used if there is no
                 exception defined for the returned HTTP status code
    """
    pass
