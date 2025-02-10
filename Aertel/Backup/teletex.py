from flask import Flask, render_template, url_for
import feedparser
import datetime

app = Flask(__name__)

# Current RTÉ News RSS feed:
RTE_NEWS_FEED = "https://www.rte.ie/feeds/rss/?index=/news/"

def get_rte_news():
    # Parse feed, return up to e.g. 10 headlines
    feed = feedparser.parse(RTE_NEWS_FEED)
    headlines = []
    if feed.entries:
        for entry in feed.entries[:10]:
            headlines.append({
                "title": entry.title,
                "summary": entry.summary if hasattr(entry, 'summary') else "",
                "link": entry.link
            })
    return headlines

@app.context_processor
def inject_date():
    # Provide a date string in the format: THU 31 JUL 2025
    now = datetime.datetime.now()
    day_of_week = now.strftime("%a").upper()
    day = now.strftime("%d")
    month = now.strftime("%b").upper()
    year = now.strftime("%Y")
    date_string = f"{day_of_week} {day} {month} {year}"
    return {"today_date": date_string}

@app.route("/")
def index_redirect():
    # Redirect to Aertel "index" page which we'll call /100
    return '<html><head><meta http-equiv="refresh" content="0; url=/100" /></head><body></body></html>'

@app.route("/<int:page_number>")
def show_page(page_number):
    if page_number == 100:
        page_title = "Aertel Index"
        # Page 100 simply shows the Ireland.PNG image in page.html
        template_data = {
            "page_number": page_number,
            "page_title": page_title
        }
        return render_template("page.html", **template_data)

    elif page_number == 101:
        page_title = "Headlines / Breaking News"
        news_headlines = get_rte_news()
        template_data = {
            "page_number": page_number,
            "page_title": page_title,
            "headlines": news_headlines
        }
        return render_template("page.html", **template_data)

    elif page_number == 102:
        # Another “National News” page, for now same feed but truncated
        page_title = "National News"
        news_headlines = get_rte_news()
        news_headlines = news_headlines[3:]
        template_data = {
            "page_number": page_number,
            "page_title": page_title,
            "headlines": news_headlines
        }
        return render_template("page.html", **template_data)

    else:
        page_title = f"Page {page_number}"
        placeholder_text = [
            f"Content for page {page_number} not yet implemented.",
            "Check back soon!"
        ]
        template_data = {
            "page_number": page_number,
            "page_title": page_title,
            "content_list": placeholder_text
        }
        return render_template("page.html", **template_data)

if __name__ == "__main__":
    print("Starting Aertel-like teletext Flask server")
    # Accessible to other devices on your network
    app.run(debug=True, host="0.0.0.0", port=5000)
