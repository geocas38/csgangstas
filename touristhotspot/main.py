import json
import jinja2
import logging
import urllib
import rauth
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
            template = jinja_environment.get_template('tour.html')
            login = ('login':users.create_login_url('/'))
            self.response.out.write(template.render(login))
#This handler allows the user to chose if they want to "review" or if they want to make a schedule
class IntroHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('intro.html')
        logout = {'logout':users.create_logout_url('/')}
        self.response.out.write(template.render(logout))

#Renders the search HTML for the user to input their city, state, zip code and radius in which they want to travel
class SearchHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('settings.html')
        logout = {'logout':users.create_logout_url('/')}
        self.response.write(template.render(logout))

class ScheduleHandler(webapp2.RequestHandler):

        ##post schedule
    def get(self):

        template = jinja_environment.get_template('schedule.html')

        city = self.request.get('city')
        state = self.request.get('state')
        radius = self.request.get('radius')

        if city and state and radius:
            attractions = self.fetch_attractions(city, state, radius)
            resturants = self.fetch_resturants(city, state, radius)
            variables = {
                'search_attraction': attractions,
                'search_resturant': resturants
            }
            self.response.write(template.render(variables))
        else:
            self.response.write("Please specify a city, state, or radius")

        ##Find attractions
    def fetch_attractions(self, city, state, radius):

        data_source = urlfetch.fetch(self.yelp_search_attractions(city, state, radius))
        results = data_source

        attractions = []
        for attract_entry in results:
            attractions.append(attract_entry)

        return attractions
        ##Find Resturants
    def fetch_resturants(self, city, state, radius ):

        data_source = urlfetch.fetch(self.yelp_search_resturants(city, state, radius))

        results = data_source

        resturants = []
        for resturant_entry in results:
            resturants.append(resturant_entry)

        return resturants
        ##Utilize yelp search to find the resturants and attractions
    def yelp_search_attractions(self, city, state, radius):

        params= {
            'location': (city, state),
            'sort': 2,
            'limit': 25,
            'radius_filter': radius,
            'category_filter': 'landmarks, museums'
        }

         #Obtain these from Yelp's manage access page
        consumer_key = "bM0VPHWh91R0g46amxYbnA"
        consumer_secret = "l-p2JF_V2BZSsNWGPRT7QywfoGE"
        token = "rD8K96AXRAxiwI_R_mQwwdMUwb65Ctt_"
        token_secret = "ugp2wQ8Pb4tcV0Qc8pc23MlkvLw"

        session = rauth.OAuth1Session(
            consumer_key = consumer_key
            ,consumer_secret = consumer_secret
            ,access_token = token
            ,access_token_secret = token_secret)

        request = session.get("http://api.yelp.com/v2/search",params=params)

          #Transforms the JSON API response into a Python dictionary
        data = request.json()
        session.close()

        return data
    def yelp_search_resturants(self, city, state, radius):

        params= {
            'location': (city, state),
            'sort': 2,
            'limit': 25,
            'radius_filter': radius,
            'category_filter': 'resturants',
        }

         #Obtain these from Yelp's manage access page
        consumer_key = "bM0VPHWh91R0g46amxYbnA"
        consumer_secret = "l-p2JF_V2BZSsNWGPRT7QywfoGE"
        token = "rD8K96AXRAxiwI_R_mQwwdMUwb65Ctt_"
        token_secret = "ugp2wQ8Pb4tcV0Qc8pc23MlkvLw"

        session = rauth.OAuth1Session(
            consumer_key = consumer_key,
            consumer_secret = consumer_secret,
            access_token = token,
            access_token_secret = token_secret)

        request = session.get("http://api.yelp.com/v2/search",params=params)

          #Transforms the JSON API response into a Python dictionary
        data = request.json()
        session.close()

        return data



app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/intro', IntroHandler),
  ('/settings', SearchHandler),
  ('/schedule', ScheduleHandler)
], debug=True)
