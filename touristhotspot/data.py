from google.appengine.ext import ndb

class User(ndb.Model):

    attractions= ndb.StringProperty(repeated=True)
    resturantsBreakfast= ndb.StringProperty(repeated=True)
    resturantsGeneral= ndb.StringProperty(repeated=True)
    dateNum= ndb.IntegerProperty(required=True)
    user= ndb.StringProperty(required=True)
