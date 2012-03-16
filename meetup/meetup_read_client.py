import types
import logging
import json
from urllib import urlencode
from urllib2 import HTTPError, HTTPErrorProcessor, urlopen, Request, build_opener

# This is a client wrapper that you can use to make calls to the Meetup.com API.
# This wrapper only supports the API call which not require OAuth or some other
# authentication.
# It requires that you have a JSON parsing module available.

API_JSON_ENCODING = 'ISO-8859-1'
parse_json = lambda s: json.loads(s.decode(API_JSON_ENCODING))

API_BASE_URL = 'http://api.meetup.com/'

class MeetupHTTPErrorProcessor(HTTPErrorProcessor):
    def http_response(self, request, response):
        try:
            return HTTPErrorProcessor.http_response(self, request, response)
        except HTTPError, e:
            error_json = parse_json(e.read())
            if e.code == 401:
                raise UnauthorizedError(error_json)
            elif e.code in ( 400, 500 ):
                raise BadRequestError(error_json)
            else:
                raise ClientException(error_json)

class Meetup(object):
    opener = build_opener(MeetupHTTPErrorProcessor)

    def __init__(self, api_key):
        """
        Initializes a new session with an api key that will be added
        to subsequent api calls
        """
        self.api_key = api_key

    def args_str(self, url_args):
        if self.api_key:
            url_args['key'] = self.api_key
        return urlencode(url_args)

    def _fetch(self, uri, **url_args):
        args = self.args_str(url_args)
        url = API_BASE_URL + uri + '/' + "?" + args
        logging.debug("requesting %s" % (url))
        return parse_json(self.opener.open(url).read())

    def _fetch_with_id(self, uri, id, **url_args):
        args = self.args_str(url_args)
        url = API_BASE_URL + uri + '/' + id + "?" + args
        logging.debug("requesting %s" % (url))
        return parse_json(self.opener.open(url).read())

"""
Add read methods to Meetup class dynamically (avoiding boilerplate)
"""
READ_METHODS = {
    # checkins
    'checkins': '2/checkins',
    # events
    'open_events': '2/oven_events',
    'events': '2/events',
    'event_comments': '2/event_comments',
    'event_ratings': '2/event_ratings',
    # groups
    'groups': '2/groups',
    # members
    'members': '2/members',
    'profiles': '2/profiles',
    # photos
    'photo_comments': '2/photo_comments',
    'photo_albums': '2/photo_albums',
    'photos': '2/photos',
    # rsvps
    'rsvps': '2/rsvps',
    # venues
    'open_venues': '2/open_venues',
    'venues': '2/venues',
}
def _generate_read_method(uri):
    def read_method(self, **args):
        return API_Response(self._fetch(uri, **args))
    return read_method

for method, uri in READ_METHODS.items():
    read_method = types.MethodType(_generate_read_method(uri), None, Meetup)
    setattr(Meetup, 'get_' + method, read_method)

READ_METHODS_WITH_ID = {
    # events
    'event': '2/event',
    # members
    'member': '2/member',
    # rsvps
    'rsvp': '2/rsvp',
}
def _generate_read_method_with_id(uri):
    def read_method(self, id, **args):
        # TODO need some validation to make sure that id is given
        return self._fetch_with_id(uri, id, **args)
    return read_method

for method, uri in READ_METHODS_WITH_ID.items():
    read_method = types.MethodType(_generate_read_method_with_id(uri), None, Meetup)
    setattr(Meetup, 'get_' + method, read_method)


class NoToken(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return "NoRequestToken: %s" % (self.description)

class API_Response(object):
    def __init__(self, json):
        """
        Copies metadata from JSON.
        Copies results from JSON.
        """
        self.meta = json['meta']
        self.results = json['results']

    def __str__(self):
        return 'meta: ' + str(self.meta) + '\n' + str(self.results)


########################################

class ClientException(Exception):
    """
         Base class for generic errors returned by the server
    """
    def __init__(self, error_json):
         self.description = error_json['details']
         self.problem = error_json['problem']

    def __str__(self):
         return "%s: %s" % (self.problem, self.description)

class UnauthorizedError(ClientException):
    pass;

class BadRequestError(ClientException):
    pass;

