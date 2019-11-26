from flask import Flask
from flask import render_template
from flask import jsonify
import requests
from flask import request

app = Flask(__name__)

port_sec = '4000'

@app.route('/', methods=['GET'])
def initial_menu():
    return render_template("mainPage.html")

@app.route('/secretariats', methods=['GET'])
def secretariats_menu():
    return render_template("secretariatsMenu.html")

@app.route('/secretariats/all', methods=['GET'])
def all_secretariats():
    url = 'http://127.0.0.1:' + port_sec + '/api/secretariats/'
    print(url)
    r = requests.get(url=url)
    return render_template("allSecretariats.html", list_secs=r.json())

@app.route('/secretariats/<_id>', methods=['GET'])
def secretariat(_id):
    url = 'http://127.0.0.1:' + port_sec + '/api/secretariats/'+_id
    print(url)
    r = requests.get(url=url)
    return render_template("showSecretariat.html", sec_dict=r.json())

@app.route('/secretariats/<_id>/location', methods=['GET'])
def secretariat_local(_id):
    url = 'http://127.0.0.1:' + port_sec + '/api/secretariats/'+_id+'/location'
    print(url)
    r = requests.get(url=url)
    print(r.json())
    return render_template("showSecretariatLocation.html", sec=r.json())

@app.route('/secretariats/<_id>/timetable', methods=['GET'])
def secretariat_timetable(_id):
    url = 'http://127.0.0.1:' + port_sec + '/api/secretariats/'+_id+'/timetable'
    print(url)
    r = requests.get(url=url)
    print(r.json())
    return render_template("showSecretariatTimetable.html", sec=r.json())

@app.route('/secretariats/<_id>/description', methods=['GET'])
def secretariat_desc(_id):
    url = 'http://127.0.0.1:' + port_sec + '/api/secretariats/'+_id+'/description'
    print(url)
    r = requests.get(url=url)
    print(r.json())
    return render_template("showSecretariatDescription.html", sec=r.json())

@app.route('/secretariats/create')
def create_sec_form():
    return render_template("addSecretariatForm.html")

'''@app.route('/secretariats/addSecretariat', methods=['POST'])
def add_secretariat():   
    if request.method == "POST":
        name = str(request.form['Name'])
        campus =str(request.form['Campus'])
        building=str(request.form['Building'])
        hours=str(request.form['Hours'])
        description=str(request.form['Description'])
        db.addSecretariats(name, building, campus, hours, description)
        count = len(db.listAllSecretariats())
    return render_template("mainPage.html", count=count)'''

if __name__ == '__main__':
    app.run(port=3998)