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

r = []
for root, dirs, files in os.walk('C:\\Users\\admin\\Desktop\\汽车'):
    r = files

# for i in r:
#     print(i)
#     s = re.search(r'([\u2E80-\u9FFF]+)_(\S+)_([\u2E80-\u9FFF]+)', i)
#     print(s.group(2))
#     break

ms = MSSQL()
# sql = "select fid, fnumber, fcode, fname_l2 from t_org_company where fnumber in ('003', '004')"
# sql = "dbcc showcontig(t_org_baseUnit)"
sql = "exec dbo.proce_Update_FVIN 'LHGRU184XH8008828', '0708002'"
# sql = "insert into ITGReport_TargetCalcul(idx, proceName) select 100 ,'测试'"
# sql = "select top 100 fid, FARAmount from T_ATS_RepairSettlemententry where FID = '///a0wK4R96QG39O+Xyd7z8NAp8='"
r = ms.ExecQuery(sql)
# r = chardet.detect(r)

print(r)