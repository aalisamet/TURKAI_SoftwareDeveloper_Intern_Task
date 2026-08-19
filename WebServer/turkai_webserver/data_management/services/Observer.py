from abc import ABC, abstractmethod
from enum import Enum
from data_management.dto.WantedPersonDto import WantedPersonDto

class DataEventType(Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"


class DataEvent:
    def __init__(self,data,data_event_type:DataEventType) -> None:
        self.event_type: DataEventType = data_event_type
        self.data: WantedPersonDto = data

class Observer(ABC):

    @abstractmethod
    async def update( self,data_event:DataEvent) -> None:
        ...
