
from apscheduler.schedulers.blocking import BlockingScheduler


scheduler = BlockingScheduler()
scheduler.add_job(parse_data, 'interval', minutes=1)
scheduler.start()