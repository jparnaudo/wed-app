import datetime
import json
import webapp2
from webapp2_extras import sessions

from path import jinja_environment
from util import dt2ts


class StaticHandler(webapp2.RequestHandler):
    def get(self, _):

        name = self.request.path.split("/")[1]
        if name == "":
            name = "welcome"

        values = {
            "name": name
        }
        
        try:
            self.response.write(jinja_environment.get_template("/templates/" + name + '.html').render(values))
        except IOError, e:
            self.error(404)
            self.response.write("404: %s not found! %s" % (name, e))


class ImageHandler(webapp2.RequestHandler):
    def get(self):
        blob = self.get_blob()
        if blob:
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.headers['Cache-Control'] = 'no-cache'
            self.response.out.write(blob)
        else:
            self.redirect('/static/img/noimage.jpg')
            
class BaseSessionHandler(webapp2.RequestHandler):
    def dispatch(self):
        # get a session store for this request
        self.session_store = sessions.get_store(request=self.request)
        try:
            # dispatch the request
            webapp2.RequestHandler.dispatch(self)
        finally:
            # save all sessions
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        backend = "securecookie"  # default
        return self.session_store.get_session(backend=backend)
        
class JsonAPIHandler(BaseSessionHandler):
    def post(self):
        self.get()
        
    def get(self):
        resp = self.handle()
        self.response.headers['Content-Type'] = "application/json"
        dthandler = lambda obj: dt2ts(obj) if isinstance(obj, datetime.datetime) else None
        self.response.write(json.dumps(resp, default=dthandler))
    
    def get_json(self, data):
        dthandler = lambda obj: dt2ts(obj) if isinstance(obj, datetime.datetime) else None
        return json.dumps(data, default=dthandler)