import os
import json
from time import time

from bottle import run, get, post, template, static_file
from bottle import response, request, redirect, error
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

COOKIE_ID = 'omm-account'
COOKIE_SECRET = '49fz0348lQk5q110hRTt2An0'
COOKIE_EXPIRE = (3600 * 24 * 10)   # 10 Days

allowed_static = ('.css', '.js', '.png')

connections = set()
chart_data = dict()
users_data = json.load(open("config/users.json")).get("users")


# Cookies

def set_cookie(username):
    response.set_cookie(
        'omm-account',
        username,
        secret=COOKIE_SECRET,
        expires=time() + COOKIE_EXPIRE
    )


def get_cookie():
    return request.get_cookie(COOKIE_ID, secret=COOKIE_SECRET)


def clear_cookie():
    response.set_cookie(
        COOKIE_ID,
        '',
        secret=COOKIE_SECRET,
        expires=time() - COOKIE_EXPIRE
    )


# Methods

def broadcast(data):
    for conn in connections:
        conn.send(data)


def update_chart(data):
    print "Event data:{}".format(data)


def user_login(user, password):
    return str(users_data.get(user, dict()).get("password")) == password


def user_image(user):
    return str(users_data.get(user, dict()).get("image"))


# Routes

@get('/')
def index():
    user = {"name": get_cookie(), "img": user_image(get_cookie())}
    return template('www/html/index', user=user)


@get('/<path:path>')
def static(path):
    if os.path.splitext(path)[1] in allowed_static:
        return static_file(path, root='www')


@get('/login')
def login():
    return template('www/html/login') if not get_cookie() else redirect("/")


@post('/login')
def login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    if user_login(username, password):
        set_cookie(username)
        redirect("/")
    else:
        return {"error": "Bad login"}


@post('/logout')
def logout():
    clear_cookie()
    redirect("/")


@post('/update')
def update():
    value = request.POST.get("value")
    username = get_cookie()
    if value and username:
        chart_data.update({username: value})
        broadcast(json.dumps(chart_data))


@error(404)
def error404(error):
    return 'Nothing here, sorry'


@get('/socket', apply=[websocket])
def router(sock):
    connections.add(sock)
    sock.send(json.dumps(chart_data))
    while True:
        data = sock.receive()
        if data is not None:
            broadcast(data)
        else:
            break
    connections.remove(sock)

# Main

run(host='0.0.0.0', port=8080, server=GeventWebSocketServer)
