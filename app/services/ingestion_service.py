import time

from app.services.alert_service import (
    alert_exists,
    delete_expired_alerts,
    is_alert_expired,
    save_alert,
)
from app.services.feed_fetcher import extract_identifer_from_link, get_alert_links
from app.services.state_service import get_selected_states
from app.services.warning_service import refresh_warnings
from app.services.xml_parser import fetch_and_parse_alert

REQUEST_DELAY_SECONDS = 1


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
                        time.sleep(REQUEST_DELAY_SECONDS)
                        continue
                    alert_data = fetch_and_parse_alert(link)
                    if is_alert_expired(alert_data):
                        print(f"Skipping expired alert: {alert_data['identifier']}")
                        time.sleep(REQUEST_DELAY_SECONDS)
                        continue
                    save_alert(alert_data, state_id)
                    print(f"Saved alert: {alert_data['identifier']}")
                    time.sleep(REQUEST_DELAY_SECONDS)
                except Exception as error:
                    print(f"Failed alert: {link}")
                    print(error)
        except Exception as error:
            print(f"Failed feed: {feed_slug}")
            print(error)

    delete_expired_alerts()
    print("Alert ingestion complete.")

    refresh_warnings()
    print("New alerts generated.")
