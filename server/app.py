# -*- coding: utf-8 -*-
from flask import Flask,session,render_template
from lib.RedisSesison import RedisSessionInterface

app = Flask(__name__)
app.config.from_pyfile("settings.py")
app.session_interface = RedisSessionInterface()

import server
server.setup(app)

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def test():
    return render_template('login.html')

@app.route('/name/<name>')
def set_name(name):
    session['name'] = name
    return 'hi {0}'.format(name)

def runserver(host=None,port=None):
    host = host or app.config['SERVER_HOST']
    port = port or app.config['SERVER_PORT']
    app.run(host,port)
    
