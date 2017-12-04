# -*- coding: utf-8 -*-
import json
import MySQLdb
import time
from mailsender import sender

sql = '''
SELECT LEFT(DATE_SUB(DATE, INTERVAL 3 HOUR),10),AVG(CASE WHEN ab_test_value = 1 THEN is_win END) AS 'ab1的胜率',
COUNT(CASE WHEN ab_test_value = 1 THEN id END) /5 AS 'ab1的场次',
COUNT(CASE WHEN ab_test_value = 1 THEN id END) * AVG(CASE WHEN ab_test_value = 1 THEN is_win END)/5 AS 'ab1的胜场',
AVG(CASE WHEN ab_test_value = 2 THEN is_win END) AS 'ab2的胜率',
COUNT(CASE WHEN ab_test_value = 2 THEN id END) /5 AS 'ab2的场次',
COUNT(CASE WHEN ab_test_value = 2 THEN id END) * AVG(CASE WHEN ab_test_value = 2 THEN is_win END)/5 AS 'ab2的胜场',
AVG(is_win) AS '总的胜率',
COUNT(*) /5 AS '总的场次',
COUNT(*) * AVG(is_win)/5 AS '总的胜场', 
DATE_FORMAT(DATE, '%W') AS '工作日' 
FROM ai_stat_one_round 
WHERE is_ai = 1 AND map_name = '{map}' AND round_id IN 
(SELECT round_id FROM ai_stat_one_round WHERE is_ai = 1  AND DATE >=DATE_ADD('{st}', INTERVAL 3 HOUR) AND DATE<=DATE_ADD('{et}', INTERVAL 3 HOUR) 
GROUP BY round_id HAVING COUNT(*) = 5 AND SUM(LEVEL = {ai_difficulty}) = 5 AND (SUM(team=1) = 5 OR SUM(team=2) = 5)) GROUP BY LEFT(DATE_SUB(DATE, INTERVAL 3 HOUR),10)
'''

sql10v10 = '''
SELECT LEFT(DATE_SUB(DATE, INTERVAL 3 HOUR),10),AVG(CASE WHEN ab_test_value = 1 THEN is_win END) AS 'ab1的胜率',
COUNT(CASE WHEN ab_test_value = 1 THEN id END) / 10 AS 'ab1的场次',
COUNT(CASE WHEN ab_test_value = 1 THEN id END) * AVG(CASE WHEN ab_test_value = 1 THEN is_win END)/ 10 AS 'ab1的胜场', 
AVG(CASE WHEN ab_test_value = 2 THEN is_win END) AS 'ab2的胜率',
COUNT(CASE WHEN ab_test_value = 2 THEN id END) / 10 AS 'ab2的场次',
COUNT(CASE WHEN ab_test_value = 2 THEN id END) * AVG(CASE WHEN ab_test_value = 2 THEN is_win END)/ 10 AS 'ab2的胜场',
AVG(is_win) AS '总的胜率',
COUNT(*) / 10 AS '总的场次',
COUNT(*) * AVG(is_win)/ 10 AS '总的胜场', 
DATE_FORMAT(DATE, '%W') AS '工作日' 
FROM ai_stat_one_round 
WHERE map_name = '10v10' AND is_ai = 1 and DATE >=DATE_ADD('{st}', INTERVAL 3 HOUR) AND DATE<=DATE_ADD('{et}', INTERVAL 3 HOUR) GROUP BY LEFT(DATE_SUB(DATE, INTERVAL 3 HOUR),10)
'''

settings = json.load(open('settings.json', 'r'))

column_map = ['地图', '难度', 'ab1场次', 'ab1胜场', 'ab1胜率', 'ab2场次', 'ab2胜场', 'ab2胜率', '总场次', '胜场', '胜率']


def gen_table_head():
    head = ''
    for d in column_map:
        head += gen_a_tag('th', d)
    head = gen_a_tag('tr', head)
    return head


def gen_a_tag(tag, c='', attr=''):
    if isinstance(c, unicode):
        c = c.encode('utf-8')
    return '<{} {}>{}</{}>'.format(tag, attr, c, tag)


def send_report_mail(today, yesterday):
    conn_in = MySQLdb.connect(host=settings['host'], user=settings['user'], passwd=settings['passwd'], db=settings['db'], port=settings['port'])
    conn_in.set_character_set("utf8")
    cur_in = conn_in.cursor()
    # head
    content = gen_a_tag('h1', 'DAILY REPORT')
    content += gen_a_tag('p', 'DATE: {}~{}'.format(yesterday, today))
    content += '<br/>'
    # table
    tbl = gen_table_head()
    for m in settings['maps']:
        d_c = 1
        if m == 'FantasyAllStar':
            d_c = 4
        tbl += '<tr>' + gen_a_tag('td', m, 'rowspan=\"{}\"'.format(d_c))
        closed = False
        for d in settings['difficulty']:
            if closed:
                tbl += '<tr>'
            if m == '10v10':
                cur_in.execute(sql10v10.format(st=yesterday, et=today))
            else:
                cur_in.execute(sql.format(map=m, ai_difficulty=settings['difficulty'][d], st=yesterday, et=today))
            conn_in.commit()
            for res in cur_in:
                row = [d]
                row.extend([
                    round(res[2] or 0),
                    round(res[3] or 0),
                    float(res[1] or 0),
                    round(res[5] or 0),
                    round(res[6] or 0),
                    float(res[4] or 0),
                    round(res[8] or 0),
                    round(res[9] or 0),
                    float(res[7] or 0)
                ])
                print row
                for r in row:
                    tbl += gen_a_tag('td', r)
            tbl += '</tr>'
            closed = True
    content += gen_a_tag('table', tbl, 'border=\"1\"')

    title = '[AI]daily report'
    with open('html.html', 'w') as c:
        c.write(content)
    # ms = sender.MailSender()
    # ms.send_mail(title, content, settings['receiver_group'])


if __name__ == '__main__':
    last = ''
    while True:
        now = time.time()
        fmt_now = time.localtime(now)
        today = time.strftime('%Y-%m-%d', fmt_now)
        if fmt_now.tm_hour == 10 and fmt_now.tm_min == 0 and today != last or not last:
            print '{} sending mail'.format(today)
            yesterday = time.strftime('%Y-%m-%d', time.localtime(now - 24 * 3600))
            send_report_mail(today, yesterday)
            last = today
        time.sleep(1)
