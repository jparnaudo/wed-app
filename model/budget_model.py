from base_model import BaseModel
from google.appengine.ext import db

class Budget(BaseModel):
    description = db.StringProperty() 

class VenueBudget(Budget):
    venue = db.ReferenceProperty(db.Key)