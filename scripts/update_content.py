import os
import feedparser
from jinja2 import Environment, FileSystemLoader

# === CONFIG ===
NEWS_RSS_URL = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
AMAZON_DEALS_RSS_URL = "https://www.amazon.com/gp/rss/bestsellers/electronics/ref=zg_bs_e_1_rss"
AMAZON_ASSOCIATE_TAG = "your-amazon-tag"  # Replace this with your real Amazon affiliate tag

# File paths
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "../templates")
OUTPUT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index.html"))

# === FUNCTIONS ===

def fetch_feed(url):
    return feedparser.parse(url).entries

def main():
    news = fetch_feed(NEWS_RSS_URL)[:5]
    deals = fetch_feed(AMAZON_DEALS_RSS_URL)[:5]

    # Print debug info
    print(f"Fetched {len(news)} news articles")
    print(f"Fetched {len(deals)} deals")

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("template.html")

  # Attach Amazon affiliate tag to each deal link
deals = [
    {**deal, "link": f"{deal.link}?tag=thegadgetgobl-20"}
    for deal in deals
]

    html = template.render(news=news, deals=deals)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
