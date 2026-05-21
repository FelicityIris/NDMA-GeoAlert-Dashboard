import feedparser
from app.services.http_client import session
from urllib.parse import ( urlparse, parse_qs )

BASE_RSS_URL = "https://sachet.ndma.gov.in/cap_public_website/rss/"

def generate_feed_url(feed_slug):
    return f"{BASE_RSS_URL}rss_{feed_slug}.xml"

def fetch_rss_feed(feed_slug):
    url = generate_feed_url(feed_slug)
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def extract_alert_links(rss_data):
    parsed_feed = feedparser.parse(rss_data)
    links = []
    for entry in parsed_feed.entries:
        link = entry.get("link")
        if link:
            links.append(link)
    return links

def get_alert_links(feed_slug):
    rss_data = fetch_rss_feed(feed_slug)
    return extract_alert_links(rss_data)

def extract_identifer_from_link(link):
    parsed_url = urlparse(link)
    query_params = parse_qs(parsed_url.query)
    identifier = query_params.get("identifier", [None])[0]
    return identifier