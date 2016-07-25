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
                'search_attraction': attraction
                'search_resturant': resturants
            }
            self.response.write(template.render(variables))
        else:
            self.response.write("Please specify a city, state, or radius")

        ##Find attractions
    def fetch_attractions(self, city, state, radius):

        data_source = urlfetch(self.yelp_search(city, state, radius))
        results = json.loads(data_source.content)

        attractions = []
        for attract_entry in results['data']
            attractions.append(attract_entry['attractsite'])

        return attractions
        ##Find Resturants
    def fetch_resturants(self, city, radius ):

        data_source = urlfetch(self.yelp_search(city, state, radius))
        results = json.loads(data_source.content)

        resturants = []
        for resturant_entry in results['data']
            resturants.append(resturant_entry['attractsite'])

        return attractions
        ##Utilize yelp search to find the resturants and attractions
    def yelp_search(self, city, radius):

        yelp_api = 'bM0VPHWh91R0g46amxYbnA'
        base_url = 'https://api.yelp.com/v2/search?'
        if
        url_params= {
            'c': city

        }

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/intro', IntroHandler),
  ('/search', SearchHandler),
], debug=True)
