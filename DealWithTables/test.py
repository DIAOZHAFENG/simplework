# -*- coding: utf-8 -*-
import time
# from db_inconnect import MSSQL
from servers import get_info

get_ping_tables = '''
    SELECT Name FROM SysObjects Where XType='U' AND Name LIKE 'UserPingListTable_%' ORDER BY Name
    '''

mark_test_ip = '''
    update ip set Name = '{name}' where IpAddress = '{ip}'
    '''

get_name = '''
    select Name from ip where IpAddress = '{ip}'
    '''

ips = '''115.159.158.220;101.226.247.79;183.129.141.83;116.211.92.26;118.123.240.10;113.106.98.174;125.76.242.76;119.188.39.132;125.46.49.74;111.206.162.204;123.56.177.90;139.129.193.189;120.27.142.56;60.191.12.142;222.73.235.79;115.238.100.105;123.206.26.215'''

if __name__ == '__main__':
    # i = 0
    # now = time.time()
    # db = MSSQL()
    # while i < 1000:
    #     for row in db.query('select * from ip where name = \'阿里北京\''):
    #         print(row[1].encode('latin1').decode('gbk'))
    #     i += 1
    # print time.time() - now
    req = '''/SubmitUserPingListInterface/?command=submit&userid=389506263&username=%3F%3F%3F&ipaddress=101.226.247.79&pings=1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000;1000'''
    info = get_info(req)
    print info
