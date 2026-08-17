from time import sleep


class WantedPersonManager:

    def __init__(self):
        self.wanted_list = dict()


    @staticmethod
    def add_wanted_person(person):
        print(f"Adding {person.__str__()}")
        sleep(2)