import requests
import xml.etree.ElementTree as ET

NAMESPACE = { "cap" : "urn:oasis:names:tc:emergency:cap:1.2" }

def fetch_alert_xml(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def fetch_polygon_xml(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def parse_polygon_xml(xml_data):
    root = ET.fromstring(xml_data)
    polygons = []
    polygon_elements = root.findall(".//polygon")
    for polygon_element in polygon_elements:
        polygon_text = polygon_element.text
        if polygon_text:
            polygons.append(polygon_text.strip())
    return polygons

def extract_polygon_url(root):
    parameters = root.findall(".//cap:parameter", namespaces=NAMESPACE)
    for parameter in parameters:
        value_name = parameter.findtext("cap:valueName", namespaces=NAMESPACE)
        value = parameter.findtext("cap:value", namespaces=NAMESPACE)
        if value_name == "Polygon URL":
            return value
    return None

def parse_alert_xml(xml_data):
    root = ET.fromstring(xml_data)
    
    alert_data = {}
    alert_data["identifier"] = (root.findtext(".//cap:identifier", namespaces=NAMESPACE)).split("-")[1].split("_")[0]
    alert_data["event"] = root.findtext(".//cap:event", namespaces=NAMESPACE)
    alert_data["headline_en"] = root.findtext(".//cap:headline", namespaces=NAMESPACE)
    alert_data["severity"] = root.findtext(".//cap:severity", namespaces=NAMESPACE)
    alert_data["urgency"] = root.findtext(".//cap:urgency", namespaces=NAMESPACE)
    alert_data["certainty"] = root.findtext(".//cap:certainty", namespaces=NAMESPACE)
    
    polygon_url = extract_polygon_url(root)
    polygons = []
    if polygon_url:
        try:
            polygon_xml = fetch_polygon_xml(polygon_url)
            polygons = parse_polygon_xml(polygon_xml)
        except Exception as error:
            print(f"Failed to fetch polygon: {polygon_url}")
            print(error)
    alert_data["polygons"] = polygons

    return alert_data

def fetch_and_parse_alert(url):
    xml_data = fetch_alert_xml(url)
    return parse_alert_xml(xml_data)