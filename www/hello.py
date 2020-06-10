# monkey.patch_all()

import time, pymongo, random, os
import param as param
# from gevent.queue import Queue
from multiprocessing import Queue

client = pymongo.MongoClient(host=param.dbip, port=param.dbport)
db = client[param.dbName]

# baseUrl = 'http://httpbin.org/get'
# baseUrl = 'https://myip.ipip.net/'

queue = Queue()
baseUrl = 'http://www.boohee.com/food/'
headers = {
    'use-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}


def write(queue):
    print('Process to write ({})'.format(os.getpid()))
    for value in ['A', 'B', 'C']:
        print('Put {} to queue...'.format(value))
        queue.put(value)
        time.sleep(random.random() * 3)


def read(queue):
    print('Process to read ({})'.format(os.getpid()))
    while True:
        value = queue.get(True)
        print('Get {} from queue'.format(value))


# if __name__ == '__main__':
#     queue = Queue()
#     pw = Process(target=write, args=(queue,))
#     pr = Process(target=read, args=(queue,))
#
#     pw.start()
#     pr.start()
#
#     pw.join()
#     pr.terminate()


baseUrl = 'http://chromedriver.python-class-fos.svc:4444/wd/hub", chrome_options.to_capabilities()'