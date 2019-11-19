from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import databases.secretariatsDB as secdb

'''
Scretariats: id, name, building, campus, opening hours e description.
endpoints:
GET
- "api/secreteriats/<id>" apresenta nome, campus, edificio, horário e descrição
- "api/secreteriats/<id>/location" apresenta nome, campus e edificio
- "api/secreteriats/<id>/description" apresenta nome e descrição
- "api/secreteriats/<id>/hours" apresenta nome, horas
POST
- "api/secretariats/create" - cria secretaria, tem que ser admin
- "api/secretariats/<id>/hours" - modificar as horas de abertura, tem que ser admin
- "api/secretariats/<id>/description" - modificar descrição, tem que ser admin
- "api/secretariats/<id>/name" - modificar nome, tem que ser admin
'''

app = Flask(__name__)
db = secdb.secretariatsDB("secretariats")

@app.route('/')
def hello_world():
    return render_template("mainPage.html")

if __name__ == '__main__':
    app.run()