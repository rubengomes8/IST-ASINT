from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import requests
'''
endpoints:
- "api/canteen" apresenta menu de opções do microserviço cantina
- "api/canteen/week" apresenta infromação para a semana
- "api/canteen/day" escolher o dia da semana
- "api/canteen/<ddmmyyyy>" apresenta informação para um dia almoço e jantar
- "api/canteen/<ddmmyyyy>/lunch"  apresenta informação para o almoço de um dia
- "api/canteen/<ddmmyyyy>/dinner" apresenta informação para o jantar de um dia 
'''

app = Flask(__name__)

@app.route('/api/canteen')
def canteen_menu():
    return render_template("canteenMenu.html")

@app.route('/api/canteen/week', methods=['GET'])
def week_info():
    if request.method == "GET":
        url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen/'
        r = requests.get(url=url)
        data = r.json()
        print(data)
        days = []
        _meals = {}
        for day in data:
            days.append(day['day'])
            for meals in day['meal']['info']:
                type1 = day['meal']['type']
                for meal in meals:
                    meals[type1] = [meal['type'], meal['name']]

        print(days)
        print(_meals)
        
    return render_template("weeklyCanteenInfo.html")

@app.route('/api/canteen/day')
def choose_day():
    return render_template("chooseDayCanteen.html")

if __name__ == '__main__':
    app.run()