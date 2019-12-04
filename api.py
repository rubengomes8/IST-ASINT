from flask import Flask
from flask import jsonify
import requests

app = Flask(__name__)

# no futuro vai ser dicionario e para cada serviço guarda: IP, porto, nome
port_sec = '4000'
port_canteen = '4001'
port_rooms = '4002'
log_path = './log.txt'
# SECRETARIAS

@app.route('/api/secretariats/', methods=['GET'])
def secretariats():
    add_log('Backend', 'api', 'GET')
    url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'
    #url=127.0.0.1:4000 e fazer pedido
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/secretariats/<_id>', methods=['GET'])
def secretariat(_id):
    add_log('Backend', 'api', 'GET')
    url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/secretariats/<_id>/location', methods=['GET'])
def secretariat_local(_id):
    add_log('Backend', 'api', 'GET')
    url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id+'/location'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/secretariats/<_id>/timetable', methods=['GET'])
def secretariat_hours(_id):
    add_log('Backend', 'api', 'GET')
    url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id+'/timetable'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/secretariats/<_id>/description', methods=['GET'])
def secretariat_desc(_id):
    add_log('Backend', 'api', 'GET')
    url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id+'/description'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

# CANTINA

@app.route('/api/canteen', methods=['GET'])
def canteen():
    add_log('Backend', 'api', 'GET')
    url = 'http://127.0.0.1:'+port_canteen+'/api/canteen'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/canteen/<_day>', methods=['GET'])
def canteen_day(_day):
    add_log('Backend', 'api', 'GET')
    day = process_day(_day)
    url = 'http://127.0.0.1:'+port_canteen+'/api/canteen/'+day
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/canteen/<_day>/lunch', methods=['GET'])
def canteen_day_lunch(_day):
    add_log('Backend', 'api', 'GET')
    day = process_day(_day)
    print(day)
    url = 'http://127.0.0.1:'+port_canteen+'/api/canteen/'+day+'/lunch'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/canteen/<_day>/dinner', methods=['GET'])
def canteen_day_dinner(_day):
    add_log('Backend', 'api', 'GET')
    day = process_day(_day)
    url = 'http://127.0.0.1:'+port_canteen+'/api/canteen/'+day+'/dinner'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)



# SALAS

@app.route('/api/room', methods=['GET'])
def room():
    add_log('Backend', 'api', 'GET')
    url = 'http://127.0.0.1:'+port_rooms+'/api/rooms'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/room/<_id>')
def room_info(_id):
    add_log('Backend', 'api', 'GET')
    url = 'http://127.0.0.1:'+port_rooms+'/api/rooms/'+_id
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/room/<_id>/location')
def room_location(_id):
    add_log('Backend', 'api', 'GET')
    url = 'http://127.0.0.1:'+port_rooms+'/api/rooms/'+_id+'/location'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/room/<_id>/events')
def room_events(_id):
    add_log('Backend', 'api', 'GET')
    url = 'http://127.0.0.1:'+port_rooms+'/api/rooms/'+_id+'/events'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/room/<_id>/events/<day>')
def room_day_events(_id, day):
    add_log('Backend', 'api', 'GET')
    url = 'http://127.0.0.1:'+port_rooms+'/api/rooms/'+_id+'/events/'+day
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

def add_log(type = 'empty', module = 'empty', info = 'empty'):
    global log_path
    f = open(log_path, 'a')
    f.write('Type: ' + type + ' Module: ' + module + ' Info: ' + info + '\n')
    f.close()

def process_day(_day):
    print(_day)
    day=_day[0:2]
    month=_day[2:4]
    print(_day[0])
    print(_day[2])
    if _day[0] == '0':
        day = _day[1]
    if _day[2] == '0':
        month = _day[3]
    print(day+month+_day[4:8])
    return day+month+_day[4:8]


    return day
if __name__ == '__main__':
    app.run(port=3999)
