from google.appengine.ext import db
from util import dt2ts


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%d-%m-%Y"
MONTH_FORMAT = '%Y-%m'

class BaseModel(db.Model):
    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        self.put()

    def to_dict(self):
        d = db.to_dict(self)
        return d
    
    def delete(self):
        d = db.delete(self)
        return d

class Contact(BaseModel):
    contact_name = db.StringProperty()
    contact_phone = db.StringProperty()
    contact_email = db.StringProperty()
    
class Address(BaseModel):
    street_address = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    zip = db.StringProperty()
    country = db.StringProperty()
    
class Period(BaseModel):
    start = db.DateProperty()
    end = db.DateProperty()

    def to_dict(self):
        d = db.to_dict(self)
        if self.start : d["start"] = self.start.strftime(DATE_FORMAT)
        if self.end : d["end"] = self.end.strftime(DATE_FORMAT)
        return d

class ServiceModel(BaseModel):
    name = db.StringProperty()
    webpage = db.StringProperty()
    recommended_by = db.StringProperty()
    contact = db.ReferenceProperty(Contact)
    days_available = db.ListProperty(db.Key)
    comment = db.StringProperty()
    venues = db.ListProperty(db.Key)
    budgets = db.ListProperty(db.Key)

