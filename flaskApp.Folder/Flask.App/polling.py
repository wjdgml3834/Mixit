import requests
import datetime
from dateutil.relativedelta import relativedelta
import cache
import app_config

def parse_iso_datetime(iso_str):
    iso_str = iso_str.rstrip('Z')
    if '.' in iso_str:
        parts = iso_str.split('.')
        iso_str = parts[0] + '.' + parts[1][:6]
    return datetime.datetime.fromisoformat(iso_str)

def is_significant_change(created_time, modified_time):

    time_diff = modified_time - created_time

    return time_diff.total_seconds() >= 5

def get_updated_events():
    token = cache._get_token_from_cache(app_config.SCOPE)
    if not token:
        return None

    last_checked = (datetime.datetime.utcnow() - relativedelta(months=1)).isoformat() + 'Z'
    current_time = datetime.datetime.utcnow().isoformat() + 'Z'

    endpoint = app_config.ENDPOINT.format(current_datetime=last_checked, end_datetime=current_time)
    headers = {'Authorization': 'Bearer ' + token['access_token']}
    response = requests.get(endpoint, headers=headers)
    current_events = response.json().get('value', [])

    updated_events = []
    for event in current_events:
        created_time = parse_iso_datetime(event['createdDateTime'])
        modified_time = parse_iso_datetime(event['lastModifiedDateTime'])

        if created_time != modified_time and is_significant_change(created_time, modified_time):
            updated_events.append(event)

    return updated_events