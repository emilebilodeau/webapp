from flask import Flask, render_template
import sqlite3
import json

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template('welcome.html')

def get_db_connection():
    conn = sqlite3.connect('demo.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/data/")
def data():
    conn = get_db_connection()
    lumber = conn.execute('SELECT * FROM LumberFut ORDER BY Date').fetchall()
    conn.close()

    json_data = {
        'Date' : [],
        'Open' : [],
        'High' : [],
        'Low' : [],
        'Close*' : [],
        'Adj Close**' : [],
        'Volume' : []
    }

    # keeping every category except Date
    categories = list(json_data.keys())[1:7]

    for entry in lumber:
        json_data['Date'].append(entry['Date'][:10])
        for category in categories:
            if category == 'Volume':
                try:
                    json_data[category].append(int(entry[category]))
                except:
                    json_data[category].append(0)
            else:
                try:
                    json_data[category].append(float(entry[category]))
                except:
                    json_data[category].append(0.0)

    return render_template('data.html', json_data=json.dumps(json_data), categories=categories)