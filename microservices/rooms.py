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



@app.route('/api/rooms')
def hello_world():    
    return render_template("roomsMenu.html")

@app.route('/api/rooms/<_id>', methods=['GET'])
def search(_id): 
    if request.method == "GET":        
        url='https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+_id
        r = requests.get(url = url)
        data=r.json()
        parent_space=data['parentSpace'] 
        print(parent_space) 
        id_parent=parent_space['id']
        print(id_parent)
    return render_template("showRoom.html", room=r.json())

@app.route('/api/rooms/<_id>/location', methods=['GET'])
def show_location(_id): 
    if request.method == "GET":        
        url='https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+_id
        r = requests.get(url = url)
        data=r.json()

        parent_space=data['parentSpace'] 
        print(parent_space) 
        id_parent=parent_space['id']
        print(id_parent)

        url='https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+id_parent
        r_parent = requests.get(url = url)
        data_parent=r_parent.json()
        parent_parentSpace=data_parent['parentSpace'] 
        print(parent_parentSpace)
    return render_template("showRoomLocation.html", room=r.json(), location=parent_parentSpace)

@app.route('/api/rooms/<_id>/events', methods=['GET'])
def show_events(_id): 
    if request.method == "GET":        
        url='https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+_id
        date=datetime.datetime.today()
        today=str(date.day)+"/"+str(date.month)+"/"+str(date.year)
        r = requests.get(url = url, params={"day":today})
        data=r.json()
        
        events=data['events']
        print(events)

        events.sort(key = lambda x:(x['day'], x['period']['start']))
        
       
    return render_template("showRoomEvents.html", room=r.json(), events=events)


if __name__ == '__main__':
    app.run()