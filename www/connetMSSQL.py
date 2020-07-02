import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    import pymssql

import param as param
from www.log import log


class MSSQL:
    def __init__(self, host=param.msdbhost, user=param.msdbuser, pwd=param.msdbpassword, db=param.msdbname):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db,
                                    charset="UTF-8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        resList = []
        try:
            cur.execute(sql)
            resList = cur.fetchall()
            self.conn.commit()
        except pymssql.OperationalError as e:
            log.warning('没有返回信息: [{sql}] {e}'.format(sql=sql[:100], e=e))

        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecUpdate(self, sql):
        cur = self.__GetConnect()
        try:
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
            return True
        except pymssql.OperationalError as e:
            pass
        except Exception as e:
            log.error('{} {} [err: {}]'.format(Exception, e, sql[:100]))

        self.conn.rollback()
        return False

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        r = cur.fetchone()
        self.conn.commit()
        self.conn.close()

    def ExecNonQueryInsert(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        returnId = int(cur.lastrowid)
        # print(returnId)
        self.conn.commit()
        self.conn.close()
        return returnId

    def ExecProc(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        # result = cur.fetchall()
        # print(result)
        self.conn.close()

# ms = MSSQL(host=server, user=user, pwd=password, db=dbname)
# r = ms.ExecQuery('select fid from t_org_company')
# print(r)
