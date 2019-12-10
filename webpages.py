from flask import Flask
from flask import render_template
from flask import jsonify
from flask import redirect
import requests
from flask import request
import auth
import datetime
import uuid

app = Flask(__name__)

port_api='3999'
port_webpages='3998'
log_path='./log.txt'
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

@app.route('/', methods=['GET']) 
def login():
    return render_template("Login.html", username=loginName)

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
        # precisamos de guardar o nome e foto
        key = str(uuid.uuid1())
        global users_dict
        users_dict[str(key)] = (r_info['username'], r_token['access_token'])
        send_log('backend: webpages, render services options, GET')
        return render_template("mainPage.html", key=str(key))
    else:
        return 'oops2'


# LOGS

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

# SECRETARIA

@app.route('/secretariats', methods=['GET'])
def secretariats_menu():
    global users_dict
    try:
        if str(request.args['id']) in users_dict:
            send_log('backend: webpages, render secretariats options, GET')
            print("Secretariats menu key:", request.args['id'])
            return render_template("secretariatsMenu.html", key=request.args['id'])
        else:
            print("else in secretariats_menu")
            return redirect('/private')
    except:
        return redirect('/private')


@app.route('/secretariats/all', methods=['GET'])
def all_secretariats():
    global users_dict    
    try:
        print("List of All Secretariats key:", request.args['id'])
        if str(request.args['id']) in users_dict:
            send_log('backend: webpages, render all secretariats, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'
            r = requests.get(url=url)
            return render_template("allSecretariats.html", list_secs=r.json(), key=request.args['id'])
        else:
            print("else in all_secretariats")
            return redirect('/private')
    except:
        return redirect('/private')

@app.route('/secretariats/<_id>', methods=['GET'])
def secretariat(_id):
    global users_dict  
    try:
        if str(request.args['id']) in users_dict:
            send_log('backend: webpages, render secretariat by id, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id
            r = requests.get(url=url)
            return render_template("showSecretariat.html", sec_dict=r.json(), key=request.args['id'])
        else:
            return redirect('/private')
    except:
        return redirect('/private')


@app.route('/secretariats/<_id>/location', methods=['GET'])
def secretariat_local(_id):
    global users_dict  
    try:
        if str(request.args['id']) in users_dict:
            send_log('backend: webpages, render secretariat location, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/location'
            r = requests.get(url=url)
            return render_template("showSecretariatLocation.html", sec=r.json(), key=request.args['id'])
        else:
            return redirect('/private')
    except:
        return redirect('/private')

@app.route('/secretariats/<_id>/timetable', methods=['GET'])
def secretariat_timetable(_id):
    global users_dict  
    try:
        if str(request.args['id']) in users_dict:
            send_log('backend: webpages, render secretariat timetable, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/timetable'
            r = requests.get(url=url)
            return render_template("showSecretariatTimetable.html", sec=r.json())
        else:
            return redirect('/private')
    except:
        return redirect('/private')
        

@app.route('/secretariats/<_id>/description', methods=['GET'])
def secretariat_desc(_id):
    global users_dict  
    try:
        if str(request.args['id']) in users_dict:
            send_log('backend: webpages, render secretariat description, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/description'
            r = requests.get(url=url)
            return render_template("showSecretariatDescription.html", sec=r.json())
        else:
            return redirect('/private')
    except:
        return redirect('/private')

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
    #try:
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
    #except:
        #return redirect('/private')

# CANTINA

@app.route('/canteen', methods=['GET'])
def canteen():
    global users_dict  
    try:
        if request.args['id'] in users_dict.keys():
            send_log('backend: webpages, render canteen form, GET')
            return render_template('canteenForm.html', key=request.args['id'] )
        else:
            return redirect('/private')
    except:
        return redirect('/private')


@app.route('/canteen/<day>', methods=['GET'])
def canteen_day(day):
    global users_dict  
    try:
        if request.args['id'] in users_dict.keys():
            send_log('backend: webpages, render canteen lunch and dinner, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/canteen/' + day + '/lunch'
            r = requests.get(url=url)
            lunch = r.json()
            url = 'http://127.0.0.1:' + port_api + '/api/canteen/' + day + '/dinner'
            r = requests.get(url=url)
            dinner = r.json()
            return render_template("showLunchDinner.html", list_lunch=lunch, list_dinner=dinner)
        else:
            return redirect('/private')
    except:
        return redirect('/private')

@app.route('/canteen/<day>/lunch', methods=['GET'])
def canteen_lunch(day):
    global users_dict  
    try:
        if request.args['id'] in users_dict.keys():
            send_log('backend: webpages, render canteen lunch, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/canteen/'+day+'/lunch'
            r = requests.get(url=url)
            data = r.json()
            return render_template("showLunch.html", list=data)
        else:
            return redirect('/private')
    except:
        return redirect('/private')

@app.route('/canteen/<day>/dinner', methods=['GET'])
def canteen_dinner(day):
    global users_dict  
    try:
        if request.args['id'] in users_dict.keys():
            send_log('backend: webpages, render canteen dinner, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/canteen/'+day+'/dinner'
            r = requests.get(url=url)
            data = r.json()
            return render_template("showDinner.html", list=data)
        else:
            return redirect('/private')
    except:
        return redirect('/private')
    #return jsonify(data)

#Rooms
@app.route('/rooms', methods=['GET'])
def rooms_menu():
    global users_dict  
    try:
        if request.args['id'] in users_dict.keys():
            send_log('backend: webpages, render rooms form, GET')        
            return render_template("roomsMenu.html", port_webpages=port_webpages, key=request.args['id'])
        else:
            return redirect('/private')
    except:
        return redirect('/private')

@app.route('/rooms/<_id>', methods=['GET'])
def room(_id):
    global users_dict
    try:
        if request.args['id'] in users_dict.keys():
            print("key ", request.args['id'])
            print("id room ", _id)
            send_log('backend: webpages, render room by id, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id
            r = requests.get(url=url)
            data = r.json()
            if 'error' in data.keys():
                return jsonify(data)
            else:
                print("render show room!!")
                return render_template("showRoom.html", room=data,  port_webpages=port_webpages, key=request.args['id'])
                #return jsonify(data)
        else:
            return redirect('/private')
    except:
        return redirect('/private')

    
        
@app.route('/rooms/<_id>/location', methods=['GET'])
def room_location(_id):
     global users_dict
     try:
         if request.args['id'] in users_dict.keys():
            send_log('backend: webpages, render room location, GET')

            url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id+'/location'
            r = requests.get(url=url)
            data = r.json()
            if 'error' in data.keys():
                return jsonify(data)
            else:
                return render_template("showRoomLocation.html", room=data,  port_webpages=port_webpages, key=request.args['id'])
         else:
             return redirect('/private')
     except:
         return redirect('/private')

@app.route('/rooms/<_id>/events', methods=['GET'])
def room_events(_id):
    global users_dict
    try:
        if request.args['id'] in users_dict.keys():
            send_log('backend: webpages, render room events, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id+'/events'
            r = requests.get(url=url)
            data = r.json()
            if 'error' in data.keys():
                return jsonify(data)
            else:
                return render_template("showRoomEvents.html", room=data, events=data['events'] ,port_webpages=port_webpages, key=request.args['id'])
        else:
            return redirect('/private')
    except:
        return redirect('/private')


@app.route('/rooms/<_id>/events/<day>', methods=['GET'])
def room_events_day(_id,day):
    global users_dict
    try:
        if request.args['id'] in users_dict.keys():
            send_log('backend: webpages, render room events by day, GET')
            url = 'http://127.0.0.1:' + port_api + '/api/room/'+_id+'/events/'+day
            r = requests.get(url=url)
            data = r.json()
            if 'error' in data.keys():
                return jsonify(data)
            else:
                return render_template("showRoomEvents.html", room=data, events=data['events'] ,port_webpages=port_webpages, key=request.args['id'])
        else:
            return redirect('/private')
    except:
        return redirect('/private')

def send_log(msg):
    url = 'http://127.0.0.1:'+port_log+'/addlog'
    date = datetime.datetime.now()
    requests.post(url=url, data={'log': str(date) + ' - ' + msg})
    data={'msg' : '200 - OK'}
    return data

if __name__ == '__main__':
    app.run(port=3998,debug=True)