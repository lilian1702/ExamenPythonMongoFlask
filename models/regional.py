from mongoengine import *

class Regional(Document):
    
    nombre = StringField(required=True)
       
    def __str__(self):
        return self.nombre