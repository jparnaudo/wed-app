import webapp2
from handlers.basic_handlers import StaticHandler
from handlers.guest_handlers import UpdateGuestHandler, NewGuestHandler

config = {}
SESSION_SECRET_KEY = "test-secret-key"
config['webapp2_extras.sessions'] = {
    'secret_key': SESSION_SECRET_KEY,
}

app = webapp2.WSGIApplication([
    ('/((?!api).)*', StaticHandler),
    ('/api/guest/update', UpdateGuestHandler),
    ('/api/guest/new', NewGuestHandler)
    ], config=config,
   debug=True)