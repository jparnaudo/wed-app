


import json
import urllib

from google.appengine.api import urlfetch
from handlers.basic_handlers import JsonAPIHandler
from model.model import Person, DATETIME_FORMAT
from model.user import User
from util import ts2dt
from model.field_metadata import FieldMetadata


class NewPersonHandler(JsonAPIHandler):
    def handle(self):
        p = Person.new()
        return {"success": True, "person_id": p.person_id}

class GetFullDictHandler(JsonAPIHandler):
    def handle(self):
        person_id = int(self.request.get("person_id"))
        p = Person.get(person_id)
        if not p:
            return {"success": False, "reason": "No such person"}
        
        return {"success": True, "value": p.to_dict_full()}

class ApprovePersonHandler(JsonAPIHandler):
    def handle(self):
        # check for user or manager, depending on risk
        person_id = int(self.request.get("person_id"))
        p = Person.get(person_id)
        if not p:
            return {"success": False, "reason": "No such person"}
        
        p_dict = p.to_dict_full()
        values = {}
        values["validationKey"] = 'f180637fc6a7a0fd712add51930fd23cdd521caa'
        values["customerId"] = 'btcchina'
        values["clientId"] = '1'
        values["name"] = 'a'
        values["age"] = 's'
        values["person"] = self.get_json(p_dict) 
        
        url = 'https://evisafe-api-4394.herokuapp.com/1/getThreatResult'
        data = urllib.urlencode(values)
        result = urlfetch.fetch(url=url,
                                payload=data,
                                method=urlfetch.POST,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        r = json.loads(result.content)
        
        if r['errorCode'] == 200:
            p.approve()
            return {"success": True}
        
        return {"success": False, "reason": "error code"+str(r['errorCode'])}

class SetPendingHandler(JsonAPIHandler):
    def handle(self):
        
        current_user = User.get(self.session.get("username") )
        if not current_user:
            return {"success": False, "reason": "You must be logged-in to create a record"}
        
        data = {p: self.request.get(p) for p in self.request.arguments()}
        person_id = int(data["person_id"])
        p = Person.get(person_id)
        if not p:
            return {"success": False, "reason": "No such person"}
        p.set_pending()
        return {"success": True}

class GetStateHandler(JsonAPIHandler):
    def handle(self):
        
        person_id = int(self.request.get("person_id"))
        p = Person.get(person_id)
        if not p:
            return {"success": False, "reason": "No such person"}
        return {"success": True, "value": p.get_state()}
    
class BasePersonListHandler(JsonAPIHandler):
    def handle(self):
        people = []
        for p in self.get_list():
            d = p.to_dict()
            d["timestamp"] = ts2dt(d["person_id"]).strftime(DATETIME_FORMAT)
            people.append(d)
        return {"success": True, "list": people}

class PersonListHandler(BasePersonListHandler):
    def get_list(self):
        return Person.get_all()

class PendingPersonListHandler(BasePersonListHandler):
    def get_list(self):
        return Person.get_pending()
    
class GetMissingMandatoryFields(JsonAPIHandler):
    def handle(self):
        person_id = int(self.request.get("person_id"))
        p = Person.get(person_id)
        return {"success": True, "fields_metadata": FieldMetadata.get_missing_fields_of(p)}