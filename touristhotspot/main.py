import json
import jinja2
import logging
import urllib
import webapp2
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from google.appengine.api import urlfetch
from google.appengine.api import users
import random
from datetime import datetime


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

#This handler will sign the user into the website
class MainHandler(webapp2.RequestHandler): #log-in page
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/intro')
        else:
            template = jinja_environment.get_template('tour.html')
        #    login = ('login':users.create_login_url('/'))
            login = {'login':users.create_login_url('/')}
            self.response.out.write(template.render(login))

#This handler allows the user to chose if they want to "review" or if they want to make a schedule
class IntroHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('intro.html')
        logout = {'logout':users.create_logout_url('/')}
        self.response.out.write(template.render(logout))

#Allows the user to submit a review of a certain place.
class ReviewHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('reviewing.html')
        logout = {'logout':users.create_logout_url('/')}
        self.response.out.write(template.render(logout))

#Renders the search HTML for the user to input their city, state, zip code and radius in which they want to travel
class SearchHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('settings.html')
        logout = {'logout':users.create_logout_url('/')}
        self.response.write(template.render(logout))

#Sets the schedule of the user
class ScheduleHandler(webapp2.RequestHandler):

        ##post schedule
    def get(self):

        template = jinja_environment.get_template('schedule.html')

        date_format = "%m/%d/%Y"

        #gets variables from the settings html
        city = self.request.get('city')
        state = self.request.get('state')
        radius = self.request.get('radius')
        dateStart = datetime.strptime(self.request.get('dateStart'), date_format)
        dateEnd = datetime.strptime(self.request.get('dateEnd'), date_format)

        #Finds the number of days
        dateNum = (dateEnd - dateStart)


        #checks to see if user has inputed all relevant fields
        if city and state and radius and dateStart and dateEnd:
            attractions = self.fetch_attractions(city, state, radius)
            resturants = self.fetch_resturants(city, state, radius)
            variables = {
                'search_attraction': attractions,
                'search_resturant': resturants
            }
            self.response.write(template.render(variables)) #Renders the schedule Html
        else:
            self.response.write("Please specify a city, state, radius, start date, and end date")

        #fetches attractions from the yelp api
    def fetch_attractions(self, city, state, radius):

        data_source = self.yelp_search_attractions(city, state, radius)
        results = data_source

        attractions = []

        #assisgns JSON data to a directory for attractions
        for business in results.businesses:
            attractions.append(business.name)

        return attractions
        ##Fetches resturants from the yelp api
    def fetch_resturants(self, city, state, radius ):

        data_source = self.yelp_search_resturants(city, state, radius)

        resturants = []

        #assigns JSON data to a directory for resturants
        for business in data_source.businesses:
            resturants.append(business.name)

        return resturants

        ##Utilize yelp search to find the resturants and attractions
    def yelp_search_attractions(self, city, state, radius):


        cityState = city + ',' + state

        #Authentication keys for yelp
        auth = Oauth1Authenticator(
            consumer_key= 'bM0VPHWh91R0g46amxYbnA',
            consumer_secret='l-p2JF_V2BZSsNWGPRT7QywfoGE',
            token='rD8K96AXRAxiwI_R_mQwwdMUwb65Ctt_',
            token_secret= 'ugp2wQ8Pb4tcV0Qc8pc23MlkvLw'
                )

        client = Client(auth)


        params = {
            'term': 'landmarks',
            'radius_filter': str(int(radius) * 1609),
            'sort': '2'
            }

        data = client.search(cityState, **params)
        return data


    def yelp_search_resturants(self, city, state, radius):

         cityState = city + ',' + state

         auth = Oauth1Authenticator(
                 consumer_key= 'bM0VPHWh91R0g46amxYbnA',
                 consumer_secret='l-p2JF_V2BZSsNWGPRT7QywfoGE',
                 token='rD8K96AXRAxiwI_R_mQwwdMUwb65Ctt_',
                 token_secret= 'ugp2wQ8Pb4tcV0Qc8pc23MlkvLw'
                 )

         client = Client(auth)
         print "My client is authenticated" + str(client)
         params = {
                 'term': 'restaurants',
                 'radius_filter': str(int(radius) * 1609),
                 'sort': '2'
                 }

         data = client.search(cityState, **params)
         return data


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/intro', IntroHandler),
  ('/settings', SearchHandler),
  ('/schedule', ScheduleHandler)
], debug=True)
