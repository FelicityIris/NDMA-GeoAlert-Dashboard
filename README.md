# NDMA Alerts Filter
Selectively filtering NDMA Alerts based on Prioritized States

## Requirements
### System Dependencies
- python (v3.14.5)
- python-pip
- python-virtualenv
- mysql (v8.0.46)
### Python Dependencies
```
blinker==1.9.0
certifi==2026.4.22
charset-normalizer==3.4.7
click==8.3.3
Flask==3.1.3
Flask-SQLAlchemy==3.1.1
greenlet==3.5.0
idna==3.15
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
PyMySQL==1.1.3
python-dotenv==1.2.2
requests==2.34.2
SQLAlchemy==2.0.49
typing_extensions==4.15.0
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
SESSION_KEY=<generated_session_key>

# DB Auth
DB_USER=<mysql_user_name>
DB_PASSWORD=<mysql_user_password>
DB_HOST=localhost
DB_NAME=<mysql_database_name>
```

## Run
```shell
flask run
```