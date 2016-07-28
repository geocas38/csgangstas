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
from data import User


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

#This handler will sign the user into the website
class MainHandler(webapp2.RequestHandler): #log-in page
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/intro')
        else:
            template = jinja_environment.get_template('tour.html')
            login = {'login':users.create_login_url('/')}
            self.response.out.write(template.render(login))

#This handler allows the user to chose if they want to "review" or if they want to make a schedule
class IntroHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('intro.html')
        logout = {'logout':users.create_logout_url('/')}
        self.response.out.write(template.render(logout))

#Allows the user to access their previous schedule
class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('calendar.html')
        logout = {'logout':users.create_logout_url('/')}
        self.response.out.write(template.render(logout))
        data = User.query().filter(User.user == users.get_current_user().email())
        print str(data) + '!!!!!!!!!!!!!!!!!!!!!!'
#pulls list out of Datastore



        userCal = User.query().filter(User.user == users.get_current_user().email())
        userAttract= userCal.get().attractions
        userRestBreak= userCal.get().resturantsBreakfast
        userRestGeneral= userCal.get().resturantsGeneral
        userDay= userCal.get().dateNum
        variables = {
        'attractions': userAttract,
        'resturantsBreakfast' : userRestBreak,
        'resturantsGeneral': userRestGeneral
        }
        self.response.write(template.render(variables))







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
        user = users.get_current_user()
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
            #Fetch calls
            attractions = self.fetch_attractions(city, state, radius)
            resturantsBreakfast = self.fetch_resturants_breakfast(city, state, radius)
            resturantsGeneral = self.fetch_resturants_general(city, state, radius)

            #Datastore


        # if User.query().filter(User.user == users.get_current_user().email()):
        #         userCal.delete()
            bizData = User(user= user.email(), attractions=attractions, resturantsBreakfast=resturantsBreakfast, resturantsGeneral= resturantsGeneral, dateNum=dateNum.days, id=user.email())
            bizData.put()
            variables = {
                'ad1p1': attractions[0:3],
                'ad1p2': attractions[3:6],
                'ad2p1': attractions[6:9],
                'ad2p2': attractions[9:12],
                'ad3p1': attractions[12:15],
                'ad3p2': attractions[15:18],
                'rd1b1': resturantsBreakfast[0:1],
                'rd2b2': resturantsBreakfast[1:2],
                'rd2b3': resturantsBreakfast[2:3],
                'rd1g1': resturantsGeneral[0:1],
                'rd1g2': resturantsGeneral[1:2],
                'rd2g3': resturantsGeneral[2:3],
                'rd2g4': resturantsGeneral[3:4],
                'rd3g5': resturantsGeneral[4:5],
                'rd3g6': resturantsGeneral[5:6]

            }
            self.response.write(template.render(variables)) #Renders the schedule Html
        else:
            self.response.write("Please specify a city, state, radius, start date, and end date")

        #fetches attractions from the yelp api


#Calls the yelp search function which accesses the yelp api and returns attractions. This function then puts those attractions into a list of strings
    def fetch_attractions(self, city, state, radius):

        data_source = self.yelp_search_attractions(city, state, radius)
        results = data_source

        attractions = []

        #assisgns JSON data to a directory for attractions
        for business in results.businesses:
            attractions.append(business.name)

        attract = self.random_shuffle(attractions)
        return attract
        #return attractions

        ##Fetches breakfast resturants from the yelp api
    def fetch_resturants_breakfast(self, city, state, radius ):

        data_source = self.yelp_search_resturants_breakfast(city, state, radius)

        resturants = []

        #assigns JSON data to a directory for resturants
        for business in data_source.businesses:
            resturants.append(business.name)

        rest = self.random_shuffle(resturants)
        return rest
        #return resturants


#Calls on the yelp search to find the lunch and dinner restaurants and puts them into a list of strings
    def fetch_resturants_general(self, city, state, radius ):

        data_source = self.yelp_search_resturants_general(city, state, radius)

        resturants = []
        #url = []

        #assigns JSON data to a directory for resturants
        for business in data_source.businesses:
            resturants.append(business.name)
            #url.append(business.url)

        rest = self.random_shuffle(resturants)
        return rest

        ##Utilize yelp search to find the resturants and attractions

#See-mongs function that allows us to randomize when a string is printed out
    def random_shuffle(self,x):
        y = [];
        while len(x) > 0:
            index = random.randint(0, len(x)-1)
            y.append(x[index])
            del x[index]
        return y

#Finds attractions for the tourist
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
            'category_filter': 'landmarks,museums,beaches',
            'radius_filter': str(int(radius) * 1609),
            'sort': '0',
            'limit': '20'
            }

        data = client.search(cityState, **params)
        return data

#This function finds only breakfast and brunch restaurants
    def yelp_search_resturants_breakfast(self, city, state, radius):

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
                 'category_filter': 'breakfast_brunch',
                 'radius_filter': str(int(radius) * 1609),
                 'sort': '0',
                 'limit':'5'
                 }

         data = client.search(cityState, **params)
         return data

#This finds lunch and dinner restaurants
    def yelp_search_resturants_general(self, city, state, radius):

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
                 'sort': '0',
                 'limit':'20'
                 }

         data = client.search(cityState, **params)
         return data

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/intro', IntroHandler),
  ('/calendar', CalendarHandler),
  ('/settings', SearchHandler),
  ('/schedule', ScheduleHandler)
], debug=True)
