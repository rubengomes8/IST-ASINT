'''
Room: id, name, building, campus, horário.
endpoints:
- "api/rooms/<id>" apresenta nome, campus, edificio e horário
- "api/rooms/<id>/events" apresenta horário
- "api/rooms/<id>/events/<ddmmyyyy>" apresenta horário de um dia
- "api/rooms/<id>/location" apresenta name, campus e building
-
'''

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import requests
import datetime

app = Flask(__name__)
log_path = './log.txt'

port_log='4003'

@app.route('/api/rooms', methods=['GET'])
def api_rooms():
    if request.method=='GET':
        send_log('microservice: rooms, get rooms, GET')
        url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'
        r = requests.get(url=url)
        data = r.json()
        return jsonify(data)

@app.route('/api/rooms/<_id>', methods=['GET'])
def search(_id):
    
    if request.method == "GET":
        send_log('microservice: rooms, get room by id, GET')
        url='https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+_id
        r = requests.get(url = url)
        data=r.json()        
        if 'error' in data:
            error = {}
            error['error'] = 404
            return jsonify(error)
        else:
            if data['type']=="ROOM":
                room={}
                room['id']=data['id']
                room['name']=data['name']
                room['description']=data['description']
                room['capacity']=data['capacity']
                return jsonify(room)
            else:
                error = {}
                error['error'] = 404
                return jsonify(error)


@app.route('/api/rooms/<_id>/location', methods=['GET'])
def show_location(_id):
    
    if request.method == "GET":
        send_log('microservice: rooms, get room location, GET')
        url='https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+_id
        r = requests.get(url = url)
        data=r.json()

        if 'error' in data:
            error = {}
            error['error'] = 404
            return jsonify(error)
        else:
            if data['type']=="ROOM":
                room={}
                room['id']=data['id']
                room['name']=data['name']
                room['description']=data['description']
                room['capacity']=data['capacity']
                parent_space=data['parentSpace'] 
                
                print(parent_space) 
                id_parent=parent_space['id']
                print(id_parent)
                data_parent={}

                url='https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+data['parentSpace']['id']
                r_parent = requests.get(url = url)
                data_parent=r_parent.json()                    
                

                while data_parent['parentSpace']['type'] != "BUILDING":                    
                    url='https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+data_parent['parentSpace']['id']
                    r_parent = requests.get(url = url)
                    data_parent=r_parent.json()                    
                    
                room['building']=data_parent['parentSpace']['name']
                room['campus']=data_parent['parentSpace']['topLevelSpace']['name']
                return jsonify(room)
            else:
                error = {}
                error['error'] = 404
                return jsonify(error)

       
    return jsonify(room)

@app.route('/api/rooms/<_id>/events', methods=['GET'])
def show_events(_id):
    
    if request.method == "GET":
        send_log('microservice: rooms, get room events, GET')
        url='https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+_id
        date=datetime.datetime.today()
        today=str(date.day)+"/"+str(date.month)+"/"+str(date.year)
        r = requests.get(url = url, params={"day":today})
        data=r.json()
        
        if 'error' in data:
            error = {}
            error['error'] = 404
            return jsonify(error)
        else:
            if data['type']=="ROOM":
                room={}
                room['id']=data['id']
                room['name']=data['name']
                room['description']=data['description']
                room['capacity']=data['capacity']

                events=data['events']
                events.sort(key = lambda x:(x['day'], x['period']['start']))
                room['events']=events
                return jsonify(room)
            else:
                error = {}
                error['error'] = 404
                return jsonify(error)

@app.route('/api/rooms/<_id>/events/<day>', methods=['GET'])
def show_date_events(_id, day):
    
    if request.method == "GET": 
        send_log('microservice: rooms, get room events by day, GET')
        _day = day[0:2]
        _month = day[2:4]
        _year = day[4:8]       
        url='https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+_id
       
        today=_day+"/"+_month+"/"+_year        
        r = requests.get(url = url, params={"day":today})
        data=r.json()
        
        if 'error' in data:
            error = {}
            error['error'] = 404
            return jsonify(error)
        else:
            if data['type']=="ROOM":
                room={}
                room['id']=data['id']
                room['name']=data['name']
                room['description']=data['description']
                room['capacity']=data['capacity']

                events=data['events']
                events.sort(key = lambda x:(x['day'], x['period']['start']))
                d_events=[]

                for item in events:
                    if item['day']==today:
                        d_events.append(item)

                room['events']=d_events
                return jsonify(room)
            else:
                error = {}
                error['error'] = 404
                return jsonify(error)

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
    app.run(port=4002,debug=True)