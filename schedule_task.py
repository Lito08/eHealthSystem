import schedule
import time
import subprocess
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ehealth_system.settings")
django.setup()

def run_update_appointments():
    print("Running update_appointments command...")
    subprocess.run(["python", "manage.py", "update_appointments"], check=True)

def run_mark_recovered():
    print("Running mark_recovered command...")
    subprocess.run(["python", "manage.py", "mark_recovered"], check=True)

# Schedule the tasks
schedule.every(10).minutes.do(run_update_appointments)  # Check every 10 minutes for past appointments
schedule.every().day.at("00:00").do(run_mark_recovered)  # Run mark_recovered at midnight

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(10)  # Check every minute
