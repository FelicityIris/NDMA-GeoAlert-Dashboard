# NDMA GeoAlert Dashboard
Selectively filtering NDMA Alerts based on Prioritized States

## Requirements
### System Dependencies
- python (v3.14.5)
- python-pip
- python-virtualenv
- mysql (v8.0.46)
### Python Dependencies
```
annotated-types==0.7.0
APScheduler==3.11.2
blinker==1.9.0
certifi==2026.4.22
charset-normalizer==3.4.7
click==8.3.3
feedparser==6.0.12
Flask==3.1.3
greenlet==3.5.0
idna==3.15
isort==8.0.1
itsdangerous==2.2.0
Jinja2==3.1.6
lance-namespace==0.7.7
lance-namespace-urllib3-client==0.7.7
MarkupSafe==3.0.3
numpy==2.4.6
pyarrow==24.0.0
pydantic==2.13.4
pydantic_core==2.46.4
PyMySQL==1.1.3
pyproj==3.7.2
python-dateutil==2.9.0.post0
python-dotenv==1.2.2
requests==2.34.2
sgmllib3k==1.0.0
shapely==2.1.2
six==1.17.0
typing-inspection==0.4.2
typing_extensions==4.15.0
tzlocal==5.3.1
urllib3==2.7.0
Werkzeug==3.1.8
```

## Setup
Clone repository:
```shell
git clone https://github.com/FelicityIris/ndma-alerts-filter
cd ndma-alerts-filter
```
Create Virtual Environment:
```shell
python -m venv venv
source venv/bin/activate
```
Install Python Dependencies:
```shell
pip install -r requirements.txt
```
Configure `.env`:
```.env
# Flask App
FLASK_APP=run.py
FLASK_ENV=development

# Flask Session Key
# Generate using `python -c "import secrets; print(secrets.token_hex(32))"`
SECRET_KEY=<generated_session_key>

# DB Auth
DB_USER=<mysql_user_name>
DB_PASSWORD=<mysql_user_password>
DB_HOST=localhost
DB_NAME=<mysql_database_name>

# Admin Auth
# Generate using `python ./scripts/generate_password_hash.py`
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=<hashed_password>

# Scheduler Config
# Minimum 5 minutes
SCHEDULER_INTERVAL_MINUTES=15
```

## Run
```shell
flask run
```