import os
import feedparser
from jinja2 import Environment, FileSystemLoader

# === CONFIG ===

NEWS_FEEDS = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://www.theverge.com/rss/index.xml",
    "https://www.engadget.com/rss.xml",
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "https://www.techradar.com/rss"
]

DEAL_FEEDS = [
    "https://slickdeals.net/newsearch.php?mode=popdeals&searcharea=deals&rss=1",
    "https://www.reddit.com/r/buildapcsales/.rss",
    "https://9to5toys.com/feed/",
    "https://www.dealnews.com/rss.html",
    "https://www.kotaku.com/deals/rss"
]

AMAZON_ASSOCIATE_TAG = "thegadgetgobl-20"

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "../templates")
OUTPUT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index.html"))

# === FUNCTIONS ===

def fetch_combined_entries(feed_urls, max_total=5):
    combined = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            combined.extend(feed.entries)
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
    # Sort by publish time if available
    combined = sorted(combined, key=lambda x: x.get("published_parsed", None), reverse=True)
    return combined[:max_total]

def main():
    news = fetch_combined_entries(NEWS_FEEDS, max_total=5)
    deals = fetch_combined_entries(DEAL_FEEDS, max_total=5)

    print(f"Fetched {len(news)} news articles")
    print(f"Fetched {len(deals)} deals")

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("template.html")

    # Add Amazon tag and clean links if needed
    for d in deals:
        if "amazon.com" in d.link:
            clean_link = d.link.split("ref=")[0].split("?")[0]
            d.link = f"{clean_link}?tag={AMAZON_ASSOCIATE_TAG}"

    html = template.render(news=news, deals=deals)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
