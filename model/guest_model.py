from base_model import BaseModel, Address
from google.appengine.ext import db
import datetime
from util import dt2ts

YES = "yes"
NO = "no"
class Guest(BaseModel):
    guest_id = db.IntegerProperty()
    name = db.StringProperty()
    surname = db.StringProperty()
    email = db.StringProperty()
    address = db.ReferenceProperty(Address)
    phone = db.StringProperty()  
    invitation_level = db.StringProperty(choices=["church", "dinner", "after_dinner"])
    table = db.IntegerProperty()
    confirmed =  db.StringProperty(choices=[YES, NO])
    guest_group = db.ListProperty(db.Key)
    # gifts
    
    @classmethod
    def get_all(cls):
        return cls.all()

    @classmethod
    def get(cls, ts):
        return cls.all().filter("guest_id =", ts).get()

    @classmethod
    def new(cls, gift):
        g = cls()
        g.guest_id = dt2ts(datetime.datetime.now())
        g.address = Address().put()
        g.confirmed = NO
        g.put()
        return g
    
    def get_full_name(self):
        return self.name + " " + self.surname
    
    def to_dict(self):
        g = db.to_dict(self)
        return g
    
    def to_dict_full(self):
        g = db.to_dict(self)
        g["address"] = self.address.to_dict()
        g["gifts"] = ""
        for gift in self.gifts:
            g["gifts"] = g["gifts"] + gift + ","
        return g
    
    
    def add_guest_group(self, guest_group):
        group = GuestGroup.gql("WHERE name = ", guest_group).get()
        
        if group.key() not in self.guest_group:
            self.guest_group.append(group.key())
            self.put()
            
    def add_gift(self, gift_description):
        Gift(guest=self, gift_description = gift_description).put()
        
class Gift(BaseModel):
    guest = db.ReferenceProperty(Guest, collection_name='gifts')
    gift_description =  db.StringProperty()

  
class GuestGroup(BaseModel):
    group_name =  db.StringProperty()
    group_size = db.IntegerProperty()
    
    @property
    def members(self):
        return Guest.gql("WHERE groups = :1", self.key())