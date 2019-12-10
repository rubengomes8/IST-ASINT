from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import databases.logDB as logdb

app = Flask(__name__)
db = logdb.logDB("logs")


@app.route('/addlog', methods=['POST'])
def add_log():
    if request.method == "POST":
        log = str(request.form['log'])       
        db.addLog(log)
        data={'msg': '200 - OK'}
        return data
    

@app.route('/api/logs/getlogs', methods=['GET'])
def get_logs():
    if request.method == "GET":
        return jsonify(db.showLogs())

if __name__ == '__main__':
    app.run(port=4003,debug=True)