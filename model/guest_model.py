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
    confirmed =  db.StringProperty(choices=[YES, NO])
    guest_group = db.ListProperty(db.Key)
    gift = db.StringProperty()
    
    @classmethod
    def get_all(cls):
        return cls.all()

    @classmethod
    def get(cls, ts):
        return cls.all().filter("guest_id =", ts).get()

    @classmethod
    def new(cls):
        g = cls()
        g.guest_id = dt2ts(datetime.datetime.now())
        g.address = Address().put()
        g.confirmed = NO
        g.put()
        return g
    
    def update(self, data):
        #self.address.update(data['address'])
        del data['address']
        if 'group' in data:
            ''' CREAR LOS GUESTGROUPS EN API/BOOTSTRAP! '''
            #self.add_guest_group(data['group'])
            del data['group']
        if 'table' in data:
            ''' CREAR LAS TABLES EN API/BOOTSTRAP! '''
            #Table().get('table_number = ', data['table']).add_member(data['guest_id'])
            del data['table']
        del data['guest_id']
        super(Guest, self).update(data)
        
    def get_full_name(self):
        return self.name + " " + self.surname
    
    def to_dict(self):
        g = db.to_dict(self)
        return g
    
    def to_dict_full(self):
        g = db.to_dict(self)
        g["address"] = self.address.to_dict()
        return g
    
    
    def add_guest_group(self, guest_group):
        group = GuestGroup.gql("WHERE name = ", guest_group).get()
        
        if group.key() not in self.guest_group:
            self.guest_group.append(group.key())
            self.put()
  
class GuestGroup(BaseModel):
    group_name =  db.StringProperty()
    group_size = db.IntegerProperty()
    
    @property
    def members(self):
        return Guest.gql("WHERE groups = :1", self.key())
    
class Table(BaseModel):
    table_number =  db.StringProperty()
    table_members = db.ListProperty(db.Key)
    
    @property
    def members(self):
        return len(self.table_members)
    
    def add_member(self, guest_id):
        guest = Guest.gql("WHERE guest_id = ", guest_id).get()
        
        if guest.key() not in self.table_members:
            self.table_members.append(guest.key())
            self.put()
           
