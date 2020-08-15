from flask import Flask, request, render_template
import feedparser
import json

app = Flask(__name__)
app.config.from_object('config.Config')

#404 error handler
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


#This page will be automatically rendered when an exception is encountered 
@app.errorhandler(Exception)
def handle_exception(exception):
    return render_template('exception.html', exception="Opps something went wrong")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        feed = feedparser.parse(request.form['rss_url'])
        feed_title = feed['feed']['title']
        feed_entries = feed.entries
        processed_feeds = []
        for entry in feed.entries:
            item = {
                "article_title": entry.title,
                "article_link": entry.link,
                "article_description": entry.description,
                "article_published_at": entry.published[:16],
                "article_published_at_parsed": entry.published_parsed
            }
            processed_feeds.append(item)
        return render_template('index.html', feeds=processed_feeds, title=feed_title)
    else:
        return render_template('index.html', feeds=[], title="")


if __name__ == "__main__":
    app.run(debug=True)
