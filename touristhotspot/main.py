from google.appengine.api import users
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/intro')
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                users.create_login_url('/'))

            self.response.out.write('<html><body>%s</body></html>' % greeting)

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/greeting', MessageHandler)
], debug=True)
