from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import databases.secretariatsDB as secdb

'''
Scretariats: id, name, building, campus, opening hours e description.
endpoints:
GET
- "api/secretariats/<id>" apresenta nome, campus, edificio, horário e descrição
- "api/secretariats/<id>/location" apresenta nome, campus e edificio
- "api/secretariats/<id>/description" apresenta nome e descrição
- "api/secretariats/<id>/hours" apresenta nome, horas
POST
- "api/secretariats/create" - cria secretaria, tem que ser admin
- "api/secretariats/<id>/hours" - modificar as horas de abertura, tem que ser admin
- "api/secretariats/<id>/description" - modificar descrição, tem que ser admin
- "api/secretariats/<id>/name" - modificar nome, tem que ser admin 
'''

app = Flask(__name__)
db = secdb.secretariatsDB("secretariats")

@app.route('/api/secretariats')
def hello_world():
    count = len(db.listAllSecretariats())
    return render_template("secretariatsMenu.html", count=count)
    
@app.route('/api/secretariats/listAllSecretariats')
def list_all_Secretariats():
    list_secs = db.listAllSecretariats()
    return render_template("allSecretariats.html", list_secs=list_secs)

@app.route('/api/secretariats/create')
def create_sec_form():   
    return render_template("addSecretariatForm.html")

@app.route('/api/secretariats/addSecretariat', methods=['POST'])
def add_secretariat():   
    if request.method == "POST":
        name = str(request.form['Name'])
        campus =str(request.form['Campus'])
        building=str(request.form['Building'])
        hours=str(request.form['Hours'])
        description=str(request.form['Description'])
        db.addSecretariats(name, building, campus, hours, description)
        count = len(db.listAllSecretariats())
    return render_template("mainPage.html", count=count)

@app.route('/api/secretariats/<_id>', methods=['GET'])
def single_secretariat(_id):   
    if request.method == "GET":
        sec = db.showSecretariat(int(_id))
        sec_dict = sec.__dict__
        print(sec_dict)
    return render_template("showSecretariat.html", sec_dict=sec_dict)

@app.route('/api/secretariats/<_id>/location', methods=['GET'])
def secretariat_location(_id):   
    if request.method == "GET":
        sec=db.showLocation(int( _id))
        print(sec)       
    #return jsonify(sec) 
    return render_template("showSecretariatLocation.html", sec=sec)

@app.route('/api/secretariats/<_id>/description', methods=['GET'])
def secretariat_description(_id):   
    if request.method == "GET":
        sec=db.showDescription(int( _id))
        print(sec)       
    #return jsonify(sec) 
    return render_template("showSecretariatDescription.html", sec=sec)

@app.route('/api/secretariats/<_id>/timetable', methods=['GET'])
def secretariat_timetable(_id):   
    if request.method == "GET":
        sec=db.showHours(int( _id))
        print(sec)       
    #return jsonify(sec) 
    return render_template("showSecretariatTimetable.html", sec=sec)



if __name__ == '__main__':
    app.run()