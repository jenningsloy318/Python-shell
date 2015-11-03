#!/usr/bin/env python2
import json
import urllib
import urllib2



class zenoss_session(object):
    def __init__(self, zenoss_username,zenoss_password,zenoss_instance,routes,debug=False):
	self.zenoss_username=zenoss_username
	self.zenoss_password=zenoss_password
	self.zenoss_instance=zenoss_instance
	self.routes=routes
        self.debug=debug
        """
        Initialize the API connection, log in, and store authentication cookie
        """
        # Use the HTTPCookieProcessor as urllib2 does not save cookies by default
        self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        if self.debug: self.urlOpener.add_handler(urllib2.HTTPHandler(debuglevel=1))
        self.reqCount = 1

        # Contruct POST params and submit login.
        loginParams = urllib.urlencode(dict(
                        __ac_name = self.zenoss_username,
                        __ac_password = self.zenoss_password,
                        submitted = 'true',
                        came_from = self.zenoss_instance + '/zport/dmd'))
        self.urlOpener.open(self.zenoss_instance + '/zport/acl_users/cookieAuthHelper/login',
                            loginParams)

    def router_request(self, router, method, data=[]):
        if router not in self.routes:
            raise Exception('Router "' + router + '" not available.')

        # Contruct a standard URL request for API calls
        req = urllib2.Request(self.zenoss_instance + '/zport/dmd/' +
                              self.routes[router] + '_router')

        # NOTE: Content-type MUST be set to 'application/json' for these requests
        req.add_header('Content-type', 'application/json; charset=utf-8')

        # Convert the request parameters into JSON
        reqData = json.dumps([dict(
                    action=router,
                    method=method,
                    data=data,
                    type='rpc',
                    tid=self.reqCount)])

        # Increment the request count ('tid'). More important if sending multiple
        # calls in a single request
        self.reqCount += 1

        # Submit the request and convert the returned JSON to objects
        return json.loads(self.urlOpener.open(req, reqData).read())

