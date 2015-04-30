'''
Created on 05.11.2014

Based on Flask Snippet 'Securely Redirect Back'
URL: http://flask.pocoo.org/snippets/62/

@author: Philip
'''

import urlparse

import flask


def is_safe_url(target):
    """
    Checks if a redirect target will lead to the same server.
    """
    ref_url = urlparse.urlparse(flask.request.host_url)
    test_url = urlparse.urlparse(urlparse.urljoin(flask.request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    """
    Retrieves the redirect target from the 'next' URL parameter or the HTTP referrer.
    """
    for target in flask.request.values.get('next'), flask.request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def redirect_back(endpoint, **values):
    """
    Redirects to the target from the 'next' URL parameter or the given default endpoint.
    """
    target = get_redirect_target()
    #print "Target: {}".format(target)
    #print "Request Referrer: {}".format(flask.request.referrer)
    #print "Request URL: {}".format(flask.request.url)
    if not target or target == flask.request.url:
        target = flask.url_for(endpoint, **values)
    return flask.redirect(target)
