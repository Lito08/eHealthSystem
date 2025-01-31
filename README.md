📌 eHealth System

A Django-based system for managing COVID-19 quarantine tracking, appointments, and health monitoring for MMU residents.

---

## Features Implemented

### ✅ Infected Hostels
- Integrated infected hostels into the **Hostels App**.
- Admins can mark specific hostels as quarantine facilities.
- Residents marked **infected** are automatically relocated to quarantine rooms.

### ✅ Automatic Relocation for Infected Residents (Quarantine)
- If a resident tests **positive**, they are automatically relocated to an available **quarantine** room.
- If no quarantine rooms are available, admin intervention is required.
- Residents can only book new appointments after **recovery**.

### ✅ Automatic Recovery and Relocation
- If an infected resident has been **infected for more than 2 weeks**, their status changes to **recovered**.
- They are automatically relocated back to their original room.
- The system ensures a smooth transition between **quarantine and normal hostels**.

---

🤟 ## Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-repo/eHealthSystem.git
cd eHealthSystem
```

### 2️⃣ Create and activate a virtual environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3.1️⃣ Install CMake (Required for some dependencies)
```bash
https://cmake.org
```

---

🏢 ## Database Setup

### 4️⃣ Apply database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a superadmin (for initial setup)
```bash
python manage.py createsuperuser
```
Enter your username, email, and password when prompted.

---

🚀 ## Running the Application

### 6️⃣ Start the Django server
```bash
python manage.py runserver
```
Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

📁 ## Handling Static Files

To collect static files (for production environments):
```bash
python manage.py collectstatic --noinput
```

---

⏳ ## Running the Cron Job (Task Scheduler)

To ensure automatic updates for appointment status:
```bash
python manage.py schedule_task.py
```
Add it to a task scheduler (like Windows Task Scheduler or cron for Linux).

---

🔑 ## API Keys
- **Google Maps API Key** → Required for Hotspots mapping.
- **Email SMTP Config** → Required for email notifications.

Ensure API keys are set in `.env` before running the project!

---

🛠 ## Technologies Used
- **Django 5.1**
- **SQLite (Default, supports PostgreSQL)**
- **Bootstrap 5**
- **Google Maps API**
- **Django-Cron for scheduled tasks**
- **Chart.js for visual analytics**

---

📞 ## Support
If you encounter any issues, please open an issue in the repository.

