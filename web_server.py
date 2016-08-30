#--*--coding: utf-8--*--
#!/usr/bin/python2

import sqlite3
from bottle import route, request, post, run, template, static_file

def write_To_DB(login, pwd, email):
    db = sqlite3.connect("site.db")
    cur = db.cursor()
    cur.execute("insert into users(login, password, email) values(?, ?, ?)", (login,pwd, email,))
    db.commit()
    db.close()

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file('style.css', root='static')
    st

@route('/')
def index():
    return template('views/index.tpl')

@route('/reg')
def reg():
    return """
        <form action='/reg' method='post'>
        Login:    <input type='text' name='login'/>
        Password: <input type='password' name='pwd'/>
        Email:    <input type='text' name='email'/>
        <input type='submit' value='reg'>
        """

@post('/reg')
def do_reg():
    login = request.forms.get('login')
    pwd = request.forms.get('pwd')
    email = request.forms.get('email')
    write_To_DB(login, pwd, email)
    return "user was be added"



run(reloader=True, debug=True)