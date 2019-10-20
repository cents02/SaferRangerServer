import sqlite3
from flask import Flask, render_template, url_for, request, redirect
from flask import send_file
import requests
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from matplotlib.patches import Circle
import sys
import urllib.request
import json
from PIL import Image, ImageOps

app = Flask(__name__)
@app.route('/')
def home():
    return send_file('home.html')

blue = 'b'
red = 'r'
yellow = 'y'
green = 'g'

@app.route('/triggerballadd')
def triggerballaddfunc():
    return send_file('addball.html')

@app.route('/ballsget')
def ballsget():
    conn = sqlite3.connect('dbl.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT * FROM BALLS")

    rows = cur.fetchall()
    conn.close()
    return str(rows)


@app.route('/balladd', methods=["GET","POST"])
def balladd():
    if request.method == 'POST':
        id = request.form['ID']
        x = request.form['X']
        y = request.form['Y']
        date = request.form['DATE']
        status = request.form['STATUS']
        conn = sqlite3.connect('dbl.sqlite3')
        cur = conn.cursor()
        sqlite_insert_with_param = """INSERT INTO 'BALLS'
                          ('ID', 'X', 'Y', 'Date', 'Status')
                          VALUES (?, ?, ?, ?, ?);"""
        data_tuple = (id, x, y, date, status)
        cur.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        cur.close()
    return 'successfully added'

@app.route('/data')
def data_page():
    return send_file('form.html')

@app.route('/mapgen', methods = ["GET", "POST"])
def mapgenerate():
    if request.method == "POST":
        x = request.form['LON']
        y = request.form['LAT']

        URL = 'https://api.nasa.gov/planetary/earth/imagery/'

        PARAMS = {'lat':float(x), 'lon':float(y), 'dim':0.005, 'api_key':'yDGVtpaNPdr3GfFrbVxwoTIFA2MJru2Qtq5webkg'}
        r = requests.get(url = URL, params = PARAMS)

        data = r.json()
        print(data['url'])

        urllib.request.urlretrieve(data['url'], 'downloaded.png')

        conn = sqlite3.connect('dbl.sqlite3')
        cur = conn.cursor()
        cur.execute("SELECT * FROM BALLS")

        rows = cur.fetchall()
        image_file = cbook.get_sample_data('downloaded.png')

        img = plt.imread(image_file)


        circle_size = 1000

        fig,ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.imshow(img)
        for row in rows:
            if row[4] == 'dead':
                plt.scatter(row[1], row[2], s=circle_size, facecolors='none', edgecolors=red)
                plt.scatter(row[1],row[2],s=20, facecolors = red)
            elif row[4] == 'idle':
                plt.scatter(row[1], row[2], s=circle_size, facecolors='none', edgecolors=green)
                plt.scatter(row[1],row[2], s=20, facecolors = green)
            elif row[4] == 'tower':
                plt.scatter(row[1], row[2], s=circle_size*5, facecolors='none', edgecolors=blue)
                plt.scatter(row[1],row[2], s=20, facecolors = blue)

        plt.title('Position')
        plt.xlabel('Longitude')
        plt.ylabel('Inverse Latitude')
        plt.savefig('request.png')
        conn.close()
    return send_file('request.png')

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=5005)
