# 🌿 Cauliflower AI – Disease Detection Platform

## Description

Cauliflower AI is a Django-based platform that helps farmers detect diseases in cauliflower crops using uploaded images.  
It provides **role-based dashboards** for farmers, doctors, and admins to manage, review, and monitor crop health efficiently.

---

## 🚀 Project Structure

```plaintext
cauliflower_ai/
├── venv/                       # Virtual environment
├── manage.py
├── db.sqlite3                   # Local DB (SQLite for dev)
├── config/                      # Django settings + URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── ui/                      # Frontend templates and static files
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── image/
│   │   │   └── js/
│   │   └── templates/
│   │       ├── base.html
│   │       ├── landing.html
│   │       ├── auth/
│   │       │   ├── login.html
│   │       │   └── register/
│   │       │       ├── register_user.html
│   │       │       └── register_doctor.html
│   │       ├── components/
│   │       │   ├── footer.html
│   │       │   └── navbar.html
│   │       └── dashboard/
│   │           ├── dashboard_admin.html
│   │           ├── dashboard_doctor.html
│   │           └── dashboard_user.html
│   ├── doctor/                  # Logic/models for doctors
│   ├── user/                    # Logic/models for farmers
│   └── core/                    # Shared logic
├── tailwind_build/
│   ├── input.css
│   ├── package-lock.json
│   ├── package.json
│   └── tailwind.config.js
├── scripts.txt
```

### Notes

- All UI templates and static files are located under `apps/ui/`.
- Styling is implemented using **Tailwind CSS** with **daisyUI**.

---

## 🔧 Setup Instructions

### 1. Clone and Navigate to Project

```bash
git clone <repo-url>
cd cauliflower_ai
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows:
venv\Scripts\activate

# For Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Build Tailwind CSS

```bash
cd tailwind_build
npx tailwindcss -i input.css -o ../apps/ui/static/css/styles.css
cd ..
```

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start Development Server

```bash
python manage.py runserver
```

---

## 🧠 Roles and Dashboards

| Role   | Path              | Features                          |
| ------ | ----------------- | --------------------------------- |
| Farmer | /dashboard/user   | Upload image, see prediction      |
| Doctor | /dashboard/doctor | Review cases, give advice         |
| Admin  | /dashboard/admin  | Manage users and platform content |

---

## ✨ Sample Accounts

### Superuser

- **Username:** wamiq
- **Email:** wamiq@email.com
- **Password:**adminpass

### Farmer

- **Username:** greenfields_john
- **Password:** SecureFarm2025!

### Doctor

- **Username:** dr_smwangi
- **Password:** CauliExpert@2025

### Admin

- **Username:** admin01
- **Password:** Password

---

## 📄 Project Team

- **Frontend/Backend Project Lead:** Wamiq Aahid
- **AI Engineer:** Anonymous
