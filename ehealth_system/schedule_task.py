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

# Schedule the task every 10 minutes
schedule.every(10).minutes.do(run_update_appointments)

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
