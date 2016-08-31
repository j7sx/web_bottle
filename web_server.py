#--*--coding: utf-8--*--
#!/usr/bin/python2

import sqlite3
from bottle import route, request, post, run, template, static_file, response

def write_To_DB(login, pwd, email):
    db = sqlite3.connect("site.db")
    cur = db.cursor()
    cur.execute("insert into users(login, password, email) values(?, ?, ?)", (login,pwd, email,))
    db.commit()
    db.close()

def check_login(login):
    db = sqlite3.connect("site.db")
    cur = db.cursor()
    cur.execute("select count(login) from users where login=?", (login,))
    user = cur.fetchone()
    db.close()
    return user[0]

def read_pwd(login):
    db = sqlite3.connect("site.db")
    cur = db.cursor()
    cur.execute("select password from users where login=?", (login,))
    result = cur.fetchone()
    db.close()
    return result[0]

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file('style.css', root='static')

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

@route('/login')
def login():
    return """
        <form action="/login" method="post">
        Login: <input type="text" name="login"/>
        Password: <input type="password" name="pwd"/>
        <input type="submit" value="enter"/> """

@post('/login')
def do_login():
    login = request.forms.get("login")
    pwd = request.forms.get("pwd")
    isUser = check_login(login)
    if isUser:
        user_pwd = read_pwd(login)
        if pwd == user_pwd:
            response.set_cookie("account", login, secret='some-secret-key')
            return template("<p>Welcome {{name}}! You are now logged in.</p>", name=login)
        else:
            return "Bad password!"
    else:
        return "Bad Login!"

run(reloader=True, debug=True)
