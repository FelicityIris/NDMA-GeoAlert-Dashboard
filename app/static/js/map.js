const map = L.map("map").setView([22.9734, 78.6569], 5);
const polygon_layers = {};
let active_layers = [];

L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    { attribution: "&copy; OpenStreetMap contributors" }
).addTo(map)

const parse_polygon = (polygon_string) => {
    return polygon_string.trim().split(" ").map((coordinate_pair) => {
        const [lat, lng] = coordinate_pair.split(",").map(Number);
        return [lat, lng];
    });
}

polygon_data.forEach((alert) => {
    if (!alert.polygons) { return; }

    polygon_layers[alert.alert_id] = [];

    let polygon_color = "";
    if (alert.severity === "Extreme") polygon_color = "black";
    else if (alert.severity === "Severe") polygon_color = "red";
    else if (alert.severity === "Moderate") polygon_color = "orange";
    else if (alert.severity === "Minor") polygon_color = "yellow";
    else polygon_color = "#3388ff";

    console.log(alert.severity);

    alert.polygons.forEach((polygon) => {
        try {
            const coordinates = parse_polygon(polygon);
            const polygon_layer = L.polygon(coordinates, { weight: 2, color: polygon_color, opacity: 0.8, fillOpacity: 0.2 }).addTo(map);
            polygon_layers[alert.alert_id].push(polygon_layer);
        } catch (error) {
            console.error("Polygon parse failed:", error);
        }
    });
});

document.querySelectorAll(".alert-card").forEach((card) => {
    card.addEventListener(
        "click",
        () => {
            const alert_id = card.dataset.alertId;
            const layers = polygon_layers[alert_id];

            if (!layers) { return; }

            active_layers.forEach((layer) => {
                layer.setStyle({ weight: 2, fillOpacity: 0.2 });
            });
            active_layers = [];
            
            layers.forEach((layer) => {

                layer.setStyle({ weight: 4, fillOpacity: 0.4 });
                active_layers.push(layer);
                map.fitBounds(layer.getBounds());
            });
        }
    );
});

