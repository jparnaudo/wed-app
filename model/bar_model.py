from base_model import ServiceModel
from google.appengine.ext import db

class Bar(ServiceModel):
    caterers = db.ListProperty(db.Key)
    
    