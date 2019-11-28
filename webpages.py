from flask import Flask
from flask import render_template
from flask import jsonify
import requests
from flask import request

app = Flask(__name__)

port_api='3999'
port_webpages='3998'
log_path='./log.txt'

@app.route('/', methods=['GET'])
def initial_menu():
    add_log('Backend', 'Web Pages', 'GET mainPage.html')
    return render_template("mainPage.html")

# SECRETARIA

@app.route('/secretariats', methods=['GET'])
def secretariats_menu():
    add_log('Backend', 'Web Pages', 'GET secretariatsMenu.html')
    return render_template("secretariatsMenu.html")

@app.route('/secretariats/all', methods=['GET'])
def all_secretariats():
    add_log('Backend', 'Web Pages', 'GET allSecretariats.html')
    url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'
    print(url)
    r = requests.get(url=url)
    return render_template("allSecretariats.html", list_secs=r.json())

@app.route('/secretariats/<_id>', methods=['GET'])
def secretariat(_id):
    add_log('Backend', 'Web Pages', 'GET showSecretariat.html')
    url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id
    print(url)
    r = requests.get(url=url)
    return render_template("showSecretariat.html", sec_dict=r.json())

@app.route('/secretariats/<_id>/location', methods=['GET'])
def secretariat_local(_id):
    add_log('Backend', 'Web Pages', 'GET showSecretariatLocation.html')
    url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/location'
    print(url)
    r = requests.get(url=url)
    print(r.json())
    return render_template("showSecretariatLocation.html", sec=r.json())

@app.route('/secretariats/<_id>/timetable', methods=['GET'])
def secretariat_timetable(_id):
    add_log('Backend', 'Web Pages', 'GET showSecretariatTimetable.html')
    url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/timetable'
    print(url)
    r = requests.get(url=url)
    print(r.json())
    return render_template("showSecretariatTimetable.html", sec=r.json())

@app.route('/secretariats/<_id>/description', methods=['GET'])
def secretariat_desc(_id):
    add_log('Backend', 'Web Pages', 'GET showSecretariatDescription.html')
    url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/description'
    print(url)
    r = requests.get(url=url)
    print(r.json())
    return render_template("showSecretariatDescription.html", sec=r.json())

@app.route('/secretariats/create')
def create_sec_form():
    add_log('Backend', 'Web Pages', 'GET addSecretariatForm.html')
    return render_template("addSecretariatForm.html")

@app.route('/secretariats/addSecretariat', methods=['POST'])
def add_secretariat():
    add_log('Backend', 'Web Pages', 'POST addSecretariat')
    if request.method == "POST":
        url = 'http://127.0.0.1:' + port_api + '/api/secretariats/addSecretariat'
        data = {
            'name': str(request.form['Name']),
            'campus': str(request.form['Campus']),
            'building': str(request.form['Building']),
            'hours': str(request.form['Hours']),
            'description': str(request.form['Description'])
        }
        r = requests.post(url=url, data=data)
    return jsonify(r.json())

# CANTINA

@app.route('/canteen', methods=['GET'])
def canteen():
    add_log('Backend', 'Web Pages', 'GET canteenForm.html')
    return render_template('canteenForm.html')


@app.route('/canteen/<day>', methods=['GET'])
def canteen_day(day):
    add_log('Backend', 'Web Pages', 'GET showLunchDinner.html')
    url = 'http://127.0.0.1:' + port_api + '/api/canteen/' + day + '/lunch'
    print(url)
    r = requests.get(url=url)
    lunch = r.json()
    url = 'http://127.0.0.1:' + port_api + '/api/canteen/' + day + '/dinner'
    print(url)
    r = requests.get(url=url)
    dinner = r.json()
    return render_template("showLunchDinner.html", list_lunch=lunch, list_dinner=dinner)
    return jsonify(data)

@app.route('/canteen/<day>/lunch', methods=['GET'])
def canteen_lunch(day):
    add_log('Backend', 'Web Pages', 'GET showLunch.html')
    url = 'http://127.0.0.1:' + port_api + '/api/canteen/'+day+'/lunch'
    print(url)
    r = requests.get(url=url)
    data = r.json()
    return render_template("showLunch.html", list=data)

@app.route('/canteen/<day>/dinner', methods=['GET'])
def canteen_dinner(day):
    add_log('Backend', 'Web Pages', 'GET showDinner.html')
    url = 'http://127.0.0.1:' + port_api + '/api/canteen/'+day+'/dinner'
    print(url)
    r = requests.get(url=url)
    data = r.json()
    return render_template("showDinner.html", list=data)
    #return jsonify(data)

#Rooms

@app.route('/rooms', methods=['GET'])
def rooms_menu():
    add_log('Backend', 'Web Pages', 'GET roomsMenu.html')
    return render_template("roomsMenu.html", port_webpages=port_webpages)

@app.route('/rooms/<_id>', methods=['GET'])
def room(_id):
    add_log('Backend', 'Web Pages', 'GET showRoom.html')
    url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id
    print(url)
    r = requests.get(url=url)
    data = r.json()
    if 'error' in data.keys():
        return jsonify(data)
    else:
        return render_template("showRoom.html", room=data,  port_webpages=port_webpages)
    
        
@app.route('/rooms/<_id>/location', methods=['GET'])
def room_location(_id):
    add_log('Backend', 'Web Pages', 'GET showRoomLocation.html')
    url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id+'/location'
    print(url)
    r = requests.get(url=url)
    data = r.json()
    if 'error' in data.keys():
        return jsonify(data)
    else:
        return render_template("showRoomLocation.html", room=data,  port_webpages=port_webpages)

@app.route('/rooms/<_id>/events', methods=['GET'])
def room_events(_id):
    add_log('Backend', 'Web Pages', 'GET showRoomEvents.html')
    url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id+'/events'
    print(url)
    r = requests.get(url=url)
    data = r.json()
    if 'error' in data.keys():
        return jsonify(data)
    else:
        return render_template("showRoomEvents.html", room=data, events=data['events'] ,port_webpages=port_webpages)

@app.route('/rooms/<_id>/events/<day>', methods=['GET'])
def room_events_day(_id,day):
    url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id+'/events/'+day
    print(url)
    r = requests.get(url=url)
    data = r.json()
    if 'error' in data.keys():
        return jsonify(data)
    else:
        return render_template("showRoomEvents.html", room=data, events=data['events'] ,port_webpages=port_webpages)

def add_log(type = 'empty', module = 'empty', info = 'empty'):
    global log_path
    f = open(log_path, 'a')
    f.write('Type: ' + type + ' Module: ' + module + ' Info: ' + info + '\n')
    f.close()

if __name__ == '__main__':
    app.run(port=3998)