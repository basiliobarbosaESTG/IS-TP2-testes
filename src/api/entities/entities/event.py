import uuid
from datetime import datetime


class Event:

    def __init__(self, event, id=None, created_on=None, updated_on=None):
        self.id = id or uuid.uuid4()
        self.event = event
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "event": self.event,
        }
