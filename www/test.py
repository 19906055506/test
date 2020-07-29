import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    import pymssql
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError, SchedulerAlreadyRunningError
from flask import Flask, request, Response, jsonify, abort, make_response, redirect, url_for, flash
from www.log import log
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import copy, pymysql, functools, sys, time, random
from www.util import log_excute_time

pymysql.install_as_MySQLdb()

app = Flask(__name__)
scheduler = BackgroundScheduler()
Base = declarative_base()


@app.route('/login', methods=['get', 'post'])
def index(username):
    flash('abc')
    return '123'


Base = declarative_base()


# app.run()


class Count:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print('num of calls is: {}'.format(self.num_calls))
        return self.func(*args, **kwargs)


@log_excute_time
def test():
    a = random.random()
    time.sleep(a)


test()
