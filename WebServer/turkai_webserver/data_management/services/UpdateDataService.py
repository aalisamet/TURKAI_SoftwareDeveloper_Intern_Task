from typing import override

from data_management.services.Observer import Observer, DataEventType


class UpdateDataService(Observer):




    @override
    async def update(self,data_event):

            match data_event.event_type:
                case DataEventType.CREATED:
                    pass

                case DataEventType.UPDATED:
                    pass

