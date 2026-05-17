from app.services.feed_fetcher import get_alert_links
from app.services.xml_parser import fetch_and_parse_alert

def ingest_state_alerts(feed_slug):
    links = get_alert_links(feed_slug)
    alerts = []
    for link in links:
        try:
            alert = fetch_and_parse_alert(link)
            alerts.append(alert)
        except Exception as error:
            print(f"Failed to process {link}")
            print(error)
    return alerts