from mongoengine import *
from models.regional import Regional

class Instructores(Document):
    nombre = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    regional = ReferenceField(Regional, reverse_delete_rule=DENY, required=True)
    
    def __str__(self):
        return self.nombre
