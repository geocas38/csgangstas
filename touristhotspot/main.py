import json
import jinja2
import logging
import urllib
import webapp2
from google.appengine.api import urlfetch
from google.appengine.api import users

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/intro')
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                users.create_login_url('/'))

            self.response.out.write('<html><body>%s</body></html>' % greeting)

class IntroHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/intro.html')
        logout = {'logout':users.create_logout_url('/')}
        self.response.out.write(template.render(logout))

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/intro', IntroHandler)
], debug=True)
