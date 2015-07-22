#! /usr/bin/env python3

from datetime import datetime
from apscheduler.schedulers import AsyncIOScheduler

def job():
    print(datetime.now())

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, "interval", seconds=3)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
