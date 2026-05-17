import requests
import xml.etree.ElementTree as ET

NAMESPACE = { "cap" : "urn:oasis:names:tc:emergency:cap:1.2" }

def fetch_alert_xml(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def parse_alert_xml(xml_data):
    root = ET.fromstring(xml_data)
    alert_data = {}
    alert_data["identifier"] = (root.findtext(".//cap:identifier", namespaces=NAMESPACE)).split("-")[1].split("_")[0]
    alert_data["event"] = root.findtext(".//cap:event", namespaces=NAMESPACE)
    alert_data["headline_en"] = root.findtext(".//cap:headline", namespaces=NAMESPACE)
    alert_data["severity"] = root.findtext(".//cap:severity", namespaces=NAMESPACE)
    alert_data["urgency"] = root.findtext(".//cap:urgency", namespaces=NAMESPACE)
    alert_data["certainty"] = root.findtext(".//cap:certainty", namespaces=NAMESPACE)
    alert_data["polygon"] = root.findtext(".//cap:polygon", namespaces=NAMESPACE)
    return alert_data

def fetch_and_parse_alert(url):
    xml_data = fetch_alert_xml(url)
    return parse_alert_xml(xml_data)