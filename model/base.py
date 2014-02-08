from google.appengine.ext import db

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