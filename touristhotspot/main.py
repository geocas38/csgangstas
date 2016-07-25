import json
import jinja2
import logging
import urllib
import webapp2
from google.appengine.api import users
from google.appengine.api import urlfetch


class MainHandler(webapp2.RequestHandler):

    def get(self):
        

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
