import os
from flask import Flask, render_template, url_for
import feedparser
import datetime
import requests
import csv
import re  # For our regex approach

app = Flask(__name__)

RTE_NEWS_FEED = "https://www.rte.ie/feeds/rss/?index=/news/"

def get_rte_news():
    feed = feedparser.parse(RTE_NEWS_FEED)
    headlines = []
    if feed.entries:
        for entry in feed.entries:
            headlines.append({
                "title": entry.title,
                "summary": entry.summary if hasattr(entry, 'summary') else "",
                "link": entry.link
            })
    return headlines

def load_substitutions(csv_file=None):
    """
    Loads a dictionary of {word: explanation} from a CSV file.
    If csv_file is None, we automatically build the absolute path to 'substitutions.csv'
    in the same directory as this script.
    """
    if csv_file is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file = os.path.join(script_dir, "substitutions.csv")

    subs = {}
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    key = row[0].strip()
                    explanation = row[1].strip()
                    subs[key] = explanation
    except Exception as e:
        print("Error loading CSV:", e)
    return subs

def granny_substitutions(text, subs):
    """
    Use regex to replace each key with 'key (explanation)' only the FIRST time
    it appears in 'text', ignoring case but preserving the original matched case.
    We do word-boundary matching so "Man" won't match inside "Manchester" etc.
    """
    replaced_keys = set()
    for key, explanation in subs.items():
        pattern = r"\b" + re.escape(key) + r"\b"

        def replacement_func(match):
            original_word = match.group(0)  # e.g. "Man" or "man"
            if key in replaced_keys:
                return original_word  # skip if already replaced once
            replaced_keys.add(key)
            return f"{original_word} ({explanation})"

        # Replace only the first occurrence per key (count=1), ignoring case
        text = re.sub(pattern, replacement_func, text, count=1, flags=re.IGNORECASE)
    return text

@app.context_processor
def inject_date():
    now = datetime.datetime.now()
    day_of_week = now.strftime("%a").upper()
    day = now.strftime("%d")
    month = now.strftime("%b").upper()
    year = now.strftime("%Y")
    date_string = day_of_week + " " + day + " " + month + " " + year
    return {"today_date": date_string}

@app.route("/")
def index_redirect():
    return '<html><head><meta http-equiv="refresh" content="0; url=/100" /></head><body></body></html>'

@app.route("/100")
def page_100():
    return render_template("100.html", page_number=100)

@app.route("/101")
def page_101():
    headlines = get_rte_news()
    # Load granny-style substitutions with an absolute path
    subs = load_substitutions()  # no argument => uses "substitutions.csv" in script folder

    for item in headlines:
        item["title"] = granny_substitutions(item["title"], subs)
        # If you want to substitute in summaries as well, add this:
        # item["summary"] = granny_substitutions(item["summary"], subs)

    return render_template("101.html", page_number=101, headlines=headlines)

@app.route("/102")
def page_102():
    headlines = get_rte_news()
    headlines = headlines[3:]
    return render_template("102.html", page_number=102, headlines=headlines)

@app.route("/104")
def page_104():
    headlines = get_rte_news()
    item = headlines[0] if len(headlines) > 0 else {"title": "No data", "summary": ""}
    return render_template("104.html", page_number=104, item=item)

@app.route("/105")
def page_105():
    headlines = get_rte_news()
    item = headlines[1] if len(headlines) > 1 else {"title": "No data", "summary": ""}
    return render_template("105.html", page_number=105, item=item)

@app.route("/106")
def page_106():
    headlines = get_rte_news()
    item = headlines[2] if len(headlines) > 2 else {"title": "No data", "summary": ""}
    return render_template("106.html", page_number=106, item=item)

@app.route("/107")
def page_107():
    headlines = get_rte_news()
    item = headlines[3] if len(headlines) > 3 else {"title": "No data", "summary": ""}
    return render_template("107.html", page_number=107, item=item)

@app.route("/108")
def page_108():
    headlines = get_rte_news()
    item = headlines[4] if len(headlines) > 4 else {"title": "No data", "summary": ""}
    return render_template("108.html", page_number=108, item=item)

@app.route("/109")
def page_109():
    headlines = get_rte_news()
    item = headlines[5] if len(headlines) > 5 else {"title": "No data", "summary": ""}
    return render_template("109.html", page_number=109, item=item)

@app.route("/110")
def page_110():
    headlines = get_rte_news()
    item = headlines[6] if len(headlines) > 6 else {"title": "No data", "summary": ""}
    return render_template("110.html", page_number=110, item=item)

@app.route("/111")
def page_111():
    headlines = get_rte_news()
    item = headlines[7] if len(headlines) > 7 else {"title": "No data", "summary": ""}
    return render_template("111.html", page_number=111, item=item)

@app.route("/112")
def page_112():
    headlines = get_rte_news()
    item = headlines[8] if len(headlines) > 8 else {"title": "No data", "summary": ""}
    return render_template("112.html", page_number=112, item=item)

@app.route("/113")
def page_113():
    headlines = get_rte_news()
    item = headlines[9] if len(headlines) > 9 else {"title": "No data", "summary": ""}
    return render_template("113.html", page_number=113, item=item)

@app.route("/<int:page_number>")
def fallback_page(page_number):
    placeholder_text = [
        f"Content for page {page_number} not yet implemented.",
        "Check back soon!"
    ]
    return render_template("fallback.html",
                           page_number=page_number,
                           page_title=f"Page {page_number}",
                           content_list=placeholder_text)

@app.route("/160")
def page_160():
    return render_template("160.html", page_number=160)

@app.route("/598")
def page_598():
    url = "https://www.met.ie/Open_Data/json/National.json"
    response = requests.get(url)
    data = response.json()

    forecasts = data.get("forecasts", [])
    current_forecast = forecasts[0] if forecasts else {}
    regions = current_forecast.get("regions", [])

    region_name = ""
    issued_time = ""
    today_text = ""
    tonight_text = ""
    tomorrow_text = ""
    outlook_text = ""

    for obj in regions:
        if "region" in obj:
            region_name = obj["region"]
        elif "issued" in obj:
            issued_time = obj["issued"]
        elif "today" in obj:
            today_text = obj["today"]
        elif "tonight" in obj:
            tonight_text = obj["tonight"]
        elif "tomorrow" in obj:
            tomorrow_text = obj["tomorrow"]
        elif "outlook" in obj:
            outlook_text = obj["outlook"]

    return render_template(
        "598.html",
        page_number=598,
        region_name=region_name,
        issued_time=issued_time,
        today_text=today_text,
        tonight_text=tonight_text,
        tomorrow_text=tomorrow_text,
        outlook_text=outlook_text
    )

if __name__ == "__main__":
    print("Starting Aertel-like teletext Flask server")
    app.run(debug=True, host="0.0.0.0", port=5000)
