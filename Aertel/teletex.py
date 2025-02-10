from flask import Flask, render_template, url_for
import feedparser
import datetime

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

@app.context_processor
def inject_date():
    now = datetime.datetime.now()
    day_of_week = now.strftime("%a").upper()
    day = now.strftime("%d")
    month = now.strftime("%b").upper()
    year = now.strftime("%Y")
    date_string = f"{day_of_week} {day} {month} {year}"
    return {"today_date": date_string}

@app.route("/")
def index_redirect():
    # Re-route to page 100 (index)
    return '<html><head><meta http-equiv="refresh" content="0; url=/100" /></head><body></body></html>'

@app.route("/100")
def page_100():
    return render_template("100.html", page_number=100)

@app.route("/101")
def page_101():
    headlines = get_rte_news()
    # This page might show multiple headlines as you already did in 101.html
    return render_template("101.html", page_number=101, headlines=headlines)

@app.route("/102")
def page_102():
    headlines = get_rte_news()
    # Possibly show the tail of the feed
    headlines = headlines[3:]
    return render_template("102.html", page_number=102, headlines=headlines)

# Now the single-item pages: 104..113
@app.route("/104")
def page_104():
    headlines = get_rte_news()
    item = headlines[0] if len(headlines) > 0 else {"title":"No data","summary":""}
    return render_template("104.html", page_number=104, item=item)

@app.route("/105")
def page_105():
    headlines = get_rte_news()
    item = headlines[1] if len(headlines) > 1 else {"title":"No data","summary":""}
    return render_template("105.html", page_number=105, item=item)

@app.route("/106")
def page_106():
    headlines = get_rte_news()
    item = headlines[2] if len(headlines) > 2 else {"title":"No data","summary":""}
    return render_template("106.html", page_number=106, item=item)

@app.route("/107")
def page_107():
    headlines = get_rte_news()
    item = headlines[3] if len(headlines) > 3 else {"title":"No data","summary":""}
    return render_template("107.html", page_number=107, item=item)

@app.route("/108")
def page_108():
    headlines = get_rte_news()
    item = headlines[4] if len(headlines) > 4 else {"title":"No data","summary":""}
    return render_template("108.html", page_number=108, item=item)

@app.route("/109")
def page_109():
    headlines = get_rte_news()
    item = headlines[5] if len(headlines) > 5 else {"title":"No data","summary":""}
    return render_template("109.html", page_number=109, item=item)

@app.route("/110")
def page_110():
    headlines = get_rte_news()
    item = headlines[6] if len(headlines) > 6 else {"title":"No data","summary":""}
    return render_template("110.html", page_number=110, item=item)

@app.route("/111")
def page_111():
    headlines = get_rte_news()
    item = headlines[7] if len(headlines) > 7 else {"title":"No data","summary":""}
    return render_template("111.html", page_number=111, item=item)

@app.route("/112")
def page_112():
    headlines = get_rte_news()
    item = headlines[8] if len(headlines) > 8 else {"title":"No data","summary":""}
    return render_template("112.html", page_number=112, item=item)

@app.route("/113")
def page_113():
    headlines = get_rte_news()
    item = headlines[9] if len(headlines) > 9 else {"title":"No data","summary":""}
    return render_template("113.html", page_number=113, item=item)

# For any other page not implemented
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

if __name__ == "__main__":
    print("Starting Aertel-like teletext Flask server")
    # Host on 0.0.0.0 so other devices on LAN can access
    app.run(debug=True, host="0.0.0.0", port=5000)
