import json
import jinja2
import logging
import urllib
import webapp2
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
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

        data_source = self.yelp_search_attractions(city, state, radius)
        results = data_source

        attractions = []
        for business in results.businesses:
            attractions.append(business.name)
        # for attract_entry in results['businesses']:
        #     attractions.append(attract_entry['name'])

        return attractions
        ##Find Resturants
    def fetch_resturants(self, city, state, radius ):

        data_source = self.yelp_search_resturants(city, state, radius)


        resturants = []
        for business in data_source.businesses:
            resturants.append(business.name)
        # for attract_entry in results['businesses']:
        #     attractions.append(attract_entry['name'])


        return resturants
    #
    #     data_source = self.yelp_search_resturants(city, state, radius)
    #
    #     results = data_source
    #
    #     resturants = []
    #     for resturant_entry in results:
    #         resturants.append(resturant_entry)
    #
    #     return resturants
        ##Utilize yelp search to find the resturants and attractions
    def yelp_search_attractions(self, city, state, radius):

        # params= {}
        # params["term"] = "landmarks"
        # params["location"] = "Seattle"
        # params["radius_filter"] = "2000"
        # params["limit"] = "10"



        auth = Oauth1Authenticator(
            consumer_key= 'bM0VPHWh91R0g46amxYbnA',
            consumer_secret='l-p2JF_V2BZSsNWGPRT7QywfoGE',
            token='rD8K96AXRAxiwI_R_mQwwdMUwb65Ctt_',
            token_secret= 'ugp2wQ8Pb4tcV0Qc8pc23MlkvLw'
                )

        client = Client(auth)
        print "My client is authenticated" + str(client)

        params = {
            'term': 'landmarks',
            'radius_filter': str(radius),
            'sort': '2'



                }

        data = client.search((city,state) **params)
        return data

         #Obtain these from Yelp's manage access page
        # consumer_key = "bM0VPHWh91R0g46amxYbnA"
        # consumer_secret = "l-p2JF_V2BZSsNWGPRT7QywfoGE"
        # token = "rD8K96AXRAxiwI_R_mQwwdMUwb65Ctt_"
        # token_secret = "ugp2wQ8Pb4tcV0Qc8pc23MlkvLw"

        # session = rauth.OAuth1Session(
        #     consumer_key = consumer_key
        #     ,consumer_secret = consumer_secret
        #     ,access_token = token
        #     ,access_token_secret = token_secret)
        # print ">>>>" + str(session)
        # request = session.get("http://api.yelp.com/v2/search",params={})
        # print "@@@@" + str(request)
        #   #Transforms the JSON API response into a Python dictionary
        # data = request.json()
        # session.close()
        #
        # return data


    def yelp_search_resturants(self, city, state, radius):

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
                 'radius_filter': str(radius),
                 'sort': '2'


                     }

         data = client.search((city,state) **params)
         return data
    #
    #     params= {}
    #     params["term"] = "restaurant"
    #     params["ll"] = "47.67,-123.32"
    #     params["radius_filter"] = "100000"
    #     params["limit"] = "20"
    #
    #
    #
    #
    #      #Obtain these from Yelp's manage access page
    #     consumer_key = "bM0VPHWh91R0g46amxYbnA"
    #     consumer_secret = "l-p2JF_V2BZSsNWGPRT7QywfoGE"
    #     token = "rD8K96AXRAxiwI_R_mQwwdMUwb65Ctt_"
    #     token_secret = "ugp2wQ8Pb4tcV0Qc8pc23MlkvLw"
    #
    #     session = rauth.OAuth1Session(
    #         consumer_key = consumer_key,
    #         consumer_secret = consumer_secret,
    #         access_token = token,
    #         access_token_secret = token_secret)
    #
    #     request = session.get("http://api.yelp.com/v2/search",params=params)
    #
    #       #Transforms the JSON API response into a Python dictionary
    #     data = request.json()
    #     session.close()
    #
    #     return data



app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/intro', IntroHandler),
  ('/settings', SearchHandler),
  ('/schedule', ScheduleHandler)
], debug=True)
