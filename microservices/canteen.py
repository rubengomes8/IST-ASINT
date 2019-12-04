from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import requests
import datetime

'''
endpoints:
- "api/canteen/" apresenta infromação para a semana
- "api/canteen/day" escolher o dia da semana
- "api/canteen/<ddmmyyyy>" apresenta informação para um dia almoço e jantar
- "api/canteen/<ddmmyyyy>/lunch"  apresenta informação para o almoço de um dia
- "api/canteen/<ddmmyyyy>/dinner" apresenta informação para o jantar de um dia 
'''
app = Flask(__name__)
cache = {}  # key: day value: json food
log_path = './log.txt'

@app.route('/api/canteen', methods=['GET'])
def canteen_menu():
    add_log('Microservices', 'canteen', 'GET ....')
    global cache
    dt = datetime.datetime.today()
    date = str(dt.day) + str(dt.month) + str(dt.year)
    # print(date)
    if date in cache:
        print("Hit")
        list = []
        for item in cache.values():
            list.append(item)
        return jsonify(list)
    else:
        print("Miss")
        url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen'
        r = requests.get(url=url)
        data = r.json()
        fill_cache(data)
        return jsonify(data)


@app.route('/api/canteen/<day>', methods=['GET'])
def canteen_day(day): # day must be in format ddmmyyyy
    add_log('Microservices', 'canteen', 'GET ....')
    global cache
    print(cache)
    if day in cache:
        print("Hit")
        return jsonify(cache[day])
    else:
        print("Miss")
        url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen'
        r = requests.get(url=url)
        if day[0] == 0:
            _day = day[1]
        else:
            _day = day[0:2]
        if day[2] == 0:
            _month = day[3]
        else:
            _month = day[2:4]
        _year = day[4:8]
        data = r.json()
        fill_cache(data)
        for item in data:
            if item['day'] == _day+'/'+_month+'/'+_year:
                print(_day+'/'+_month+'/'+_year)
                return jsonify(item)
        error = {}
        error['error'] = 404
        return jsonify(error)

@app.route('/api/canteen/<day>/lunch', methods=['GET'])
def canteen_day_lunch(day): # day must be in format ddmmyyyy
    add_log('Microservices', 'canteen', 'GET ....')
    global cache
    print(cache)
    if day in cache:
        print("Hit")
        daily_info = cache[day]
        meal = daily_info['meal']
        for _meal in meal:
            if _meal['type'] == 'Almoço':
                return jsonify(_meal['info'])
    else:
        print("Miss")
        url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen'
        if day[0] == 0:
            _day = day[1]
        else:
            _day = day[0:2]
        if day[2] == 0:
            _month = day[3]
        else:
            _month = day[2:4]
        _year = day[4:8]
        r = requests.get(url=url)
        data = r.json()
        fill_cache(data)
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
    add_log('Microservices', 'canteen', 'GET ....')
    global cache
    print(cache)
    if day in cache:
        print("Hit")
        daily_info = cache[day]
        meal = daily_info['meal']
        for _meal in meal:
            if _meal['type'] == 'Jantar':
                return jsonify(_meal['info'])
    else:
        print("Miss")
        url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen'
        if day[0] == 0:
            _day = day[1]
        else:
            _day = day[0:2]
        if day[2] == 0:
            _month = day[3]
        else:
            _month = day[2:4]
        _year = day[4:8]
        r = requests.get(url=url)
        data = r.json()
        fill_cache(data)
        print(cache)
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

@app.route('/api/canteen/cache', methods=['GET'])
def print_cache():
    add_log('Microservices', 'canteen', 'GET ....')
    global cache
    #print(cache)
    return jsonify(cache)

def fill_cache(data):
    global cache
    cache = {}
    for item in data:
        key = process_date(item['day'])
        print(key)
        cache[key] = item

def process_date(date):
    date_ = date.split('/')
    string = ''
    for item in date_:
        string = string + item
    return string

def add_log(type = 'empty', module = 'empty', info = 'empty'):
    global log_path
    f = open(log_path, 'a')
    f.write('Type: ' + type + ' Module: ' + module + ' Info: ' + info + '\n')
    f.close()

if __name__ == '__main__':
    app.run(port=4001)
