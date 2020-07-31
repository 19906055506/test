from suds.client import Client

# url = 'http://172.16.10.111:7888/ormrpc/services/EASLogin?wsdl'
url_login = 'http://127.0.0.1:56898/ormrpc/services/EASLogin?wsdl'
url = 'http://127.0.0.1:56898/ormrpc/services/WSImportFinanceFacade?wsdl'

headers = {'Content-Type': 'application/soap+xml;charset="UTF-8"'}
client_login = Client(url_login, headers=headers, faults=False, timeout=15)

res_login = client_login.service.login(userName='obz', password='123456', slnName='eas', dcName='CAR95', language='l2',
                                       dbType=1)

headers['SessionId'] = str(res_login[1]['sessionId'])
client = Client(url, headers=headers, faults=False, timeout=15)

with open('../凭证.xml', 'r', encoding='utf-8') as f:
    r = f.read()

res = client.service.importVoucherInfo(
    '<xmlData>{}</xmlData><isVerify>0</isVerify><isImpCashflow>0</isImpCashflow>'.format(r))
print(res)

res_login = client_login.service.logout('obz', '123456', 'CAR95', 'l2')
