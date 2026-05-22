const map = L.map("map").setView([22.9734, 78.6569], 5);

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

    alert.polygons.forEach((polygon) => {
        try {
            const coordinates = parse_polygon(polygon);
            L.polygon(coordinates, { weight: 2, opacity: 0.8, fillOpacity: 0.2 }).addTo(map);
        } catch (error) {
            console.error("Polygon parse failed:", error);
        }
    });
});