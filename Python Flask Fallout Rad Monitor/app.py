from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

THINGSPEAK_CHANNEL = 428543

def get_latest_data():
    url = f'https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL}/feeds.json?results=2000'
    resp = requests.get(url, timeout=5)
    data = resp.json()
    feeds = data['feeds']
    times = [f['created_at'] for f in feeds]
    cpm = [float(f['field1']) if f['field1'] else None for f in feeds]
    usv = [float(f['field2']) if f['field2'] else None for f in feeds]
    return {
        "times": times,
        "cpm": cpm,
        "usv": usv
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live-data')
def live_data():
    return jsonify(get_latest_data())

if __name__ == "__main__":
    app.run(debug=True, port=5009)
