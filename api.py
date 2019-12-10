from flask import Flask
from flask import jsonify
import requests
import datetime
from flask import request
app = Flask(__name__)

# no futuro vai ser dicionario e para cada serviço guarda: IP, porto, nome
port_sec = '4000'
port_canteen = '4001'
port_rooms = '4002'
port_log='4003'
log_path = './log.txt'
# SECRETARIAS

@app.route('/api/<path:subpath>', methods=['GET', 'POST'])
def api(subpath):
    print("asdfsaesrdgtedw:", subpath)
    words = subpath.split('/')
    microservice = words[0]
    if microservice == 'secretariats':
        port = port_sec
    elif microservice == 'canteen':
        port = port_canteen
    elif microservice == 'rooms':     
        port = port_rooms
    elif microservice == 'logs':
        port = port_log
    else:
        return {'msg': 'Not Found'}

    url = 'http://127.0.0.1:'+port+'/api/'+subpath
    if request.method=='GET':
        return jsonify(requests.get(url=url).json())
    elif request.method=='POST':
        print(url)
        
        data = request.form
        print(data)
        return jsonify(requests.post(url=url, data=data).json())

'''@app.route('/api/secretariats/', methods=['GET'])
def secretariats():
    if request.method=='GET':
        send_log('backend: api, get all secretariats, GET') 
        url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'
        #url=127.0.0.1:4000 e fazer pedido
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/secretariats/<_id>', methods=['GET'])
def secretariat(_id):
    if request.method=='GET':
        send_log('backend: api, get secretariat by id, GET')         
        url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/secretariats/<_id>/location', methods=['GET'])
def secretariat_local(_id):
    if request.method=='GET':
        send_log('backend: api, get secretariat location, GET') 
        url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id+'/location'
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/secretariats/<_id>/timetable', methods=['GET'])
def secretariat_hours(_id):
    if request.method=='GET':
        send_log('backend: api, get secretariat timetable, GET') 
        url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id+'/timetable'
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/secretariats/<_id>/description', methods=['GET'])
def secretariat_desc(_id):
    if request.method=='GET':
        send_log('backend: api, get secretariat description, GET') 
        url = 'http://127.0.0.1:'+port_sec+'/api/secretariats/'+_id+'/description'
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

# CANTINA

@app.route('/api/canteen', methods=['GET'])
def canteen():
    if request.method=='GET':
        send_log('backend: api, get canteen, GET') 
        url = 'http://127.0.0.1:'+port_canteen+'/api/canteen'
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/canteen/<_day>', methods=['GET'])
def canteen_day(_day):
    if request.method=='GET':
        send_log('backend: api, get canteen by day, GET') 
        #day = process_day(_day)
        url = 'http://127.0.0.1:'+port_canteen+'/api/canteen/'+_day
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/canteen/<_day>/lunch', methods=['GET'])
def canteen_day_lunch(_day):
    if request.method=='GET':
        send_log('backend: api, get canteen lunch by day, GET')
        
        #day = process_day(_day)

        url = 'http://127.0.0.1:'+port_canteen+'/api/canteen/'+_day+'/lunch'
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/canteen/<_day>/dinner', methods=['GET'])
def canteen_day_dinner(_day):
    if request.method=='GET':
        send_log('backend: api, get canteen dinner by day, GET')
        #day = process_day(_day)
        url = 'http://127.0.0.1:'+port_canteen+'/api/canteen/'+_day+'/dinner'
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)



# SALAS

@app.route('/api/room', methods=['GET'])
def room():
    if request.method=='GET':
        send_log('backend: api, get rooms, GET')
        url = 'http://127.0.0.1:'+port_rooms+'/api/rooms'
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/room/<_id>')
def room_info(_id):
    if request.method=='GET':
        send_log('backend: api, get room by id, GET')
        url = 'http://127.0.0.1:'+port_rooms+'/api/rooms/'+_id
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/room/<_id>/location')
def room_location(_id):
    if request.method=='GET':
        send_log('backend: api, get room location, GET')
        url = 'http://127.0.0.1:'+port_rooms+'/api/rooms/'+_id+'/location'
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/room/<_id>/events')
def room_events(_id):
    if request.method=='GET':
        send_log('backend: api, get room events, GET')
        url = 'http://127.0.0.1:'+port_rooms+'/api/rooms/'+_id+'/events'
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/room/<_id>/events/<day>')
def room_day_events(_id, day):
    if request.method=='GET':
        send_log('backend: api, get room events by day, GET')
        url = 'http://127.0.0.1:'+port_rooms+'/api/rooms/'+_id+'/events/'+day
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)'''

def add_log(type = 'empty', module = 'empty', info = 'empty'):
    global log_path
    f = open(log_path, 'a')
    f.write('Type: ' + type + ' Module: ' + module + ' Info: ' + info + '\n')
    f.close()


def send_log(msg):
    url = 'http://127.0.0.1:'+port_log+'/addlog'
    date = datetime.datetime.now()
    requests.post(url=url, data={'log': str(date) + ' - ' + msg})
    
if __name__ == '__main__':
    app.run(port=3999, debug=True)
