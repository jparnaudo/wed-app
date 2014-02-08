from base_model import BaseModel, Address
from google.appengine.ext import db

class GuestGroup(BaseModel):
    group_name =  db.StringProperty()
    group_size = db.IntegerProperty()
    
    # devolver cantidad de gente

class Gift(BaseModel):
    gift_description =  db.StringProperty()

class Guest(BaseModel):
    name = db.StringProperty()
    surname = db.StringProperty()
    email = db.StringProperty()
    address = db.ReferenceProperty(Address)
    phone = db.StringProperty()  # int'l code, number
    guest_group = db.ReferenceProperty(GuestGroup)
    invitation_level = db.StringProperty(choices=["church", "dinner", "after_dinner"])
    table = db.IntegerProperty()
    confirmed =  db.StringProperty(choices=["yes", "no"])
    gift = db.ReferenceProperty(Gift)
    

    def get_full_name(self):
        return self.first + " " + self.last