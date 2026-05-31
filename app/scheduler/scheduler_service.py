import os

from apscheduler.schedulers.background import BackgroundScheduler

from app.services.ingestion_service import ingest_alerts

SCHEDULER_INTERVAL_MINUTES = max(5, int(os.getenv("SCHEDULER_INTERVAL_MINUTES", "15")))


def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        ingest_alerts,
        trigger="interval",
        minutes=SCHEDULER_INTERVAL_MINUTES,
        id="alert_ingestion",
        replace_existing=True,
        max_instances=1
    )

    scheduler.start()

    print(f"Scheduler started @ {SCHEDULER_INTERVAL_MINUTES} minute interval.")
