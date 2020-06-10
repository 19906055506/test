import logging, logging.config, yaml, os


# def log():
#     with open('logging.yaml', 'rt', encoding='utf-8') as f:
#         conf = yaml.safe_load(f.read())
#
#     logging.config.dictConfig(conf)
#     return logging.getLogger()

class Logger():
    def __init__(self):
        pass

    def create_Logger(self):
        with open('./logging.yaml', 'rt', encoding='utf-8') as f:
            conf = yaml.safe_load(f.read())
        logging.config.dictConfig(conf)
        return logging.getLogger()


log = Logger().create_Logger()

# class Logger():
#
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def create_logger():
#         logger = logging.getLogger(__name__)
#
#         logging.basicConfig(
#             level=logging.INFO,
#             format='%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s',
#             datefmt='%Y-%m-%d %H:%M:%S',
#             filename='all.log',
#             filemode='a',
#         )

# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)

# return logging
