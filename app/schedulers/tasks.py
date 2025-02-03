from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime
from app.core.config import get_app_settings
import logging

def call_api():
    settings = get_app_settings()
    
    logging.info(f'settings: {settings.host_name}')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Calling API at {now}")
    apis_to_call = [
        {"endpoint": "/api/sample_router/xxx", "params": {"code": "1234"}},
    ]
    
    for api in apis_to_call:
        url = f"http://{settings.host_name}:8080{api['endpoint']}"
        try:
            response = requests.get(url, params=api["params"])
            logging.info(f"Response for {api['params']}: {response.status_code}")
        except Exception as e:
            logging.info(f"Error calling {url}: {e}")

def schedule_jobs():
    scheduler = BackgroundScheduler(timezone='Asia/Taipei')
    # scheduler.add_job(call_api, 'cron', hour=1)
    scheduler.add_job(call_api, 'interval', minutes=1)
    scheduler.start()
