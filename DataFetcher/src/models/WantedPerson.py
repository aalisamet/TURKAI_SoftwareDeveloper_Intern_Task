import json

class WantedPerson:

    def __init__(self, first_name:str, last_name:str, gender:str,date_of_birth:str,place_of_birth:str,nationality:str,height:str):
        self.first_name = first_name
        self.last_name = last_name
        self.gender=gender
        self.date_of_birth=date_of_birth
        self.place_of_birth=place_of_birth
        self.nationality=nationality
        self.height=height
    @classmethod
    def no_args_constructor(cls):
        cls.first_name = "" #
        cls.last_name = "" #
        cls.gender = "" #
        cls.date_of_birth = "" #
        cls.place_of_birth = "" #
        cls.nationality = "" #
        cls.height = "" #
        return cls

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.gender} {self.date_of_birth} {self.place_of_birth} {self.nationality} {self.height}"

    def return_json(self):

        wanted_person_fields_dict = {'first_name': self.first_name, 'last_name': self.last_name, 'gender': self.gender,
                                     'date_of_birth': self.date_of_birth, 'place_of_birth': self.place_of_birth,
                                     'nationality': self.nationality, 'height': self.height}

        return json.dumps(wanted_person_fields_dict)