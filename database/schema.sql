CREATE DATABASE IF NOT EXISTS ndma_alerts_db;

USE ndma_alerts_db;

CREATE TABLE IF NOT EXISTS states (
    state_id INT PRIMARY KEY AUTO_INCREMENT,
    state_name VARCHAR(100) NOT NULL UNIQUE,
    feed_slug VARCHAR(100) NOT NULL UNIQUE,
    is_selected BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS districs (
    district_code INT PRIMARY KEY,
    district_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id BIGINT PRIMARY KEY AUTO_INCREMENT,
	
    alert_identifier VARCHAR(100) NOT NULL UNIQUE,
	
    state_id INT NOT NULL,
	
    event VARCHAR(255),
	
    headline_en TEXT,
    headline_alt TEXT,
	
    urgency ENUM(
        'Immediate',
        'Expected',
        'Future',
        'Past',
        'Unknown'
    ),
	
    severity ENUM(
        'Extreme',
        'Severe',
        'Moderate',
        'Minor',
        'Unknown'
    ),
	
    certainty ENUM(
        'Observed',
        'Likely',
        'Possible',
        'Unlikely',
        'Unknown'
    ),
	
    effective DATETIME,
    onset DATETIME,
    expires DATETIME,
	
    polygon TEXT,
	
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	
    FOREIGN KEY (state_id)
        REFERENCES states(state_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS alert_districts (
    alert_id BIGINT NOT NULL,
    district_code INT NOT NULL,
    PRIMARY KEY (
        alert_id,
        district_code
    ),
    FOREIGN KEY (alert_id)
        REFERENCES alerts(alert_id)
        ON DELETE CASCADE,
    FOREIGN KEY (district_code)
        REFERENCES districs(district_code)
        ON DELETE CASCADE
);