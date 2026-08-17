from django.db import models

class WantedPerson(models.Model):

    def __init__(self, first_name:str, last_name:str, gender:str,date_of_birth:str,place_of_birth:str,nationality:str,height:str):
        self.first_name = first_name
        self.last_name = last_name
        self.gender=gender
        self.date_of_birth=date_of_birth
        self.place_of_birth=place_of_birth
        self.nationality=nationality
        self.height=height