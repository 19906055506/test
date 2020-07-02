from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError, SchedulerAlreadyRunningError
from flask import Flask

app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route('/')
def index():
    return '123'

app.run()