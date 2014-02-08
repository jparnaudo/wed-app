from base_model import BaseModel, Address, Contact
from google.appengine.ext import db

class Caterer(BaseModel):
    name = db.StringProperty()
    address = db.ReferenceProperty(Address)
    webpage = db.StringProperty()
    contact = db.ReferenceProperty(Contact)
    recommended_by = db.StringProperty()
    days_available = db.ListProperty(db.Key)
    comment = db.StringProperty()
    venues = db.ListProperty(db.Key)
    bars = db.ListProperty(db.Key)
    budgets = db.ListProperty(db.Key)