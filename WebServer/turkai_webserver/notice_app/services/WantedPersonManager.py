from notice_app.dto.WantedPersonDto import WantedPersonDto

class WantedPersonManager:

    def __init__(self):
        self.wanted_list = dict()



    @staticmethod
    async def save_wanted_person(person_info):
        await WantedPersonManager.add_wanted_person(WantedPersonDto(person_info))


    @staticmethod
    async def add_wanted_person(person):
        if not WantedPersonManager().wanted_list.__contains__(person.id):
            WantedPersonManager().wanted_list[person.id] = person
            print("new person has been added")
        else:
            changed = WantedPersonManager().wanted_list[person.id]
            changed_field = person.is_equal(changed)
            print(changed_field)