from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

app = Flask(__name__)




@app.route('/api/secretariats/')
def secretariats():
    #url=127.0.0.1:4000 e fazer pedido

if __name__ == '__main__':
    app.run(port=3999)
