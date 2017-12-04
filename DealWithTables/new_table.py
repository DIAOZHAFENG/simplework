import json
from data_process import MSSQL

if __name__ == '__main__':
    with open('db_settings', 'r') as sf:
        s = json.load(sf)
        db = MSSQL(host=s['host'], user=s['user'], pwd=s['pwd'], db=s['db'])
        db.new_empty_table()