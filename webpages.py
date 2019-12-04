from flask import Flask
from flask import render_template
from flask import jsonify
from flask import redirect
import requests
from flask import request
import auth
import datetime

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

@app.route('/', methods=['GET'])
def login():
    return render_template("Login.html", username=loginName)

@app.route('/private', methods=['GET'])
def private_page():
    if loginName == False:
        redPage = fenixLoginpage % (client_id, redirect_uri)
        return redirect(redPage)
    else:
        print(userToken)
        params = {'access_token': userToken}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params=params)

        if (resp.status_code == 200):
            r_info = resp.json()
            print(r_info)
            return render_template("privPage.html", username=loginName, name=r_info['name'], json=r_info)
        else:
            return "oops"

@app.route('/userAuth')
def userAuthenticated():
    #This page is accessed when the user is authenticated by the fenix login pagesetup

    #first we get the secret code retuner by the FENIX login
    code = request.args['code']
    print ("code "+request.args['code'])


    # we now retrieve a fenix access token
    payload = {'client_id': client_id, 'client_secret': clientSecret, 'redirect_uri' : redirect_uri, 'code' : code, 'grant_type': 'authorization_code'}
    response = requests.post(fenixacesstokenpage, params = payload)
    print (response.url)
    print (response.status_code)
    if(response.status_code == 200):
        #if we receive the token
        print ('getting user info')
        r_token = response.json()
        print(r_token)

        params = {'access_token': r_token['access_token']}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        r_info = resp.json()
        print( r_info)

        # we store it
        global loginName
        loginName = r_info['username']
        global userToken
        userToken = r_token['access_token']

        #now the user has done the login
        #return jsonify(r_info)
        #we show the returned infomration
        #but we could redirect the user to the private page
        return redirect('/services') #comment the return jsonify....
    else:
        return 'oops2'

@app.route('/services', methods=['GET'])
def initial_menu():
    auth.request_user_permission()
    add_log('Backend', 'Web Pages', 'GET mainPage.html')
    return render_template("mainPage.html")

@app.route('/redirect', methods=['GET'])
def get_code():
    global access_token
    global refresh_token
    global expires_in
    code = request.args.get('code')
    print(code)
    data = auth.request_access_token(code)
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    expires_in = data['expires_in']
    print(data)
    return jsonify(data)

# SECRETARIA

@app.route('/secretariats', methods=['GET'])
def secretariats_menu():
   if request.method=='GET':
        send_log('backend: webpages, render secretariats options, GET')
        return render_template("secretariatsMenu.html")

@app.route('/secretariats/all', methods=['GET'])
def all_secretariats():
    if request.method == 'GET':
        send_log('backend: webpages, render all secretariats, GET')
        url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'
        print(url)
        r = requests.get(url=url)
        return render_template("allSecretariats.html", list_secs=r.json())

@app.route('/secretariats/<_id>', methods=['GET'])
def secretariat(_id):
    if request.method == 'GET':
        send_log('backend: webpages, render secretariat by id, GET')
        url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id
        print(url)
        r = requests.get(url=url)
        return render_template("showSecretariat.html", sec_dict=r.json())

@app.route('/secretariats/<_id>/location', methods=['GET'])
def secretariat_local(_id):
    if request.method == 'GET':
        send_log('backend: webpages, render secretariat location, GET')
        url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/location'
        print(url)
        r = requests.get(url=url)
        print(r.json())
        return render_template("showSecretariatLocation.html", sec=r.json())

@app.route('/secretariats/<_id>/timetable', methods=['GET'])
def secretariat_timetable(_id):
    if request.method == 'GET':
        send_log('backend: webpages, render secretariat timetable, GET')
        url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/timetable'
        print(url)
        r = requests.get(url=url)
        print(r.json())
        return render_template("showSecretariatTimetable.html", sec=r.json())

@app.route('/secretariats/<_id>/description', methods=['GET'])
def secretariat_desc(_id):
    if request.method  == 'GET':
        send_log('backend: webpages, render secretariat description, GET')
        url = 'http://127.0.0.1:' + port_api + '/api/secretariats/'+_id+'/description'
        print(url)
        r = requests.get(url=url)
        print(r.json())
        return render_template("showSecretariatDescription.html", sec=r.json())

@app.route('/secretariats/create',methods=['GET'])
def create_sec_form():
    if request.method  == 'GET':
        send_log('backend: webpages, render add secretariat form, GET')
        return render_template("addSecretariatForm.html")

@app.route('/secretariats/addSecretariat', methods=['POST'])
def add_secretariat():
    
    if request.method == "POST":
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

# CANTINA

@app.route('/canteen', methods=['GET'])
def canteen():
    send_log('backend: webpages, render canteen form, GET')
    return render_template('canteenForm.html')


@app.route('/canteen/<day>', methods=['GET'])
def canteen_day(day):
    if request.method=='GET':
        send_log('backend: webpages, render canteen lunch and dinner, GET')
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
    if request.method=='GET':
        send_log('backend: webpages, render canteen lunch, GET')
        add_log('Backend', 'Web Pages', 'GET showLunch.html')
        url = 'http://127.0.0.1:' + port_api + '/api/canteen/'+day+'/lunch'
        print(url)
        r = requests.get(url=url)
        data = r.json()
        return render_template("showLunch.html", list=data)

@app.route('/canteen/<day>/dinner', methods=['GET'])
def canteen_dinner(day):
    if request.method=='GET':
        send_log('backend: webpages, render canteen dinner, GET')
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
    if request.method=='GET':
        send_log('backend: webpages, render rooms form, GET')        
        return render_template("roomsMenu.html", port_webpages=port_webpages)

@app.route('/rooms/<_id>', methods=['GET'])
def room(_id):
     if request.method=='GET':
        send_log('backend: webpages, render room by id, GET') 
       
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
     if request.method=='GET':
        send_log('backend: webpages, render room location, GET') 
       
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
     if request.method=='GET':
        send_log('backend: webpages, render room events, GET') 
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
     if request.method=='GET':
        send_log('backend: webpages, render room events by day, GET') 
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


def send_log(msg):
    url = 'http://127.0.0.1:'+port_log+'/addlog'
    date = datetime.datetime.now()
    requests.post(url=url, data={'log': str(date) + ' - ' + msg})

if __name__ == '__main__':
    app.run(port=3998)