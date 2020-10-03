from flask import Flask, render_template, make_response
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
import numpy as np


app = Flask(__name__)



@app.route("/")
def top_page():
    return render_template("index.html", title="社畜椅子")


@app.route('/img')
def img_show():
    fig = plt.figure(figsize=(10,5))

    plt.title('Graph')
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    x = [100, 200, 300, 400, 500, 600]
    y = [10, 20, 30, 50, 80, 130]
    plt.plot(x, y)
    
    # 図を返すためのおまじない
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()

    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    
    print()
    return response


if __name__ == "__main__":
    app.run(debug=True)