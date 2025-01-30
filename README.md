📌 eHealth System

A Django-based system for managing COVID-19 quarantine tracking, appointments, and health monitoring for MMU residents.

🔧 Installation & Setup

1️⃣ Clone the repository

git clone https://github.com/your-repo/eHealthSystem.git

cd eHealthSystem

2️⃣ Create and activate a virtual environment

# On Windows

python -m venv venv

venv\Scripts\activate

# On macOS/Linux

python3 -m venv venv

source venv/bin/activate

3️⃣ Install dependencies

pip install -r requirements.txt

⚙️ Database Setup

4️⃣ Apply database migrations

python manage.py makemigrations

python manage.py migrate

5️⃣ Create a superadmin (for initial setup)

python manage.py createsuperuser

Enter your username, email, and password when prompted.

🚀 Running the Application

6️⃣ Start the Django server

python manage.py runserver

Access the app at http://127.0.0.1:8000/.

📁 Handling Static Files

To collect static files (for production environments):

python manage.py collectstatic --noinput

⏳ Running the Cron Job (Task Scheduler)

To ensure automatic updates for appointment status:

python manage.py schedule_task.py

Add it to a task scheduler (like Windows Task Scheduler or cron for Linux).

🔑 API Keys

Google Maps API Key → Required for Hotspots mapping.

Email SMTP Config → Required for email notifications.

Ensure API keys are set in .env before running the project!

📜 Features

✅ Admin Panel – Manage users, hostels, and appointments.

✅ Resident Dashboard – View health risk reports & infected status.

✅ Appointment System – Schedule, cancel, and track clinic visits.

✅ COVID-19 Hotspot Mapping – View and report high-risk areas.

✅ Announcements System – Superadmin/Admins can post health alerts.

✅ Terms & Conditions – Manage legal policies in the system.

🛠 Technologies Used

Django 5.1

SQLite (Default, supports PostgreSQL)

Bootstrap 5

Google Maps API

Django-Cron for scheduled tasks

Chart.js for visual analytics

📞 Support

If you encounter any issues, please open an issue in the repository.