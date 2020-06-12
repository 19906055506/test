from www.connetMSSQL import MSSQL
import csv
from selenium import webdriver
import time
from lxml import etree
import os
import re
from www.log import log
import yaml
import chardet

# for i in r:
#     print(i)
#     s = re.search(r'([\u2E80-\u9FFF]+)_(\S+)_([\u2E80-\u9FFF]+)', i)
#     print(s.group(2))
#     break

ms = MSSQL()


# sql = "select fid, fnumber, fcode, fname_l2 from t_org_company where fnumber in ('003', '004')"
# sql = "dbcc showcontig(t_org_baseUnit)"
# sql = "exec dbo.proce_Update_FVIN 'LHGRU184XH8008828', '0708002'"
# sql = "insert into ITGReport_TargetCalcul(idx, proceName) select 100 ,'测试'"
# sql = "select top 10 * from ITGReport_TargetCalcul where idx = 100"
# sql = "select top 100 fid, FARAmount from T_ATS_RepairSettlemententry where FID = '///a0wK4R96QG39O+Xyd7z8NAp8='"
# sql = "exec proce_test"
# sql = "DBCC DBREINDEX('T_ATS_AutoSaleIssue')"
# r = ms.ExecQuery(sql)
# print(r)


def domain():
    with open('../test2.txt', 'r', encoding='utf-8') as f:
        r = f.readlines()
    ls = {}
    name = ''
    tig = ''
    num = 0

    pattern1 = re.compile('DBCC SHOWCONTIG 正在扫描')
    pattern2 = re.compile('- 平均页密度')
    patternName = re.compile('(?:表\: \')(.*)\'')
    patternTig = re.compile('- 扫描密度.* (\d*.\d*)% \[')

    with open('../test3.txt', 'w', encoding='utf-8') as f:
        f.write('')
    with open('../test3.txt', 'a', encoding='utf-8') as f:
        s = ''
        for i in r:
            n1 = re.match(pattern1, i)
            if n1:
                s = name = tig = ''
                num = 0
            s += i
            num += 1

            a = re.match(patternName, i)
            if a:
                name = a.group(1)

            b = re.match(patternTig, i)
            if b:
                tig = float(b.group(1))

            n2 = re.match(pattern2, i)
            if n2:
                if tig >= 0:
                    print([name, tig], '\n', s)
                    # f.write('{}, {}, {}'.format(name, tig, num))
                    f.write('insert into temp_sjl(fnumber) values(\'{name}\');'.format(name=name))
                    f.write('\n')


domain()
