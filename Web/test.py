import sqlite3
import random

# sqlite3（SQLサーバ）モジュールをインポート


dbname = 'database.db'

# テーブルの作成
con = sqlite3.connect(dbname)
cur = con.cursor()
create_table = 'create table if not exists pose_data(time int, judge int, exist int)'
cur.execute(create_table)
con.commit()
cur.close()
con.close()

def main(time):
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    sql = 'insert into pose_data(time, judge, exist) values (?,?,?)'
    cur.execute(sql, (time, random.randint(0,100)%2, random.randint(0,100)%2))
    con.commit()
    cur.close()
    con.close()



if __name__ == '__main__':
    time = 20201003161205
    for i in range(24*60):
        main(time)
        time += 1
    