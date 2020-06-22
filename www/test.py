import os, sys

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

import csv, time, re, yaml, chardet
from selenium import webdriver
from lxml import etree
from www.log import log
from www.connetMSSQL import MSSQL
import www.util as util

ms = MSSQL()
util.clearLog()


# ls = ['T_BAS_IntermitNO', 'T_CSL_TempletDispense']
# for tableName in ls:
#     begin = time.time()
#     sql = 'update statistics {} with fullscan'.format(tableName)
#     log.info('begin: {}'.format(tableName))
#     ms.ExecQuery(sql)
#     time1 = float(time.time() - begin)
#     log.info('end: {}, time: {:.2f} s'.format(sql, time1))
#
#     begin = time.time()
#     sql = 'DBCC DBREINDEX({})'.format(tableName)
#     ms.ExecQuery(sql)
#     time2 = float(time.time() - begin)
#     log.info('end: {}, time: {:.2f} s\n'.format(sql, time2))
#
#     sql = 'update temp_sjl set cost1 = {:.2f}, cost2 = {:.2f} where fnumber = \'{}\''.format(time1, time2, tableName)
#     ms.ExecUpdate(sql)


def domain():
    with open('../showcontig.txt', 'r', encoding='utf-8') as f:
        r = f.readlines()
    ls = {}
    name = ''
    tig = ''
    num = 0

    patternBegin = re.compile('DBCC SHOWCONTIG 正在扫描')
    patternEnd = re.compile('- 平均页密度')
    patternName = re.compile('(?:表\: \')(.*)\'')
    patternPage = re.compile('- 扫描页数(?:.*): (\d*)')
    patternTig = re.compile('- 扫描密度.* (\d*.\d*)% \[')

    with open('../test3.txt', 'w', encoding='utf-8') as f:
        f.write('')
    with open('../test3.txt', 'a', encoding='utf-8') as f:
        s = ''
        for i in r:
            begin = re.match(patternBegin, i)
            if begin:
                s = name = tig = ''
                num = page = 0
            s += i
            num += 1

            a = re.match(patternName, i)
            if a:
                name = a.group(1)

            p = re.match(patternPage, i)
            if p:
                page = p.group(1)

            b = re.match(patternTig, i)
            if b:
                tig = float(b.group(1))

            end = re.match(patternEnd, i)
            if end:
                if tig >= 0:
                    print([name, tig, page])
                    f.write('{} {} {}'.format(name, tig, page))
                    # f.write('insert into temp_sjl(fnumber, score) values(\'{name}\', {tig});'.format(name=name, tig=tig))
                    f.write('\n')


domain()
