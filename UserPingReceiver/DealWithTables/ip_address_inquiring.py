# -*- coding: utf8 -*-
import random
from time import time

import sys

from data_process import MSSQL

sql = '''
    select ip1, ip2, area, city, isp from ipAddress order by ip1
'''


def in_range(ip, t):
    if ip < int(t[0]):
        return -1
    elif ip <= int(t[1]):
        return 0
    else:
        return 1


class IPInquiry:
    def __init__(self, db):
        result = db.query_itr(sql)
        self.group_map = {}
        for t in result:
            ip_group1 = int(t[0]) // 65536
            ip_group2 = int(t[1]) // 65536
            for ip_group in xrange(ip_group1, ip_group2+1):
                if not self.group_map.get(ip_group):
                    self.group_map[ip_group] = [t]
                else:
                    self.group_map[ip_group].append(t)

    def directly_inquire(self, ip):
        group_range = self.group_map.get(int(ip)//65536, [])
        result = -1, -1, '', '', ''
        for t in group_range:
            if in_range(ip, t) == 0:
                result = t
                if t[3]:
                    break
        return result

    # def inquire(self, ip, begin=0, end=None):
    #     end = end or len(self.result)-1
    #     if begin > end or in_range(ip, self.result[begin]) < 0:
    #         # print ip, begin, self.result[begin]
    #         return -1, -1, '', '', ''
    #     mid = (begin+end)/2
    #     cmpr = in_range(ip, self.result[mid])
    #     if cmpr < 0:
    #         return self.inquire(ip=ip, begin=begin, end=mid-1)
    #     elif cmpr == 0:
    #         if not self.result[mid][3]:
    #             if mid - 1 >= 0:
    #                 if in_range(ip, self.result[mid-1]) == 0:
    #                     return self.result[mid-1]
    #             if mid + 1 < len(self.result):
    #                 if in_range(ip, self.result[mid+1]) == 0:
    #                     return self.result[mid+1]
    #         return self.result[mid]
    #     else:
    #         return self.inquire(ip=ip, begin=mid+1, end=end)


if __name__ == '__main__':
    import json
    with open('db_settings', 'r') as sf:
        s = json.load(sf)
        dbc = MSSQL(host=s['host'], user=s['user'], pwd=s['pwd'], db=s['db'])
        i = IPInquiry(dbc)
        print(sys.getsizeof(i.group_map))
        count = 0
        r = dbc.query(sql)
        start_time = time()
        for a in r:
            random_ip = random.randint(int(a[0]), int(a[1]))
            try:
                if i.directly_inquire(random_ip)[0] < 0:
                    raise Exception
            except Exception:
                count += 1
                print 'error', random_ip,
                for v in a:
                    print v,
                print ''
        print count, '/', len(r)
        print time() - start_time
