import feedparser

RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss"
]
RSS_FEEDS_URLS = [
    # "http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/technology/rss.xml",
    # "http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/front_page/rss.xml",
    "https://feeds.bbci.co.uk/polska/rss.xml",
    # "http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/business/rss.xml"
]

RSS_FEEDS_URLS_2 = [
    # "https://www.rp.pl/rss/aktualnosci.xml",
    # "https://www.rp.pl/rss/gospodarka.xml",
    # "https://www.rp.pl/rss/opinie.xml",
    "https://www.rp.pl/rss_main",
    # "https://www.rp.pl/rss/finanse.xml"
]


def get_image_url(entry):
    for link in entry.get("links", []):
        if link.get("type")[:5] == "image":
            return link.get("href")
    return None


def fetch_rss_articles():
    articles = []

    for feed_url in RSS_FEEDS_URLS_2:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:

            articles.append({
                "title": entry.title,
                "url": entry.link,
                "published": entry.get("published", None),
                "source": feed.feed.title,
                "img_url": get_image_url(entry),
            })

    return articles
