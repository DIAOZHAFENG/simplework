# -*- coding: utf8 -*-

import web
from data_process import MSSQL

ip_address = open('ip_address').read()

insert_sql = '''
INSERT INTO UserPingList (userId, userName, ipAddress, clientIpAddress, createTime, {pings},
area, city, isp, valid_ping_count, avg_ping, stdev_ping)
VALUES ({userId}, '{userName}', '{ipAddress}', '{clientIpAddress}', now(), {pings},
'{area}', '{city}', '{isp}', {valid_ping_count}, {avg_ping}, {stdev_ping})
'''

urls = ('/SubmitUserPingListInterface/', 'SubmitUserPingListInterface',
        '/SubmitUserPingListInterface', 'SubmitUserPingListInterface')


class SubmitUserPingListInterface:
    def GET(self):
        info = web.input()
        if not info:
            return ip_address
        else:
            try:
                if info['command'] == 'submit':
                    userid = info['userid']
                    username = info['username']
                    ipaddress = info['ipaddress']
                    pings = info['ipaddress'].split(';')
                    # db = MSSQL(host='182.254.133.64', user='sa', pwd='fdk^&asd;12fd', db='MobaDB')
                    # db.execute(insert_sql)
            except KeyError:
                return 'Lack Params'
            except Exception:
                return 'Params Error'


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()