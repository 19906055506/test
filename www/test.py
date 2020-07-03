from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError, SchedulerAlreadyRunningError
from flask import Flask, request, Response, jsonify, abort, make_response, redirect, url_for
from www.log import log
import copy

app = Flask(__name__)
scheduler = BackgroundScheduler()


@app.route('/<username>', methods=['GET'])
def index(username):
    if username == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('guest', name = username))


@app.route('/admin')
def hello_admin():
    return 'hello admin'


@app.route('/guest/<name>')
def guest(name):
    return 'hello guest: {}'.format(name)

@app.route('/login/', methods=["post"])
def login():
    res = request.form
    return '123'


@app.errorhandler(404)
def handler_404_error(err):
    return err


app.run()
