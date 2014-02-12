import webapp2
from handlers.basic_handlers import StaticHandler
from handlers.guest_handlers import UpdateGuestHandler, NewGuestHandler
from handlers.guest_group_handlers import NewGuestGroupHandler,\
    GetGuestGroupsListHandler

config = {}
SESSION_SECRET_KEY = "test-secret-key"
config['webapp2_extras.sessions'] = {
    'secret_key': SESSION_SECRET_KEY,
}


app = webapp2.WSGIApplication([
    ('/((?!api).)*', StaticHandler),
    ('/api/guest/update', UpdateGuestHandler),
    ('/api/guest/new', NewGuestHandler),
    ('/api/guest_group/new', NewGuestGroupHandler),
    ('/api/guest_group/list', GetGuestGroupsListHandler),
    ], config=config,
   debug=True)