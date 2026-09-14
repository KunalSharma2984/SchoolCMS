# Student Course & Assignment Management System

A full-featured Django web application for managing students, teachers, courses, assignments, submissions, and grades.

---

## Tech Stack

- **Backend**: Python 3.10+, Django 4.2
- **Database**: SQLite (default) — easy to swap to PostgreSQL
- **Frontend**: Plain HTML + CSS (no heavy framework)
- **Auth**: Django built-in authentication with custom user roles

---

## User Roles & Features

| Role    | Capabilities |
|---------|-------------|
| Student | Enroll in courses, view assignments, submit assignments, view grades |
| Teacher | Create courses, create assignments, view submissions, grade students |
| Admin   | Manage students, teachers, and courses via Django admin + custom UI |

---

## Project Structure

```
django_project/
├── manage.py
├── requirements.txt
├── .env.example
├── school_cms/               ← Django project settings package
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                 ← Custom user model + auth views
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── courses/                  ← Courses, assignments, submissions, grades
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── templates/
│   ├── base.html
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
│   └── courses/
│       ├── course_list.html
│       ├── course_detail.html
│       ├── assignment_detail.html
│       ├── submission_list.html
│       └── grade_form.html
└── static/
    └── css/
        └── style.css
```

---

## Setup & Run (Step by Step)

### 1. Prerequisites

Make sure you have Python 3.10+ installed:
```bash
python --version
```

### 2. Clone / Download the project

```bash
cd wherever-you-want
# if using git:
git clone <repo-url> django_project
cd django_project
```

### 3. Create a virtual environment

```bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set up environment variables

```bash
cp .env.example .env
# Open .env and set a SECRET_KEY (any random string is fine for development)
```

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create a superuser (Admin account)

```bash
python manage.py createsuperuser
# Follow the prompts — this gives you admin access
```

### 8. (Optional) Load sample data

```bash
python manage.py loaddata sample_data.json
```

### 9. Run the development server

```bash
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000**

---

## Default Admin Panel

Visit **http://127.0.0.1:8000/admin** and log in with your superuser credentials to manage everything directly.

---

## Quick Account Setup (Manual)

1. Go to `/register/` and create accounts
2. Log in to `/admin/` as superuser
3. Edit the user and set their **role** to `student`, `teacher`, or `admin`
4. Log back in as that user to see their dashboard

---

## Database (Switch to PostgreSQL)

1. Install: `pip install psycopg2-binary`
2. In `.env` set: `DATABASE_URL=postgresql://user:password@localhost:5432/school_db`
3. In `settings.py` uncomment the PostgreSQL `DATABASES` block

---

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Home / redirect to dashboard |
| `/login/` | Login page |
| `/register/` | Register new account |
| `/dashboard/` | Role-based dashboard |
| `/courses/` | Course list |
| `/courses/<id>/` | Course detail |
| `/courses/create/` | Create course (teacher) |
| `/courses/<id>/enroll/` | Enroll in course (student) |
| `/assignments/<id>/` | Assignment detail |
| `/assignments/<id>/submit/` | Submit assignment (student) |
| `/submissions/<id>/grade/` | Grade a submission (teacher) |
| `/admin/` | Django admin panel |
