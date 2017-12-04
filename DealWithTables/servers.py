import json
import math
import urllib
import web
import gc
import threading
from data_process import MSSQL
from ip_address_inquiring import IPInquiry

ip_address = open('ip_address').read()

insert_sql = u'''
INSERT INTO UserPingListTable
VALUES ({}, '{}', '{}', '{}', getdate(), {}
'{}', '{}', '{}', {}, {}, {})
'''

urls = ('/SubmitUserPingListInterface/', 'SubmitUserPingListInterface',
        '/SubmitUserPingListInterface', 'SubmitUserPingListInterface')

s = {}
with open('db_settings', 'r') as sf:
    s = json.load(sf)
ip_inquiry = IPInquiry(MSSQL(host=s['host'], user=s['user'], pwd=s['pwd'], db=s['db']))


def ip2int(ip):
    try:
        a = ip.split('.')
        r = 0
        for i in range(4):
            r *= 256
            r += int(a[i])
        return r
    except Exception:
        return -1


def get_info(url):
    a = url.split('?', 1)
    if len(a) > 1:
        p_str = a[1]
        kvs = p_str.split('&')
        r = {}
        for kv in kvs:
            pair = kv.split('=')
            try:
                r[pair[0]] = pair[1]
            except Exception:
                pass
        return r
    return {}


class SubmitUserPingListInterface:
    def GET(self):
        info = get_info(web.ctx.fullpath)
        # info = web.input()
        if not info:
            return ip_address
        else:
            # i can't figure out a way to solve the chinese codec problem
            info['username'] = web.input().get('username')
            try:
                if info['command'] == 'submit':
                    userid = info['userid']
                    username = info['username']
                    req_address = web.ctx.env.get('REMOTE_ADDR')
                    ipaddress = info['ipaddress']
                    # ip_inquiry = IPInquiry(db)
                    res = ip_inquiry.directly_inquire(ip2int(req_address))
                    area = res[2] or ''
                    city = res[3] or ''
                    isp = res[4] or ''
                    pings = urllib.unquote(info['pings']).split(';')
                    for k in info:
                        if not info[k]:
                            pings.append(k)
                    int_pings = []
                    avg_ping = 0
                    for p in pings:
                        try:
                            int_p = int(p)  # may raise exception

                            int_pings.append(int_p)
                            avg_ping += int_p
                        except Exception:
                            continue
                    valid_ping_count = len(int_pings)
                    stdev_ping = 0
                    if valid_ping_count > 0:
                        avg_ping /= valid_ping_count
                        for p in int_pings:
                            stdev_ping += (p-avg_ping) * (p-avg_ping)
                        stdev_ping = math.sqrt(stdev_ping/valid_ping_count)
                    ping_str = ''
                    for i in xrange(100):
                        if i < valid_ping_count:
                            ping_str += str(int_pings[i]) + ','
                        else:
                            ping_str += 'null,'
                    db = MSSQL(host=s['host'], user=s['user'], pwd=s['pwd'], db=s['db'])
                    to_exc = insert_sql.format(userid, username, ipaddress, req_address, ping_str, area, city, isp, valid_ping_count, avg_ping, stdev_ping)
                    # t = threading.Thread(target = db.execute, args = (to_exc,))
                    # t.start()
                    db.execute(to_exc)
                else:
                    with open('record', 'a+') as r:
                        r.write(web.ctx.fullpath + '\r\n')
            except KeyError, e:
                with open('error_request', 'a') as er:
                    print web.ctx.fullpath
                    er.write(web.ctx.fullpath)
                    er.write(str(e) + '\n')
                return 'Lack Params'
            except Exception, e:
                print type(e), str(e)
                return 'Params Error'


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
