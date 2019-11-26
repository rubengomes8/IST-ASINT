from flask import Flask
from flask import jsonify
import requests

app = Flask(__name__)

# no futuro vai ser dicionario e para cada serviço guarda: IP, porto, nome
port_sec = '4000'
port_canteen = '4001'
port_rooms = '4002'

# SECRETARIAS

@app.route('/api/secretariats/', methods=['GET'])
def secretariats():
    url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'
    #url=127.0.0.1:4000 e fazer pedido
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/secretariats/<_id>', methods=['GET'])
def secretariat(_id):
    url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/secretariats/<_id>/location', methods=['GET'])
def secretariat_local(_id):
    url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id+'/location'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/secretariats/<_id>/timetable', methods=['GET'])
def secretariat_hours(_id):
    url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id+'/timetable'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/secretariats/<_id>/description', methods=['GET'])
def secretariat_desc(_id):
    url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id+'/description'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

# CANTINA

@app.route('/api/canteen', methods=['GET'])
def canteen():
    url = 'http://127.0.0.1:'+port_canteen+'/api/canteen'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/canteen/<day>', methods=['GET'])
def canteen_day(day):
    url = 'http://127.0.0.1:'+port_canteen+'/api/canteen/'+day
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/canteen/<day>/lunch', methods=['GET'])
def canteen_day_lunch(day):
    url = 'http://127.0.0.1:'+port_canteen+'/api/canteen/'+day+'/lunch'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/canteen/<day>/dinner', methods=['GET'])
def canteen_day_dinner(day):
    url = 'http://127.0.0.1:'+port_canteen+'/api/canteen/'+day+'/dinner'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

# SALAS



if __name__ == '__main__':
    app.run(port=3999)
