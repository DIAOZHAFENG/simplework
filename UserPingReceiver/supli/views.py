# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import urllib
import math
from django.http import HttpResponse
from django.shortcuts import render
from DealWithTables.db_inconnect import MSSQL
from DealWithTables.ip_address_inquiring import IPInquiry

ip_address = open('supli/ip_address').read()

insert_sql = u'''
INSERT INTO UserPingListTable
VALUES ({}, '{}', '{}', '{}', getdate(), {}
'{}', '{}', '{}', {}, {}, {})
'''

s = {}
with open('../DealWithTables/db_settings', 'r') as sf:
    s = json.load(sf)
ip_inquiry = IPInquiry(MSSQL())


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
    a = urllib.unquote(url).split('?', 1)
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


# Create your views here.
def SubmitUserPingListInterface(request):
    info = get_info(request.get_full_path())
    if not info.get('command'):
        return HttpResponse(ip_address)
    else:
        try:
            if info['command'] == 'submit':
                userid = info['userid']
                username = request.GET.get('username')
                req_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
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
                        stdev_ping += (p - avg_ping) * (p - avg_ping)
                    stdev_ping = math.sqrt(stdev_ping / valid_ping_count)
                ping_str = ''
                for i in xrange(100):
                    if i < valid_ping_count:
                        ping_str += str(int_pings[i]) + ','
                    else:
                        ping_str += 'null,'
                db = MSSQL()
                to_exc = insert_sql.format(userid, username, ipaddress, req_address, ping_str, area, city, isp,
                                           valid_ping_count, avg_ping, stdev_ping)
                print to_exc
                # t = threading.Thread(target = db.execute, args = (to_exc,))
                # t.start()
                # db.execute(to_exc)
                return HttpResponse(to_exc)
            else:
                with open('record', 'a+') as r:
                    r.write(request.get_full_path() + '\r\n')
        except KeyError, e:
            with open('error_request', 'a') as er:
                print request.get_full_path()
                er.write(request.get_full_path())
                er.write(str(e) + '\n')
            return HttpResponse('Lack Params')
        except Exception, e:
            with open('error_request', 'a') as er:
                print type(e), str(e)
                er.write(request.get_full_path() + '\n')
                er.write(str(type(e)) + ': ' + str(e) + '\n')
            return HttpResponse('Params Error')
