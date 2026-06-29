# 🏥 Hospital Management System API

A RESTful Hospital Management System built with **Django**, **Django REST Framework**, and **JWT Authentication**. The API supports role-based access control for patients, doctors, nurses, and administrators, allowing secure management of appointments and medical records.

---

## Features

* JWT Authentication
* Role-based authorization
* Patient appointment booking
* Doctor appointment management
* Automatic medical record generation after appointment completion
* Role-based medical record access
* Swagger/OpenAPI documentation
* Comprehensive automated tests

---

## Tech Stack

* Python 3.11
* Django 5
* Django REST Framework
* MySQL
* SimpleJWT
* drf-spectacular (Swagger/OpenAPI)

---

## User Roles

| Role    | Permissions                                                             |
| ------- | ----------------------------------------------------------------------- |
| Admin   | Full access to all appointments and medical records                     |
| Patient | Book appointments and view own medical records                          |
| Doctor  | View assigned appointments, update appointment status, create diagnoses |
| Nurse   | View assigned appointments and medical records                          |

---

## Project Structure

```
hospitalmgmt/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── permissions.py
│
├── hospital/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── admin.py
│
├── records/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── admin.py
│
├── config/
│   └── settings.py
│
└── manage.py
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/hospital-management-api.git
cd hospital-management-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your MySQL database in `settings.py`.

Run migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

---

## Authentication

Obtain JWT tokens:

```
POST /api/token/
```

Refresh access token:

```
POST /api/token/refresh/
```

Include the access token in every authenticated request:

```
Authorization: Bearer <access_token>
```

---

## API Endpoints

### Authentication

| Method | Endpoint              |
| ------ | --------------------- |
| POST   | `/api/token/`         |
| POST   | `/api/token/refresh/` |
| GET    | `/api/profile/`       |

---

### Appointments

| Method | Endpoint                  | Description                                         |
| ------ | ------------------------- | --------------------------------------------------- |
| GET    | `/api/appointments/`      | List appointments visible to the authenticated user |
| POST   | `/api/appointments/`      | Patient creates appointment                         |
| PATCH  | `/api/appointments/<id>/` | Assigned doctor updates appointment                 |

---

### Medical Records

| Method | Endpoint             |
| ------ | -------------------- |
| GET    | `/api/records/`      |
| GET    | `/api/records/<id>/` |

---

## Business Rules

* Patients can create appointments.
* Doctors can update only their assigned appointments.
* Nurses have read-only access.
* Admins have unrestricted access.
* Medical records are automatically created when an appointment status changes from **PENDING** to **COMPLETED**.
* Patients can view only their own medical records.
* Doctors and nurses can view records only for appointments assigned to them.

---

## API Documentation

Swagger UI:

```
https://hospitalmgmt-qyc6.onrender.com/api/docs/
```

ReDoc:

```
https://hospitalmgmt-qyc6.onrender.com/api/redoc/
```

OpenAPI Schema:

```
https://hospitalmgmt-qyc6.onrender.com/api/schema/
```

---

## Running Tests

Run all tests:

```bash
python manage.py test
```

Run individual app tests:

```bash
python manage.py test accounts
python manage.py test hospital
python manage.py test records
```

---

## License

This project is for learning and portfolio purposes.
