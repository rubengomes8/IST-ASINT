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
log_path = './log.txt'
'''
@app.route('/api/secretariats')
def hello_world():
    count = len(db.listAllSecretariats())
    return render_template("secretariatsMenu.html", count=count)'''
    
@app.route('/api/secretariats/', methods=['GET'])
def list_all_Secretariats():
    add_log('Microservices', 'secretariats', 'GET ....')
    list_secs = db.listAllSecretariats()
    print(list_secs)
    list_of_dicts = []
    for item in list_secs:
        list_of_dicts.append(item.__dict__)
    return jsonify(list_of_dicts)

##usar apenas no backend
@app.route('/api/secretariats/create')
def create_sec_form():
    add_log('Microservices', 'secretariats', 'GET ....')
    return render_template("addSecretariatForm.html")

@app.route('/api/secretariats/addSecretariat', methods=['POST'])
def add_secretariat():
    add_log('Microservices', 'secretariats', 'GET ....')
    if request.method == "POST":
        name = str(request.form['name'])
        campus =str(request.form['campus'])
        building=str(request.form['building'])
        hours=str(request.form['hours'])
        description=str(request.form['description'])
        sec = db.addSecretariats(name, building, campus, hours, description)
    return jsonify(sec.__dict__)

@app.route('/api/secretariats/<_id>', methods=['GET'])
def single_secretariat(_id):
    add_log('Microservices', 'secretariats', 'GET ....')
    if request.method == "GET":
        sec = db.showSecretariat(int(_id)) 
        if sec==-1:
            dict_={}
            dict_['error']=404
            return jsonify(dict_)   
             
    return jsonify(sec.__dict__)

@app.route('/api/secretariats/<_id>/location', methods=['GET'])
def secretariat_location(_id):
    add_log('Microservices', 'secretariats', 'GET ....')
    if request.method == "GET":
        sec=db.showLocation(int( _id))
        if sec==-1:
            dict_={}
            dict_['error']=404
            return jsonify(dict_)   
    return jsonify(sec)

@app.route('/api/secretariats/<_id>/description', methods=['GET'])
def secretariat_description(_id):
    add_log('Microservices', 'secretariats', 'GET ....')
    if request.method == "GET":
        sec=db.showDescription(int( _id))
        if sec==-1:
            dict_={}
            dict_['error']=404
            return jsonify(dict_)   
    return jsonify(sec)

@app.route('/api/secretariats/<_id>/timetable', methods=['GET'])
def secretariat_timetable(_id):
    add_log('Microservices', 'secretariats', 'GET ....')
    if request.method == "GET":
        sec=db.showHours(int( _id))
        if sec==-1:
            dict_={}
            dict_['error']=404
            return jsonify(dict_)   
    return jsonify(sec)

def add_log(type = 'empty', module = 'empty', info = 'empty'):
    global log_path
    f = open(log_path, 'a')
    f.write('Type: ' + type + ' Module: ' + module + ' Info: ' + info + '\n')
    f.close()


if __name__ == '__main__':
    app.run(port=4000)