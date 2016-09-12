#--*--coding: utf-8--*--
#!/usr/bin/python2

import sqlite3
import random
import hashlib
import base64
import os
from bottle import route, request, post, run, template, static_file, response, redirect

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

def secret_key():
	secret = '2345fgjsdrk/+63gdjsj'
	#выбираем из строки secret 5 символов
	r = random.sample(secret, 5)

	#Преобразуем список из 5-ти символов в строку
	string = ''.join(r)
	sh=string + 'login'
	secret_key = hashlib.sha1(sh).hexdigest()
	return secret_key

def set_session_key(sk, login):
    db = sqlite3.connect("site.db")
    cur = db.cursor()
    cur.execute("update users set session_id=? where login =?", (sk, login,))
    db.commit()
    db.close()

def get_session_key(login):
    db = sqlite3.connect("site.db")
    cur = db.cursor()
    cur.execute("select session_id from users where login =?", (login,))
    sid = cur.fetchone()
    db.close()
    return sid[0]

################## not used #############################################################
#def get_cookie(user):
#	db = sqlite3.connect("site.db")
#	cur = db.cursor()
#	cur.execute("select count(session_id) from users where session_id=?", (user,))
#	sid = cur.fetchone()
#	if sid == 1:
#		cur.execute("select login from users where session_id=?", (user,))
#		cur_user = cur.fetchone()
#		return cur_user
#	else:
#		return sid
##########################################################################################

def delete_cookie(sid):
    db = sqlite3.connect("site.db")
    cur = db.cursor()
    cur.execute("update users set session_id=? where session_id =?", (None, sid,))
    db.commit()

def pwd_gen(pwd):
    password = hashlib.sha1((pwd).encode('utf-8')).digest()
    hash_pwd = base64.b64encode(password)
    return str(hash_pwd)

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
    hashed_pwd = pwd_gen(pwd)
    write_To_DB(login, hashed_pwd, email)
    return "User succesfully created! <a href='/login'>Log In</a>"

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
    hashed_pwd = pwd_gen(pwd)
    isUser = check_login(login)
    if isUser:
        user_pwd = read_pwd(login)
        if hashed_pwd == user_pwd:
            sk = secret_key()
            set_session_key(sk, login)
            cookie = get_session_key(login)
            response.set_cookie("user", str(cookie), path='/')
            redirect('/lk')
        else:
            return "Bad password!"
    else:
        return "Bad Login!"

@route('/restrict')
def restrict():
    return "You are not authorize. Please <a href='/login'>login</a> or <a href='/reg'>sign up</a>"

@route('/lk')
def lk():
    user = request.get_cookie("user")
    if user:
        return template("views/lk.tpl")
    else:
        redirect('/restrict')

@route('/logout')
def logout():
    sid = request.get_cookie("user")
    delete_cookie(sid)
    response.delete_cookie('user') 
    return "You logged out <a href='/'>Main page</a>"

run(reloader=True, debug=True)
