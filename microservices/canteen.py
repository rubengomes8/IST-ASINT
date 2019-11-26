from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import requests
'''
endpoints:
- "api/canteen/" apresenta infromação para a semana
- "api/canteen/day" escolher o dia da semana
- "api/canteen/<ddmmyyyy>" apresenta informação para um dia almoço e jantar
- "api/canteen/<ddmmyyyy>/lunch"  apresenta informação para o almoço de um dia
- "api/canteen/<ddmmyyyy>/dinner" apresenta informação para o jantar de um dia 
'''

app = Flask(__name__)

@app.route('/api/canteen', methods=['GET'])
def canteen_menu():
    url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen'
    r = requests.get(url=url)
    data = r.json()
    return jsonify(data)

@app.route('/api/canteen/<day>', methods=['GET'])
def canteen_day(day): # day must be in format ddmmyyyy
    url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen'
    _day = day[0:2]
    _month = day[2:4]
    _year = day[4:8]
    r = requests.get(url=url)
    data = r.json()
    for item in data:
        if item['day'] == _day+'/'+_month+'/'+_year:
            print(_day+'/'+_month+'/'+_year)
            return jsonify(item)
    error = {}
    error['error'] = 404
    return jsonify(error)

@app.route('/api/canteen/<day>/lunch', methods=['GET'])
def canteen_day_lunch(day): # day must be in format ddmmyyyy
    url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen'
    _day = day[0:2]
    _month = day[2:4]
    _year = day[4:8]
    r = requests.get(url=url)
    data = r.json()
    for item in data:
        if item['day'] == _day+'/'+_month+'/'+_year:
            print(_day+'/'+_month+'/'+_year)
            meal = item['meal']
            for _meal in meal:
                if _meal['type'] == 'Almoço':
                    return jsonify(_meal['info'])
    error = {}
    error['error'] = 404
    return jsonify(error)

@app.route('/api/canteen/<day>/dinner', methods=['GET'])
def canteen_day_dinner(day): # day must be in format ddmmyyyy
    url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen'
    _day = day[0:2]
    _month = day[2:4]
    _year = day[4:8]
    r = requests.get(url=url)
    data = r.json()
    for item in data:
        if item['day'] == _day+'/'+_month+'/'+_year:
            print(_day+'/'+_month+'/'+_year)
            meal = item['meal']
            for _meal in meal:
                if _meal['type'] == 'Jantar':
                    return jsonify(_meal['info'])
    error = {}
    error['error'] = 404
    return jsonify(error)

if __name__ == '__main__':
    app.run(port=4001)