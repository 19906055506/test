from suds.client import Client

# url = 'http://172.16.10.111:7888/ormrpc/services/EASLogin?wsdl'
url_login = 'http://127.0.0.1:56898/ormrpc/services/EASLogin?wsdl'
url = 'http://127.0.0.1:56898/ormrpc/services/WSImportFinanceFacade?wsdl'

headers = {'Content-Type': 'application/soap+xml;charset="UTF-8"'}
client_login = Client(url_login, headers=headers, faults=False, timeout=15)

res_login = client_login.service.login(userName='obz', password='123456', slnName='eas', dcName='CAR95', language='l2',
                                       dbType=1)

# res_login[1]['sessionId']
headers['SessionId'] = str(res_login[1]['sessionId'])
client = Client(url, headers=headers, faults=False, timeout=15)
print(res_login)

res = client.service.selectVoucher(
    '''<easparam><billNumber>0001</billNumber><dateFrom>2019-05-01</dateFrom><dateTo>2019-05-31</dateTo><companyNumber>005</companyNumber></easparam>''')
print(res)

res_login = client_login.service.logout('obz', '123456', 'CAR95', 'l2')
