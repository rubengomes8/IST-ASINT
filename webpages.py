from flask import Flask
from flask import render_template
from flask import jsonify
from flask import redirect
import requests
from flask import request
import datetime
import uuid

app = Flask(__name__)

port_api='3998'
port_webpages='3998'
log_path='./log.txt'

services = {
    'secretariats': "http://127.0.0.1:4000",
    'canteen': "http://127.0.0.1:4001",
    'room': "http://127.0.0.1:4002",
    'logs': "http://127.0.0.1:4003"
}
port_sec = '4000'
port_canteen = '4001'
port_rooms = '4002'
port_log='4003'

redirect_uri = "http://127.0.0.1:3998/userAuth" # this is the address of the page on this app
client_id= "1695915081465934" # copy value from the app registration
clientSecret = "WVVcjUVINVFwgXDyG1VOzLNN5Q4AU6tHt8/6LKFsswA+Tj00Yc9j1ryu5AKyrBDv+no+UbIUIB3INUWzw1w9Mg==" # copy value from the app registration
fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

loginName = False
userToken = None
code = False
users_dict = {}

adminName = False
adminToken = None
admin_username = "admin"
admin_password = "123"
secret = 1
get_users_dict = {}

@app.route('/', methods=['GET']) 
def login():
    return render_template("Login.html")


@app.route('/api/<path:subpath>', methods=['GET', 'POST'])
def api(subpath):
    global services
    print("subpath:", subpath)
    words = subpath.split('/')
    microservice = words[0]
    try:
        url = services[str(microservice)] + '/api/' + subpath
        print(url)
    except:
        return {'msg': 'Not Found'}

    if request.method == 'GET':
        return jsonify(requests.get(url=url).json())
    elif request.method == 'POST':
        print(url)

        data = request.form
        print(data)
        return jsonify(requests.post(url=url, data=data).json())

    '''if microservice == 'secretariats':
        port = port_sec
    elif microservice == 'canteen':
        port = port_canteen
    elif microservice == 'room':
        port = port_rooms
    elif microservice == 'logs':
        port = port_log
    else:
        return {'msg': 'Not Found'}
    url = 'http://127.0.0.1:' + port + '/api/' + subpath'''

@app.route('/users', methods=['GET'])
def show_users_dict():
    return jsonify(users_dict)

@app.route('/admin', methods=['POST'])
def admin():
    global adminToken
    global admin_username
    global admin_password
    if str(request.form['username'])  == admin_username and str(request.form['password']) == admin_password:
        adminToken = str(uuid.uuid1())
        users_dict[str(adminToken)] = ("admin", str(adminToken))
        return render_template("mainPage.html", key=str(adminToken))

@app.route('/getgetusersdict', methods=['POST'])
def get_getusersdict():
    s = request.json["secret"]
    return jsonify({'name': get_users_dict[int(s)][0], 'photo': get_users_dict[int(s)][1]['data']})


@app.route('/getuser', methods=['POST'])
def getuser():
    global get_users_dict
    if(request.is_json):
        s = request.json["secret"]
        key = request.json["key"]
        for user in users_dict.values():
            if s == user[4]:
                get_users_dict[int(s)] = (users_dict[str(key)][2], users_dict[str(key)][3]) # name and photo
                return jsonify({'name': user[2], 'photo': user[3]['data']}) #only istid
        return jsonify({'name': 'user not found', 'photo': 'user not found'})
    else:
        return "XXXX"

@app.route('/clean', methods=['POST'])
def clean():
    global get_users_dict
    if(request.is_json):
        s = request.json["secret"]
        for user in users_dict.values():
            if s == user[4]:
                get_users_dict[int(s)] = ("", {})

@app.route('/private', methods=['GET'])
def private_page():
    redPage = fenixLoginpage % (client_id, redirect_uri)
    return redirect(redPage)

@app.route('/userAuth')
def userAuthenticated():
    #This page is accessed when the user is authenticated by the fenix login pagesetup
    #first we get the secret code retuner by the FENIX login
    code = request.args['code']
    # we now retrieve a fenix access token
    payload = {'client_id': client_id, 'client_secret': clientSecret, 'redirect_uri' : redirect_uri, 'code' : code, 'grant_type': 'authorization_code'}
    response = requests.post(fenixacesstokenpage, params = payload)
    if(response.status_code == 200):
        #if we receive the token
        r_token = response.json()
        params = {'access_token': r_token['access_token']}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        r_info = resp.json()
        print(r_info)
        # precisamos de guardar o nome e foto
        key = str(uuid.uuid1())
        global users_dict
        global secret
        # 0 - username, 1 - token, 2 - name, 3 - photo, 4 - secret, 5 - name_friend, 6 - photo_friend
        users_dict[str(key)] = (r_info['username'], r_token['access_token'], r_info['name'], r_info['photo'], str(secret), "", {}) # photo é um dict com {'type': 'image/png', 'data': 'sdsdsds'}
        secret += 1
        get_users_dict[secret] = ("", {})
        send_log('backend: webpages, render services options, GET')
        return render_template("mainPage.html", key=str(key))
    else:
        return render_template("Login.html")

# SECRETARIA

@app.route('/secretariats', methods=['GET'])
def secretariats_menu():
    send_log('backend: webpages, render secretariats options, GET')
    return render_template("secretariatsMenu.html", port_webpages=port_webpages)



@app.route('/secretariats/all', methods=['GET'])
def all_secretariats():
    send_log('backend: webpages, render all secretariats, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'
    r = requests.get(url=url)
    return render_template("allSecretariats.html", list_secs=r.json())



@app.route('/secretariats/<_id>', methods=['GET'])
def secretariat(_id):
    send_log('backend: webpages, render secretariat by id, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id
    r = requests.get(url=url)
    return render_template("showSecretariat.html", sec_dict=r.json())

@app.route('/secretariats/test/<_id>', methods=['GET'])
def secretariat_test(_id):
    send_log('backend: webpages, render secretariat by id, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id
    r = requests.get(url=url)
    return jsonify(r.json())

@app.route('/secretariats/<_id>/location', methods=['GET'])
def secretariat_local(_id):
    send_log('backend: webpages, render secretariat location, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/location'
    r = requests.get(url=url)
    return render_template("showSecretariatLocation.html", sec=r.json())

@app.route('/secretariats/<_id>/timetable', methods=['GET'])
def secretariat_timetable(_id):
    send_log('backend: webpages, render secretariat timetable, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/timetable'
    r = requests.get(url=url)
    return render_template("showSecretariatTimetable.html", sec=r.json())
        

@app.route('/secretariats/<_id>/description', methods=['GET'])
def secretariat_desc(_id):
    send_log('backend: webpages, render secretariat description, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/description'
    r = requests.get(url=url)
    return render_template("showSecretariatDescription.html", sec=r.json())

# ADMIN

@app.route('/logs/getlogs',methods=['GET'])
def get_logs():
    global users_dict
    #try:
    if str(request.args['id']) in users_dict:
        if str(request.args['id']) == adminToken:
            send_log('backend: webpages, render logs, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/logs/getlogs'
            print(url)
            return jsonify(requests.get(url=url).json())
        else:
            return jsonify({"error": "you do not have permission"})
    else:
        return redirect('/private')
    #except:
        #return redirect('/private')

@app.route('/secretariats/create',methods=['GET'])
def create_sec_form():
    global users_dict  
    try:
        if str(request.args['id']) in users_dict:
            if str(request.args['id']) == adminToken:
                send_log('backend: webpages, render add secretariat form, GET')
                return render_template("addSecretariatForm.html", key=request.args['id'])
            else:
                return jsonify({"error": "you do not have permission"})
        else:
            return redirect('/private')
    except:
        return redirect('/private')

@app.route('/secretariats/addSecretariat', methods=['POST'])
def add_secretariat():
    global users_dict
    try:
        if str(request.args['id']) in users_dict:
            send_log('backend: webpages,  add secretariat, POST')
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
        else:
            return redirect('/private')
    except:
        return redirect('/private')

@app.route('/secretariats/edit', methods=['GET'])
def edit_sec_form():
    global users_dict
    try:
        if str(request.args['id']) in users_dict:
            if str(request.args['id']) == adminToken:
                send_log('backend: webpages, render edit secretariat form, GET')
                return render_template("editSecretariatForm.html", key=request.args['id'])
            else:
                return jsonify({"error": "you do not have permission"})
        else:
            return redirect('/private')
    except:
        return redirect('/private')


@app.route('/secretariats/editSecretariat', methods=['POST'])
def edit_secretariat():
    global users_dict
    if str(request.args['id']) in users_dict:
        send_log('backend: webpages, edit secretariat, POST')
        url = 'http://127.0.0.1:' + port_api + '/api/secretariats/editSecretariat'
        data = {
            'name': str(request.form['Name']),
            'campus': str(request.form['Campus']),
            'building': str(request.form['Building']),
            'hours': str(request.form['Hours']),
            'description': str(request.form['Description'])
        }
        r = requests.post(url=url, data=data)
        return jsonify(r.json())
    else:
        return redirect('/private')

# CANTINA
@app.route('/canteen', methods=['GET'])
def canteen():
    send_log('backend: webpages, render canteen form, GET')
    return render_template('canteenForm.html')


@app.route('/canteen/<day>', methods=['GET'])
def canteen_day(day):
    send_log('backend: webpages, render canteen lunch and dinner, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/canteen/' + day + '/lunch'
    r = requests.get(url=url)
    lunch = r.json()
    url = 'http://127.0.0.1:' + port_api + '/api/canteen/' + day + '/dinner'
    r = requests.get(url=url)
    dinner = r.json()
    if 'error' in lunch and 'error' in dinner:
        return jsonify("{'error': 'Canteen closed'}")
    else:
        return render_template("showLunchDinner.html", list_lunch=lunch, list_dinner=dinner)

@app.route('/canteen/<day>/lunch', methods=['GET'])
def canteen_lunch(day):
    send_log('backend: webpages, render canteen lunch, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/canteen/'+day+'/lunch'
    r = requests.get(url=url)
    data = r.json()
    if 'error' in data:
        return jsonify("{'error': 'Canteen closed'}")
    else:
        return render_template("showLunch.html", list=data)

@app.route('/canteen/<day>/dinner', methods=['GET'])
def canteen_dinner(day):
    send_log('backend: webpages, render canteen dinner, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/canteen/'+day+'/dinner'
    r = requests.get(url=url)
    data = r.json()
    if 'error' in data:
        return jsonify("{'error': 'Canteen closed'}")
    else:
        return render_template("showDinner.html", list=data)

#Rooms
@app.route('/rooms', methods=['GET'])
def rooms_menu():
    send_log('backend: webpages, render rooms form, GET')
    return render_template("roomsMenu.html", port_webpages=port_webpages)


@app.route('/rooms/<_id>', methods=['GET'])
def room(_id):
    send_log('backend: webpages, render room by id, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id
    r = requests.get(url=url)
    data = r.json()
    if 'error' in data.keys():
        return jsonify(data)
    else:
        return render_template("showRoom.html", room=data,  port_webpages=port_webpages)

    
        
@app.route('/rooms/<_id>/location', methods=['GET'])
def room_location(_id):
    send_log('backend: webpages, render room location, GET')

    url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id+'/location'
    r = requests.get(url=url)
    data = r.json()
    if 'error' in data.keys():
        return jsonify(data)
    else:
        return render_template("showRoomLocation.html", room=data,  port_webpages=port_webpages)


@app.route('/rooms/<_id>/events', methods=['GET'])
def room_events(_id):
    send_log('backend: webpages, render room events, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id+'/events'
    r = requests.get(url=url)
    data = r.json()
    if 'error' in data.keys():
        return jsonify(data)
    else:
        return render_template("showRoomEvents.html", room=data, events=data['events'] ,port_webpages=port_webpages)



@app.route('/rooms/<_id>/events/<day>', methods=['GET'])
def room_events_day(_id, day):
    send_log('backend: webpages, render room events by day, GET')
    url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id+'/events/'+day
    r = requests.get(url=url)
    data = r.json()
    if 'error' in data.keys():
        return jsonify(data)
    else:
        return render_template("showRoomEvents.html", room=data, events=data['events'] ,port_webpages=port_webpages)




# MOBILE APP

@app.route('/qrcode', methods=['GET'])
def qrcode():
    global users_dict
    try:
        if str(request.args['id']) in users_dict:
            send_log('mobile app: qrcode')
            return render_template("qrCode.html", key=request.args['id'])
        else:
            send_log('mobile app: qr code | INVALID KEY')
            return redirect('/private')
    except:
        send_log('mobile app: qr code | INVALID KEY')
        return redirect('/private')

@app.route('/mysecret', methods=['GET'])
def my_secret():
    global users_dict
    key = str(request.args['id'])
    try:
        if key in users_dict:
            send_log('mobile app: my secret')
            return render_template("mySecret.html", key=key, secret=users_dict[key][4])
        else:
            send_log('mobile app: my secret | INVALID KEY')
            return redirect('/private')
    except:
        send_log('mobile app: my secret | INVALID KEY')
        return redirect('/private')


@app.route('/findsecret', methods=['GET'])
def find_secret():
    global users_dict
    try:
        if str(request.args['id']) in users_dict:
            send_log('mobile app: find secret')
            return render_template("findSecret.html", key=request.args['id'], users=users_dict)
        else:
            send_log('mobile app: find secret | INVALID KEY')
            return redirect('/private')
    except:
        send_log('mobile app: find secret | INVALID KEY')
        return redirect('/private')


def send_log(msg):
    url = 'http://127.0.0.1:'+port_log+'/addlog'
    date = datetime.datetime.now()
    requests.post(url=url, data={'log': str(date) + ' - ' + msg})
    data={'msg' : '200 - OK'}
    return data

if __name__ == '__main__':
    app.run(port=3998,debug=True)