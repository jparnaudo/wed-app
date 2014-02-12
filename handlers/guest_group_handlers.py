from handlers.basic_handlers import JsonAPIHandler
from model.guest_model import GuestGroup

class NewGuestGroupHandler(JsonAPIHandler):
    def handle(self):
        group_name = self.request.get('group_name')
        gg = GuestGroup.new(group_name)
        if not gg:
            return {"success": False, "info": "Unable to create Guest Group"}
        return {"success": True}
    
class GetGuestGroupsListHandler(JsonAPIHandler):
    def handle(self):
        guest_groups = []
        for gg in GuestGroup.get_all():
            gg = gg.to_dict()
            guest_groups.append(gg)
        return {"success": True, "list": guest_groups}

