from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
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

@app.route('/api/canteen/week')
def week_info():
    return render_template("weeklyCanteenInfo.html")

@app.route('/api/canteen/day')
def choose_day():
    return render_template("chooseDayCanteen.html")

if __name__ == '__main__':
    app.run()