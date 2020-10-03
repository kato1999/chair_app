import sqlite3
import random

# sqlite3（SQLサーバ）モジュールをインポート


dbname = 'database.db'

# テーブルの作成
con = sqlite3.connect(dbname)
cur = con.cursor()

# 年(4桁)月日時間(24時間表示)分秒,(年以外は2桁表示)
# ex:20201003160502

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
    year = 20201003
    hour = 0
    mint = 0
    sec = 0
    for i in range(10):
        for j in range(60):
            for k in range(60):
                time = year*1000000+hour*10000+mint*100+sec
                main(time)
                sec += 1
                sec %= 60
            mint += 1
            mint %= 60
        hour += 1
        hour %= 24
    
    