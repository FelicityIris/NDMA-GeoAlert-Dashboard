import time
from app.services.state_service import get_selected_states
from app.services.feed_fetcher import ( get_alert_links, extract_identifer_from_link )
from app.services.xml_parser import fetch_and_parse_alert
from app.services.alert_service import ( save_alert, delete_expired_alerts, alert_exists, is_alert_expired )

REUQEST_DELAY_SECONDS = 0.5

def ingest_alerts():
    selected_states = get_selected_states()

    for state in selected_states:
        state_id = state["state_id"]
        feed_slug = state["feed_slug"]
        try:
            alert_links = get_alert_links(feed_slug)

            if alert_links is None:
                continue

            for link in alert_links:
                try:
                    identifier = extract_identifer_from_link(link)
                    if alert_exists(identifier):
                        print(f"Skipping existing alert: {identifier}")
                        time.sleep(REUQEST_DELAY_SECONDS)
                        continue
                    alert_data = fetch_and_parse_alert(link)
                    if is_alert_expired(alert_data):
                        print(f"Skipping expired alert: {alert_data['identifier']}")
                        time.sleep(REUQEST_DELAY_SECONDS)
                        continue
                    save_alert(alert_data, state_id)
                    print(f"Saved alert: {alert_data['identifier']}")
                    time.sleep(REUQEST_DELAY_SECONDS)
                except Exception as error:
                    print(f"Failed alert: {link}")
                    print(error)
        except Exception as error:
            print(f"Failed feed: {feed_slug}")
            print(error)
    
    delete_expired_alerts()
    print("Alert ingestion complete.")