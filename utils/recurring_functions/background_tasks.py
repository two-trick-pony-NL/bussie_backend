from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

"""
The functions underneath are triggered from the main script. 
Each is triggered at a specific interval and we can run code at these intervals for housekeeping. 
"""

def Every_minute():
    print("1 Mintute - the time is")
    print(current_time)

def Every_fifteen_minutes():
    print("15 Minutes - the time is")
    print(current_time)

def Every_hour():
    print("1 hour  - the time is")
    print(current_time)

def Every_day():
    print("1 day  - the time is")
    print(current_time)


