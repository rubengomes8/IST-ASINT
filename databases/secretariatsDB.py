import models.secretariats as sec
import pickle

'''
Scretariats: id, name, building, campus, opening hours e description.
endpoints:
GET
- "api/secreteriats/<id>" apresenta nome, campus, edificio, horário e descrição
- "api/secreteriats/<id>/location" apresenta nome, campus e edificio
- "api/secreteriats/<id>/description" apresenta nome e descrição
- "api/secreteriats/<id>/hours" apresenta nome, horas
POST
- "api/secretariats/create" - cria secretaria
- "api/secretariats/<id>/hours" - modificar as horas de abertura
- "api/secretariats/<id>/description" - modificar descrição
'''

class secretariatsDB:

        def __init__(self, name):
                self.name = name
                try:
                        f = open('bd_dump'+name, 'rb')
                        self.secretariats = pickle.load(f)
                        f.close()
                except IOError:
                        self.secretariats = {}

        # for GET Methods
        def showSecretariat(self, _id):
                return self.secretariats[_id]

        def showLocation(self, _id):
                return [self.secretariats[_id].campus, self.secretariats[_id].building]

        def showDescription(self, _id):
                return self.secretariats[_id].description

        def showHours(self, _id):
                return self.secretariats[_id].timetable

        # for POST Methods
        def addSecretariats(self, name, building, campus, hours, description):
                s_id = len(self.secretariats)
                self.secretariats[s_id] = sec.secretariats(name, campus, building, hours, description)
                f = open('bd_dump'+self.name, 'wb')
                pickle.dump(self.secretariats, f)
                f.close()

        def changeHours(self, hours, _id):
                self.secretariats[_id].timetable = hours

        def changeDescription(self, description, _id):
                self.secretariats[_id].description = description

        def changeName(self, name, _id):
                self.secretariats[_id].name = name






