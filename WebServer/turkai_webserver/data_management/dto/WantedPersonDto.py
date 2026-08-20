import json


class WantedPersonDto(object):

    def __init__(self, model_fields):
        self.data_dict = model_fields
        self.id = model_fields.get("id")
        self.first_name = model_fields.get("first_name")
        self.last_name = model_fields.get("last_name")
        self.gender = model_fields.get("gender")
        self.date_of_birth = model_fields.get("date_of_birth")
        self.place_of_birth = model_fields.get("place_of_birth")
        self.nationality = model_fields.get("nationality")
        self.height = model_fields.get("height")


    @classmethod
    def no_args_constructor(cls):
        cls.id = ""
        cls.first_name = "" #
        cls.last_name = "" #
        cls.gender = "" #
        cls.date_of_birth = "" #
        cls.place_of_birth = "" #
        cls.nationality = "" #
        cls.height = "" #
        return cls

    def is_equal(self, other):
        if not self.first_name == other.first_name:
            return "first_name"
        elif not self.last_name == other.last_name:
            return "last_name"
        elif not self.gender == other.gender:
            return "gender"
        elif not self.date_of_birth == other.date_of_birth:
            return "date_of_birth"
        elif not self.place_of_birth == other.place_of_birth:
            return "place_of_birth"
        elif not self.nationality == other.nationality:
            return "nationality"
        elif not self.height == other.height:
            return "height"
        else:
            return "nothing"

    def convert_json(self):
        return json.dumps(self.data_dict)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.gender} {self.date_of_birth} {self.place_of_birth} {self.nationality} {self.height}"