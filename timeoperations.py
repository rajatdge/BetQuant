import datetime, time

def get_current_time():
  dts = datetime.datetime.utcnow()
  current_time = round(time.mktime(dts.timetuple()) + dts.microsecond/1e6)
  return current_time
