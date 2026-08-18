from data_management.dto.WantedPersonDto import WantedPersonDto
from .Observer import Observer, DataEventType, DataEvent


class WantedPersonManager:

    def __init__(self):

        self.wanted_list: dict[str, WantedPersonDto] = {}
        self.update_observers: set[Observer] = set()
        self.new_data_observers: set[Observer] = set()

    async def save_wanted_person(self, person_info) -> None:
        await self.add_wanted_person(WantedPersonDto(person_info))

    async def add_wanted_person(self, person: WantedPersonDto) -> None:
        if person.id not in self.wanted_list:
            self.wanted_list[person.id] = person
            print("New person has been added")
            await self._notify_observers(self.new_data_observers, person, DataEventType.CREATED)
            return

        old_person = self.wanted_list[person.id]
        if not person.is_equal(old_person):
            self.wanted_list[person.id] = person
            print(f"Person updated: {person.id}")
            await self._notify_observers(self.update_observers, person, DataEventType.UPDATED)


    @staticmethod
    async def _notify_observers(observers: set[Observer], person: WantedPersonDto, event_type: DataEventType) -> None:
        event = DataEvent(person, event_type)
        for observer in list(observers):

            await observer.update(event)

    # Observer Metotları
    def register_update_observer(self, new_observer: Observer) -> bool:
        self.update_observers.add(new_observer)
        return True

    def unregister_update_observer(self, observer: Observer) -> bool:
        self.update_observers.discard(observer)  # Hata fırlatmaz
        return True

    def register_new_data_observer(self, new_observer: Observer) -> bool:
        self.new_data_observers.add(new_observer)
        return True

    def unregister_new_data_observer(self, observer: Observer) -> bool:
        self.new_data_observers.discard(observer)
        return True