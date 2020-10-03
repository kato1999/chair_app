import random
from flask import Flask, render_template, make_response, Markup, request
from io import BytesIO

from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from matplotlib.dates import drange
from matplotlib.dates import DateFormatter
import matplotlib as mpl

import datetime as dt

import pandas as pd
import datetime as dt
import numpy as np
import sqlite3

# 文字コードエラーへの対応
import locale
locale.setlocale(locale.LC_ALL, '')

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']


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
    return render_template("index.html", title="社畜椅子")


@app.route('/img')
def img_show():
    # リロード時の重複回避
    plt.close(1)

    fig = plt.figure(1, figsize=(10,6),)

    # 軸が見切れないように
    fig.subplots_adjust(bottom=0.2)

    # 軸などの設定
    # plt.title('Graph')
    plt.grid()

    axes = fig.add_subplot(111)
    xaxis = axes.xaxis
    yaxis = axes.yaxis
    plt.xticks(rotation=20)
    xaxis.set_major_formatter(DateFormatter('%m月%d日 %H:%M:%S'))
    plt.xlabel('時間', fontsize=15)
    plt.ylabel('スコア', fontsize=15)
    y_min, y_max = axes.get_ylim()
    axes.set_ylim(0, 103)

    XY = get_from_db()

    name = request.args.get('name')
    if name=="judge":
        if len(XY[0])==0:
            time = str(dt.datetime.now())[:19]
            x = pd.date_range(time,periods=24*6,freq='10T')
            y = [-1]*24*6
        else:
            x = XY[0]
            y = XY[1]

    elif name=="exist":
        yaxis.set_major_formatter(mpl.ticker.PercentFormatter(100))
        if len(XY[0])==0:
            time = str(dt.datetime.now())[:19]
            x = pd.date_range(time,periods=24*6,freq='10T')
            y = [-1]*24*6
        else:
            x = XY[0]
            y = XY[2]

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
    result = cur.fetchall()

    X = []
    Y = []
    X_exist = []
    Y_exist = []

    counter = 60
    for i in range(len(result)//counter):
        # 2016-06-02 05:00:00
        memo = str(result[i*counter][0])
        time = dt.datetime(int(memo[:4]), int(memo[4:6]), int(memo[6:8]), int(memo[8:10]), int(memo[10:12]), int(memo[12:14]))
        
        cnt_good = 0
        cnt_all = 0.01

        cnt_exist = 0
        cnt_exist_all = 0.01

        for j in range(counter):
            if result[i*counter+j][1]==1:
                cnt_good += 1
            if result[i*counter+j][2]==1:
                cnt_exist += 1
            cnt_all += 1
            cnt_exist_all += 1

        X.append(time)
        Y.append((cnt_good/cnt_all)*100)
        Y_exist.append((cnt_exist/cnt_all)*100)

    con.commit()
    cur.close()
    con.close()
    return [X, Y, Y_exist]



if __name__ == "__main__":
    app.run(debug=True)