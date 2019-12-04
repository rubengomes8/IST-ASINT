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
port_log='4003'

@app.route('/api/canteen', methods=['GET'])
def canteen_menu():
    if request.method == "GET": 
        send_log('microservice: canteen, get canteen, GET')       
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
    if request.method == "GET": 
        send_log('microservice: canteen, get canteen by day, GET')
        global cache
        print(cache)
        if day in cache:
            print("Hit")
            return jsonify(cache[day])
        else:
            print("Miss")
            url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen'
            r = requests.get(url=url)
            _day,_month,_year = process_day(day)
            print(_day, "   ", _month, "   ", _year)
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
    if request.method == "GET": 
        send_log('microservice: canteen, get canteen lunch by day, GET')
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
            print("day ", day)
            url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen'
        
            _day,_month,_year = process_day(day)
            print(_day, "   ", _month, "   ", _year)
            r = requests.get(url=url)
            data = r.json()
            fill_cache(data)
            print(_day, "   ", _month, "   ", _year)
            for item in data:
                print("item: ", item)
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
    if request.method == "GET": 
        send_log('microservice: canteen, get canteen dinner by day, GET')
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
            print(day)
            _day,_month,_year = process_day(day)
            print(_day, "   ", _month, "   ", _year)
            r = requests.get(url=url)
            data = r.json()
            fill_cache(data)
            #print(cache)
            #print(data)
            for item in data:
                #print("item: ", item)
                if item['day'] == _day+'/'+_month+'/'+_year:
                    #print(_day+'/'+_month+'/'+_year)
                    meal = item['meal']
                    for _meal in meal:
                        if _meal['type'] == 'Jantar':
                            return jsonify(_meal['info'])
            error = {}
            error['error'] = 404
            return jsonify(error)

@app.route('/api/canteen/cache', methods=['GET'])
def print_cache():
    if request.method == "GET": 
        send_log('microservice: canteen, get canteen  cache, GET')
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

def process_day(_day):
    #print(_day)
    day=_day[0:2]
    month=_day[2:4]
    #print(_day[0])
    #print(_day[2])
    if _day[0] == '0':
        day = _day[1]
    if _day[2] == '0':
        month = _day[3]
    #print(day+month+_day[4:8])
    return day,month,_day[4:8]


def send_log(msg):
    url = 'http://127.0.0.1:'+port_log+'/addlog'
    date = datetime.datetime.now()
    requests.post(url=url, data={'log': str(date) + ' - ' + msg})

if __name__ == '__main__':
    app.run(port=4001)
