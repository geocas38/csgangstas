
import json
import jinja2
import logging
import urllib
import webapp2
from google.appengine.api import urlfetch
from google.appengine.api import users

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

#This handler will sign the user into the website
class MainHandler(webapp2.RequestHandler): #log-in page
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/intro')
        else:
            greeting = ('<a href="%s">Sign in or register</a>.'% users.create_login_url('/'))

            greeting = ('<a href="%s">Sign in or register</a>.' %
            users.create_login_url('/'))
            self.response.out.write('<html><body>%s</body></html>' % greeting)
#This handler allows the user to chose if they want to "review" or if they want to make a schedule
class IntroHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('intro.html')
        logout = {'logout':users.create_logout_url('/')}
        self.response.out.write(template.render(logout))

#Renders the search HTML for the user to input their city, state, zip code and radius in which they want to travel
class SearchHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('search.html')
        logout = {'logout':users.create_logout_url('/')}
        self.response.write(template.render())

#Generates the schedule. However, in p0 we will just be printing out a list of all attractions. P1 will be generating the schedule
class ScheduleHandler(webapp2.RequestHandler):

        ##post schedule
    def post(self):

        template = jinja_env.get_template('results.html')

        city = self.request.get('city')
        state = self.request.get('state')
        radius = self.request.get('radius')

        if city, state, radius:
            attractions = self.fetch_attractions(city, state, radius)
            resturants = self.fetch_resturants(city, state, radius)
            variables = {
            
            }

        ##Find attractions
    def fetch_attractions(self, city, state, radius):

        ##Find Resturants
    def fetch_resturants(self, city, state, radius ):

        ##Utilize yelp search to find the resturants and attractions
    def yelp_search(self, city, state, radius ):





]app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/intro', IntroHandler),
  ('/search', SearchHandler),
], debug=True)
