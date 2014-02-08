from base_model import Address, ServiceModel
from google.appengine.ext import db

class Venue(ServiceModel):
    address = db.ReferenceProperty(Address)
    capacity = db.IntegerProperty()
    hour_limitation = db.StringProperty()
    caterers = db.ListProperty(db.Key)
    bars = db.ListProperty(db.Key)
    djs = db.ListProperty(db.Key)
    budgets = db.ListProperty(db.Key)
    