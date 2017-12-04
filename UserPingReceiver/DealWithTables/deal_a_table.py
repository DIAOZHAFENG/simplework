import json
from data_process import MSSQL

if __name__ == '__main__':
    #dt = input()
    #table_name = 'UserPingListTable{}'.format(dt)
    with open('db_settings', 'r') as sf:
        s = json.load(sf)
        db = MSSQL(host=s['host'], user=s['user'], pwd=s['pwd'], db=s['db'])

        #db.deal_raw_table(table_name)
        #db.process_data(table_name)
        db.get_report()
