FYP01-SE-T2430-0112 ENHANCING FACE RECOGNITION ALGORITHM ACCURACY THROUGH PARAMETER OPTIMIZATION FOR ATTENDANCE SYSTEM

# Attendance System with Face Recognition

## Project Overview
This project aims to develop an attendance system that leverages face recognition technology to automate tracking attendance in educational and corporate environments. The system enhances the accuracy of face recognition through parameter optimization.

---

## System Components

### 1. Frontend (User Interface)
- Built using **Django**, providing an intuitive interface for managing attendance.
- Features:
  - User login/logout (Admin, Staff, Student).
  - Dashboard for attendance reports and user management.
  - Real-time attendance tracking with facial recognition.
  - Attendance history and report export functionality.

### 2. Backend (Business Logic & Processing)
- Implemented using **Django**, handling application logic.
- Integrated with PostgreSQL for data management.
- API endpoints for face recognition and attendance processing.

### 3. Face Recognition Module
- Utilizes **OpenCV** and **dlib** for face detection and recognition.
- Optimization techniques used:
  - Grid Search Optimization
  - Random Search Optimization
  - Bayesian Optimization
- Model training and evaluation to improve accuracy.

### 4. Database (PostgreSQL)
- Stores user records (name, student/staff ID, profile image).
- Tracks attendance timestamps.
- Schema to manage roles and permissions.

---

## System Features

### User Roles and Authentication
- **Superadmin/Admin:**
  - Manage user accounts (students, lecturers, staff).
  - View attendance analytics and appointment data.
  - Configure face recognition settings.

- **Student/Staff:**
  - Register attendance via facial recognition.
  - View personal attendance history.

### Attendance Tracking
- Real-time face detection via webcam.
- Automatic attendance marking based on facial recognition.
- Attendance status tracking (present, absent, late).

### Reporting and Analytics
- Generate reports in CSV/PDF formats.
- Insights on attendance trends.
- Search and filter attendance records by date/user.

### Security Measures
- Role-based access control (RBAC).
- Image encryption and secure storage.
- Compliance with GDPR/PDPA for data protection.

---

## New Features Implemented

### 1. Infected Hostels
- Integrated infected hostels within the **Hostels App**.
- Admins can mark specific hostels as quarantine facilities.
- Residents marked **infected** are automatically relocated.

### 2. Automatic Relocation for Infected Residents (Quarantine)
- If a resident tests **positive**, they are relocated to an available **quarantine** room.
- If no quarantine rooms are available, admin intervention is required.
- Residents can only book new appointments after **recovery**.

### 3. Automatic Recovery and Relocation
- If an infected resident has been **infected for more than 2 weeks**, their status changes to **recovered**.
- They are automatically relocated back to their original room.
- The system ensures a smooth transition between **quarantine and normal hostels**.

---

## Research Aspects

### Face Recognition Accuracy Challenges
- Lighting conditions, facial occlusions, pose variations.

### Parameter Optimization Techniques
- Investigating hyperparameter tuning to enhance accuracy.
- Comparing different optimization techniques.

### Performance Evaluation Metrics
- Accuracy, precision, recall, F1-score, execution time.

### Datasets Used
- Publicly available datasets such as:
  - Labeled Faces in the Wild (LFW)
  - CelebA Dataset
  - Custom dataset (collected from users)

---

## Development Roadmap

### Phase 1: System Setup & Database Design
- Install and configure PostgreSQL.
- Set up Django project and authentication.
- Define database schema.

### Phase 2: Face Recognition Integration
- Implement face detection with OpenCV/dlib.
- Develop facial encoding and comparison logic.
- Conduct optimization tests.

### Phase 3: UI/UX Development
- Design frontend for user interactions.
- Integrate attendance logging and real-time feedback.

### Phase 4: Optimization & Testing
- Fine-tune recognition models.
- Conduct system testing in different environments.

### Phase 5: Deployment & Evaluation
- Deploy system locally.
- Evaluate system performance.
- Prepare documentation.

---

## Expected Deliverables
1. A fully functional face recognition-based attendance system.
2. Optimized face recognition model with enhanced accuracy.
3. Research findings on parameter optimization.
4. Comprehensive project documentation.

---

## Tools & Technologies
- **Programming Language:** Python
- **Framework:** Django (full-stack)
- **Face Recognition:** OpenCV, dlib
- **Database:** PostgreSQL
- **UI Technologies:** Django templates, Bootstrap
- **Version Control:** GitHub
- **Deployment:** Local (XAMPP), Future Cloud Deployment (AWS, Azure)

---

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/attendance_system.git
   cd attendance_system
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure PostgreSQL database in `settings.py`.
5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```
8. Run the cron job:
   ```bash
   python schedule_task.py
   ```
---

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue for improvements.

---

## License
This project is licensed under the MIT License.

