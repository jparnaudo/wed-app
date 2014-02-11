
from handlers.basic_handlers import JsonAPIHandler
from model.guest_model import Guest
import logging


class NewGuestHandler(JsonAPIHandler):
    def handle(self):
        g = Guest.new()
        return {"success": True, "guest_id": g.guest_id}

class UpdateGuestHandler(JsonAPIHandler):
    def handle(self):
        
        data = {g: self.request.get(g) for g in self.request.arguments()}
        logging.warn(data)
        guest_id = int(data["guest_id"])
        g = Guest.get(guest_id)
        g.update(data)
        g.put()
        return {"success": True}

class GetGuestHandler(JsonAPIHandler):
    def handle(self):
        guest_id = int(self.request.get("guest_id"))
        g = Guest.get(guest_id)
        if not g:
            return {"success": False, "reason": "Guest not found"}
        return {"success": True, "value": g.to_dict()}