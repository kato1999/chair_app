import random
from flask import Flask, render_template, make_response
from io import BytesIO

from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from matplotlib.dates import drange
from matplotlib.dates import DateFormatter

import pandas as pd
import datetime as dt
import numpy as np
import sqlite3


app = Flask(__name__)


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


@app.route("/")
def top_page():
    return render_template("index.html", title="社畜椅子",  result=get_from_db())


@app.route('/img')
def img_show():
    # リロード時の重複回避
    plt.close(1)

    fig = plt.figure(1, figsize=(10,6))

    # 軸が見切れないように
    fig.subplots_adjust(bottom=0.2)

    # 軸などの設定
    # plt.title('Graph')
    plt.xlabel('time')
    plt.ylabel('percentage')
    plt.grid()

    axes = fig.add_subplot(111)
    xaxis = axes.xaxis
    plt.xticks(rotation=20)
    xaxis.set_major_formatter(DateFormatter('%m.%d %H:%M'))

    # 値の設定
    y = np.random.randint(0,100,24*6)
    x = pd.date_range('2016-06-02 05:00:00',periods=24*6,freq='10T')

    axes.plot(x, y)


    # 図を返すためのおまじない
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    
    return response


def get_from_db():
    # データベース接続とカーソル生成
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    con.text_factory = str
    
    sql = 'select * from pose_data order by time'
    cur.execute(sql)
    list1 = cur.fetchall()

    memo = ""
    for i in list1:
        memo += str(i[0])+Markup("<br>")


    con.commit()
    cur.close()
    con.close()
    
    return memo

# 年(4桁)月日時間(24時間表示)分秒,(年以外は2桁表示)
# ex:20201003160502


if __name__ == "__main__":
    app.run(debug=True)