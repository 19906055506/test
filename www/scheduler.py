import time, pymongo
from www.log import log
import param as param
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError, SchedulerAlreadyRunningError
from flask import Flask

client = pymongo.MongoClient(host=param.dbip, port=param.dbport)
db = client[param.dbName]

# baseUrl = 'http://httpbin.org/get'
# baseUrl = 'https://myip.ipip.net/'

app = Flask(__name__)
scheduler = BackgroundScheduler()


# @scheduler.scheduled_job('interval', seconds=3, id='job_1')
def job():
    # print(time.localtime())
    with open('../test.txt', 'a', encoding='utf-8', newline='') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n')


@app.route('/')
def index():
    try:
        jobid = 'job_1'
        j = scheduler.get_job(jobid)
        if j == None:
            scheduler.add_job(job, 'interval', seconds=3, id=jobid)
        scheduler.start()
        log.info('Scheduler start success')
        return 'Scheduler start success'
    except SchedulerAlreadyRunningError as e:
        log.warning(str(e))
        return str(e)


@app.route('/remove_all_job')
def removejob():
    try:
        r = scheduler.get_jobs()
        ls = []
        for i in r:
            ls.append(i.id)
        scheduler.remove_all_jobs()
        log.info('scheduler job remove all : {}'.format(str(ls)))
        return 'scheduler job remove all : {}'.format(str(ls))
    except SchedulerNotRunningError as e:
        log.warning(e)
        return str(e)


app.run()
