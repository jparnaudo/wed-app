import webapp2
from handlers.basic_handlers import StaticHandler

config = {}
SESSION_SECRET_KEY = "test-secret-key"
config['webapp2_extras.sessions'] = {
    'secret_key': SESSION_SECRET_KEY,
}

app = webapp2.WSGIApplication([
    ('/((?!api).)*', StaticHandler)], config=config,
   debug=True)