import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    import pymssql

import param as param
import pymysql
from www.log import log
from DBUtils.PooledDB import PooledDB, SharedDBConnection


class MSSQLPool:
    def __init__(self):
        self.pool = PooledDB(
            creator=pymssql,  # 使用链接数据库的模块
            maxconnections=2,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=1,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=1,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=2,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host=param.msdbhost,
            port=param.msdbport,
            user=param.msdbuser,
            password=param.msdbpassword,
            database=param.msdbname,
            charset='utf8'
        )

    def __GetConnect(self):
        self.conn = self.pool.connection()
        cursor = self.conn.cursor()
        if not cursor:
            raise (NameError, '数据连接失败')
        else:
            return cursor

    def select(self, sql):
        cursor = self.__GetConnect()
        result = []
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except BaseException as e:
            log.warning(e)
        finally:
            self.conn.close()
        return result


class MYSQLPool:
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=2,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=1,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=1,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=2,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='finedb',
            charset='utf8'
        )

    def __GetConnect(self):
        self.conn = self.pool.connection()
        cursor = self.conn.cursor()
        if not cursor:
            raise (NameError, '数据连接失败')
        else:
            return cursor

    def select(self, sql):
        cursor = self.__GetConnect()
        result = []
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except BaseException as e:
            log.warning(e)
        finally:
            self.conn.close()
        return result


sqlhelp = MSSQLPool()
a = sqlhelp.select('select fid, fnumber from t_org_company where fnumber = 1')
print(a)

mysqlPool = MYSQLPool()
a = mysqlPool.select('SELECT id FROM `fine_user`')
print(a)
