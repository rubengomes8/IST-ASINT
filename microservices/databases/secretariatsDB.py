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
                if _id > len(self.secretariats) - 1 or _id <= -1:
                       return -1
                return self.secretariats[_id]

        def showLocation(self, _id):
                if _id > len(self.secretariats) - 1 or _id <= -1:
                       return -1
                dict_ = {}
                dict_['name'] = self.secretariats[_id].name
                dict_['campus'] = self.secretariats[_id].campus
                dict_['building'] = self.secretariats[_id].building
                return dict_

        def showDescription(self, _id):
                if _id > len(self.secretariats) - 1 or _id <= -1:
                       return -1
                dict_ = {}
                dict_['name'] = self.secretariats[_id].name
                dict_['description'] = self.secretariats[_id].description                
                return dict_
              

        def showHours(self, _id):
                if _id > len(self.secretariats) - 1 or _id <= -1:
                       return -1
                dict_ = {}
                dict_['name'] = self.secretariats[_id].name
                dict_['timetable'] = self.secretariats[_id].timetable                
                return dict_
        # for POST Methods
        def addSecretariats(self, name, building, campus, hours, description):
                s_id = len(self.secretariats)
                self.secretariats[s_id] = sec.secretariats(s_id,name, campus, building, hours, description)
                f = open('bd_dump'+self.name, 'wb')
                pickle.dump(self.secretariats, f)
                f.close()
                return self.secretariats[s_id]

        def changeHours(self, hours, _id):
                self.secretariats[_id].timetable = hours

        def changeDescription(self, description, _id):
                self.secretariats[_id].description = description

        def changeName(self, name, _id):
                self.secretariats[_id].name = name

        def listAllSecretariats(self):
                return list(self.secretariats.values())






