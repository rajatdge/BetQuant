import datetime, time, calendar

def get_current_time_in_unix_utc():
  return int(time.time())

def get_six_hours_before_time_utc(current_time):
     return int(current_time - 6 * 60 * 60)

def get_one_hour_before_time_utc(current_time):
    return int(current_time - 1 * 60 * 60)

def convert_str_to_unix_time_utc(match_date_time):
    return calendar.timegm(time.strptime(match_date_time, '%d-%m-%Y %H:%M:%S'))

def convert_from_unix_to_str_date_time_utc(match_time):
    return datetime.datetime.utcfromtimestamp(match_time).strftime('%d-%m-%Y')
