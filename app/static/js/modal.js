function renderAlertModal(alert) {
    const modal_body = document.getElementById("modal-body");

    modal_body.innerHTML = `
        <h2>${alert.event}</h2>
        <div class="alert-headline-box">
            ${alert.headline_en ?? ""}
        </div>

        <div class="alert-detail-grid">
            <div class="detail-item">
                <label>Severity</label>
                <span>${alert.severity}</span>
            </div>

            <div class="detail-item">
                <label>Urgency</label>
                <span>${alert.urgency}</span>
            </div>

            <div class="detail-item">
                <label>Certainty</label>
                <span>${alert.certainty}</span>
            </div>
        </div>
    `;
}

document.querySelectorAll(".project-alert-item").forEach((button) => {
    button.addEventListener("click", async () => {
        const alert_id = button.dataset.alertId;
        const response = await fetch(`/alert/${alert_id}`);
        const alert = await response.json();
        renderAlertModal(alert);
        document.getElementById("alert-modal").classList.add("open");
    });
});

document.getElementById("close-modal").addEventListener("click", () => {
    document.getElementById("alert-modal").classList.remove("open");
});

document.getElementById("alert-modal").addEventListener("click", (event) => {
    if (event.target.id === "alert-modal") {
        event.target.classList.remove("open");
    }
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") document.getElementById("alert-modal").classList.remove("open");
});
