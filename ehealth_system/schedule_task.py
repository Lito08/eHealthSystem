import schedule
import time
import subprocess
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ehealth_system.settings")
django.setup()

def run_update_appointments():
    """Runs the update_appointments command to mark past appointments as Completed."""
    print("Running update_appointments command...")
    try:
        subprocess.run(["python", "manage.py", "update_appointments"], check=True)
        print("Successfully updated past appointments.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating appointments: {e}")

def run_mark_recovered():
    """Runs the mark_recovered command to mark residents as recovered after 2 weeks."""
    print("Running mark_recovered command...")
    try:
        subprocess.run(["python", "manage.py", "mark_recovered"], check=True)
        print("Successfully marked recovered residents and relocated them.")
    except subprocess.CalledProcessError as e:
        print(f"Error marking recovered residents: {e}")

# Schedule tasks
schedule.every(10).minutes.do(run_update_appointments)  # Update past appointments every 10 minutes
schedule.every().day.at("00:00").do(run_mark_recovered)  # Run recovery process at midnight

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(15)  # Check every minute
