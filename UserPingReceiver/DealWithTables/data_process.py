# -*- coding: gbk -*-
import json
import pyodbc
import datetime
import time

# queries
make_sample = '''
    drop table sample;
    select top 5000 * into sample from UserPingListTable
    '''
calculate_valid_ping_count = '''
    update {table_name} set valid_ping_count = CASE when ping1 < 1000 then 1 else 0 end + CASE when ping2 < 1000 then 1 else 0 end + CASE when ping3 < 1000 then 1 else 0 end + CASE when ping4 < 1000 then 1 else 0 end + CASE when ping5 < 1000 then 1 else 0 end + CASE when ping6 < 1000 then 1 else 0 end + CASE when ping7 < 1000 then 1 else 0 end + CASE when ping8 < 1000 then 1 else 0 end + CASE when ping9 < 1000 then 1 else 0 end + CASE when ping10 < 1000 then 1 else 0 end + CASE when ping11 < 1000 then 1 else 0 end + CASE when ping12 < 1000 then 1 else 0 end + CASE when ping13 < 1000 then 1 else 0 end + CASE when ping14 < 1000 then 1 else 0 end + CASE when ping15 < 1000 then 1 else 0 end + CASE when ping16 < 1000 then 1 else 0 end + CASE when ping17 < 1000 then 1 else 0 end + CASE when ping18 < 1000 then 1 else 0 end + CASE when ping19 < 1000 then 1 else 0 end + CASE when ping20 < 1000 then 1 else 0 end + CASE when ping21 < 1000 then 1 else 0 end + CASE when ping22 < 1000 then 1 else 0 end + CASE when ping23 < 1000 then 1 else 0 end + CASE when ping24 < 1000 then 1 else 0 end + CASE when ping25 < 1000 then 1 else 0 end + CASE when ping26 < 1000 then 1 else 0 end + CASE when ping27 < 1000 then 1 else 0 end + CASE when ping28 < 1000 then 1 else 0 end + CASE when ping29 < 1000 then 1 else 0 end + CASE when ping30 < 1000 then 1 else 0 end + CASE when ping31 < 1000 then 1 else 0 end + CASE when ping32 < 1000 then 1 else 0 end + CASE when ping33 < 1000 then 1 else 0 end + CASE when ping34 < 1000 then 1 else 0 end + CASE when ping35 < 1000 then 1 else 0 end + CASE when ping36 < 1000 then 1 else 0 end + CASE when ping37 < 1000 then 1 else 0 end + CASE when ping38 < 1000 then 1 else 0 end + CASE when ping39 < 1000 then 1 else 0 end + CASE when ping40 < 1000 then 1 else 0 end + CASE when ping41 < 1000 then 1 else 0 end + CASE when ping42 < 1000 then 1 else 0 end + CASE when ping43 < 1000 then 1 else 0 end + CASE when ping44 < 1000 then 1 else 0 end + CASE when ping45 < 1000 then 1 else 0 end + CASE when ping46 < 1000 then 1 else 0 end + CASE when ping47 < 1000 then 1 else 0 end + CASE when ping48 < 1000 then 1 else 0 end + CASE when ping49 < 1000 then 1 else 0 end + CASE when ping50 < 1000 then 1 else 0 end + CASE when ping51 < 1000 then 1 else 0 end + CASE when ping52 < 1000 then 1 else 0 end + CASE when ping53 < 1000 then 1 else 0 end + CASE when ping54 < 1000 then 1 else 0 end + CASE when ping55 < 1000 then 1 else 0 end + CASE when ping56 < 1000 then 1 else 0 end + CASE when ping57 < 1000 then 1 else 0 end + CASE when ping58 < 1000 then 1 else 0 end + CASE when ping59 < 1000 then 1 else 0 end + CASE when ping60 < 1000 then 1 else 0 end
    '''
calculate_avg_ping = '''
    update {table_name} set avg_ping = case when valid_ping_count = 0 then 0 else cast (ping1+ping2+ping3+ping4+ping5+ping6+ping7+ping8+ping9+ping10+ping11+ping12+ping13+ping14+ping15+ping16+ping17+ping18+ping19+ping20+ping21+ping22+ping23+ping24+ping25+ping26+ping27+ping28+ping29+ping30+ping31+ping32+ping33+ping34+ping35+ping36+ping37+ping38+ping39+ping40+ping41+ping42+ping43+ping44+ping45+ping46+ping47+ping48+ping49+ping50+ping51+ping52+ping53+ping54+ping55+ping56+ping57+ping58+ping59+ping60 - (60-valid_ping_count)*1000 as float) / valid_ping_count end
    '''
calculate_stdev_ping = '''
    update {table_name} set stdev_ping = case when valid_ping_count = 0 then 0
    else
    sqrt(
    (
    case when ping1 = 1000 then 0 else square(ping1 - avg_ping) end + case when ping2 = 1000 then 0 else square(ping2 - avg_ping) end + case when ping3 = 1000 then 0 else square(ping3 - avg_ping) end + case when ping4 = 1000 then 0 else square(ping4 - avg_ping) end + case when ping5 = 1000 then 0 else square(ping5 - avg_ping) end + case when ping6 = 1000 then 0 else square(ping6 - avg_ping) end + case when ping7 = 1000 then 0 else square(ping7 - avg_ping) end + case when ping8 = 1000 then 0 else square(ping8 - avg_ping) end + case when ping9 = 1000 then 0 else square(ping9 - avg_ping) end + case when ping10 = 1000 then 0 else square(ping10 - avg_ping) end + case when ping11 = 1000 then 0 else square(ping11 - avg_ping) end + case when ping12 = 1000 then 0 else square(ping12 - avg_ping) end + case when ping13 = 1000 then 0 else square(ping13 - avg_ping) end + case when ping14 = 1000 then 0 else square(ping14 - avg_ping) end + case when ping15 = 1000 then 0 else square(ping15 - avg_ping) end + case when ping16 = 1000 then 0 else square(ping16 - avg_ping) end + case when ping17 = 1000 then 0 else square(ping17 - avg_ping) end + case when ping18 = 1000 then 0 else square(ping18 - avg_ping) end + case when ping19 = 1000 then 0 else square(ping19 - avg_ping) end + case when ping20 = 1000 then 0 else square(ping20 - avg_ping) end + case when ping21 = 1000 then 0 else square(ping21 - avg_ping) end + case when ping22 = 1000 then 0 else square(ping22 - avg_ping) end + case when ping23 = 1000 then 0 else square(ping23 - avg_ping) end + case when ping24 = 1000 then 0 else square(ping24 - avg_ping) end + case when ping25 = 1000 then 0 else square(ping25 - avg_ping) end + case when ping26 = 1000 then 0 else square(ping26 - avg_ping) end + case when ping27 = 1000 then 0 else square(ping27 - avg_ping) end + case when ping28 = 1000 then 0 else square(ping28 - avg_ping) end + case when ping29 = 1000 then 0 else square(ping29 - avg_ping) end + case when ping30 = 1000 then 0 else square(ping30 - avg_ping) end + case when ping31 = 1000 then 0 else square(ping31 - avg_ping) end + case when ping32 = 1000 then 0 else square(ping32 - avg_ping) end + case when ping33 = 1000 then 0 else square(ping33 - avg_ping) end + case when ping34 = 1000 then 0 else square(ping34 - avg_ping) end + case when ping35 = 1000 then 0 else square(ping35 - avg_ping) end + case when ping36 = 1000 then 0 else square(ping36 - avg_ping) end + case when ping37 = 1000 then 0 else square(ping37 - avg_ping) end + case when ping38 = 1000 then 0 else square(ping38 - avg_ping) end + case when ping39 = 1000 then 0 else square(ping39 - avg_ping) end + case when ping40 = 1000 then 0 else square(ping40 - avg_ping) end + case when ping41 = 1000 then 0 else square(ping41 - avg_ping) end + case when ping42 = 1000 then 0 else square(ping42 - avg_ping) end + case when ping43 = 1000 then 0 else square(ping43 - avg_ping) end + case when ping44 = 1000 then 0 else square(ping44 - avg_ping) end + case when ping45 = 1000 then 0 else square(ping45 - avg_ping) end + case when ping46 = 1000 then 0 else square(ping46 - avg_ping) end + case when ping47 = 1000 then 0 else square(ping47 - avg_ping) end + case when ping48 = 1000 then 0 else square(ping48 - avg_ping) end + case when ping49 = 1000 then 0 else square(ping49 - avg_ping) end + case when ping50 = 1000 then 0 else square(ping50 - avg_ping) end + case when ping51 = 1000 then 0 else square(ping51 - avg_ping) end + case when ping52 = 1000 then 0 else square(ping52 - avg_ping) end + case when ping53 = 1000 then 0 else square(ping53 - avg_ping) end + case when ping54 = 1000 then 0 else square(ping54 - avg_ping) end + case when ping55 = 1000 then 0 else square(ping55 - avg_ping) end + case when ping56 = 1000 then 0 else square(ping56 - avg_ping) end + case when ping57 = 1000 then 0 else square(ping57 - avg_ping) end + case when ping58 = 1000 then 0 else square(ping58 - avg_ping) end + case when ping59 = 1000 then 0 else square(ping59 - avg_ping) end + case when ping60 = 1000 then 0 else square(ping60 - avg_ping) end
    ) / valid_ping_count
    )
    end
    '''
update_null_val = '''
    update {table_name} set area = 'null' where area is null
    update {table_name} set isp = 'null' where isp is null
    '''
produce_detail_report = '''
    drop table detail_report;
    select count(*) as 测试次数, avg(avg_ping) as Ping的平均值的平均值, avg(stdev_ping) as Ping的标准差的平均值, avg(cast(60 - valid_ping_count as float) / 60) as 丢包率平均值, 0 as 完全丢包次数
        , IpAddress, convert(varchar(13), createTime, 120) as 日期, isp, area
    into detail_report
    from {table_name}
    where valid_ping_count > 0
    group by ipAddress, convert(varchar(13), createTime, 120), isp, area order by 日期
    '''
# select * from detail_report order by 日期; FOR TEST
produce_complete_loss = '''
    drop table complete_loss_detail;
    select count(*) as 测试次数,
            count(case when valid_ping_count = 0 then 1 else null end) as 完全丢包次数,
            IpAddress,
            convert(varchar(13), createTime, 120) as 日期,
            isp, area
    into complete_loss_detail
    from {table_name}
    group by IpAddress, convert(varchar(13), createTime, 120), isp, area order by 日期
    '''
# select * from complete_loss_detail FOR TEST
join_detail = '''
    insert into final_result_province
    select * from (
        select t1.*, ip.Name from (
            select a.日期, b.测试次数 as 总测试次数, a.丢包率平均值, cast(b.完全丢包次数 as float)/ b.测试次数 as 全丢包率, a.Ping的平均值的平均值, a.测试次数 as 有返回测试次数, b.完全丢包次数, a.Ping的标准差的平均值,
                a.IpAddress, a.isp, a.area
            from detail_report as a inner join complete_loss_detail as b
        on a.IpAddress = b.IpAddress and a.isp = b.isp and a.area = b.area and a.日期 = b.日期 and b.测试次数 > {times}) as t1 left outer join ip on t1.IpAddress = ip.IpAddress) as tt1
    '''
produce_report_isp = '''
    insert into final_report_isp
    select distinct 日期, sum(总测试次数) as 总测试次数,
                sum(丢包率平均值 * 有返回测试次数) / sum(有返回测试次数) as 丢包率平均值,
                sum(全丢包率 * 总测试次数) / sum(总测试次数) as 全丢包率,
                sum(Ping的平均值的平均值 * 有返回测试次数) / sum(有返回测试次数) as Ping的平均值的平均值,
                sum(有返回测试次数) as 有返回测试次数,
                sum(完全丢包次数) as 完全丢包次数,
                sum(Ping的标准差的平均值 * 有返回测试次数) / sum(有返回测试次数) as Ping的标准差的平均值,
    IpAddress, isp, Name from final_result_province group by IpAddress, isp, 日期, Name
    '''
produce_report = '''
    insert into final_report
    select distinct 日期, sum(总测试次数) as 总测试次数,
                sum(丢包率平均值 * 有返回测试次数) / sum(有返回测试次数) as 丢包率平均值,
                sum(全丢包率 * 总测试次数) / sum(总测试次数) as 全丢包率,
                    sum(Ping的平均值的平均值 * 有返回测试次数) / sum(有返回测试次数) as Ping的平均值的平均值,
                sum(有返回测试次数) as 有返回测试次数,
                sum(完全丢包次数) as 完全丢包次数,
                sum(Ping的标准差的平均值 * 有返回测试次数) / sum(有返回测试次数) as Ping的标准差的平均值,
    IpAddress, Name from final_result_province group by IpAddress, 日期, Name
    '''
test_sql = '''
    select * from (
    select t1.*, ip.Name from (
        select a.日期, b.测试次数 as 总测试次数, a.丢包率平均值, cast(b.完全丢包次数 as float)/ b.测试次数 as 全丢包率, a.Ping的平均值的平均值, a.测试次数 as 有返回测试次数, b.完全丢包次数, a.Ping的标准差的平均值,
            a.IpAddress, a.isp, a.area
        from detail_report as a inner join complete_loss_detail as b
    on a.IpAddress = b.IpAddress and a.isp = b.isp and a.area = b.area and a.日期 = b.日期 and b.测试次数 > 1000) as t1 left outer join ip on t1.IpAddress = ip.IpAddress) as tt1
    '''
get_ping_tables = '''
    SELECT Name FROM SysObjects Where XType='U' AND Name LIKE 'UserPingListTable_%' ORDER BY Name
    '''


class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.conn = None

    def __connect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pyodbc.connect('DRIVER={driver};SERVER={host};DATABASE={database};UID={user};PWD={password}'.format(driver='{SQL Server}', host=self.host, user=self.user, password=self.pwd, database=self.db))
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def query(self, sql):
        cur = self.__connect()
        cur.execute(sql)
        res_list = cur.fetchall()
        # 查询完毕后必须关闭连接
        self.conn.close()
        return res_list

    def query_itr(self, sql):
        cur = self.__connect()
        cur.execute(sql)
        while True:
            row = cur.fetchone()
            if row:
                yield row
            else:
                break
        # 查询完毕后必须关闭连接
        self.conn.close()

    def execute(self, sql):
        cur = self.__connect()
        print sql
        cur.execute(sql)
        # 执行完毕后提交并关闭连接
        self.conn.commit()
        self.conn.close()

    def new_empty_table(self):
        try:
            now = datetime.datetime.now()
            table_name = self.__get_dt_str(now)
            self.execute("execute sp_rename 'UserPingListTable' ,'{}'".format(table_name))
            self.execute(open('UserPingListTable.sql', 'r').read())
            table_list = self.query(get_ping_tables)
            if len(table_list) > 24:
                for i in xrange(len(table_list) - 24):
                    self.execute('drop table {}'.format(table_list[i][0]))
            # print table_name
            return table_name
        except Exception, e:
            print str(e), 'may fail to new table'

    def __get_dt_str(self, dt):
        month = '{:0>2}'.format(dt.month)
        day = '{:0>2}'.format(dt.day)
        hour = '{:0>2}'.format(dt.hour)
        return 'UserPingListTable{y}{m}{d}{h}'.format(y=dt.year, m=month, d=day, h=hour)

    def deal_raw_table(self, table_name):
        self.execute(calculate_valid_ping_count.format(table_name=table_name))
        self.execute(calculate_avg_ping.format(table_name=table_name))
        self.execute(calculate_stdev_ping.format(table_name=table_name))

    def process_data(self, table_name):
        self.execute(produce_detail_report.format(table_name=table_name))
        self.execute(produce_complete_loss.format(table_name=table_name))
        self.execute(update_null_val.format(table_name='detail_report'))
        self.execute(update_null_val.format(table_name='complete_loss_detail'))

    def get_report(self, times=100):
        self.execute(join_detail.format(times=times))
        self.execute(produce_report_isp)
        self.execute(produce_report)

    def test(self, table_name=''):
        if not table_name:
            self.execute(make_sample)
            table_name = 'sample'
        self.deal_raw_table(table_name)
        self.process_data(table_name)
        self.get_report()

    def deal(self):
        table_name = self.new_empty_table()
        self.deal_raw_table(table_name)
        self.process_data(table_name)
        self.get_report()

if __name__ == '__main__':
    last_deal = -1
    with open('db_settings', 'r') as sf:
        s = json.load(sf)
        db = MSSQL(host=s['host'], user=s['user'], pwd=s['pwd'], db=s['db'])
        while True:
            now = datetime.datetime.now()
            if now.hour != last_deal and now.minute == 0:
                print '{}:00 start processing'.format(now.hour)
                # 本来还判断了秒是否为零，想想感觉没必要hour变了的时候肯定是整点，除非上一个循坏卡了一个多小时，连分也不需要判断，但还是先保留了
                db.deal()
                last_deal = now.hour
            time.sleep(1)
