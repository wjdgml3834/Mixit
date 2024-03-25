from dateutil import parser
import pytz

def to_local_timezone(utc_datetime, local_timezone):
    local_tz = pytz.timezone(local_timezone)
    return utc_datetime.astimezone(local_tz)

def format_start_date(value, local_timezone='Europe/Amsterdam'):
    utc_date_time = parser.parse(value)
    utc_date_time = utc_date_time.replace(tzinfo=pytz.utc)  
    local_date_time = to_local_timezone(utc_date_time, local_timezone)
    return local_date_time.strftime('%d-%m-%Y')

def format_start_time(value, local_timezone='Europe/Amsterdam'):
    utc_date_time = parser.parse(value)
    utc_date_time = utc_date_time.replace(tzinfo=pytz.utc)  
    local_date_time = to_local_timezone(utc_date_time, local_timezone)
    return local_date_time.strftime('%H:%M')

def format_end_time(value, local_timezone='Europe/Amsterdam'):
    utc_date_time = parser.parse(value)
    utc_date_time = utc_date_time.replace(tzinfo=pytz.utc)  
    local_date_time = to_local_timezone(utc_date_time, local_timezone)
    return local_date_time.strftime('%H:%M')
