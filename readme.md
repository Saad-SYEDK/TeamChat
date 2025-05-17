# 🗨️ TeamChat – Real-Time Django Chat Platform

---

## ✨ Features

| Core Features                      | Bonus Features                        |
|-----------------------------------|---------------------------------------|
| 🔐 User login, logout, registration | ✅ Unread message badges              |
| 💬 One-on-one and group chats      | ✅ Typing-indicator (WebSocket-ready) |
| ⚡ Real-time messaging              | 🧹 Message delete/edit (TODO)         |
| 🗂 Chat history with DB persistence | 🔍 Search (placeholder UI)           |
| 🎨 Bootstrap 5 Responsive UI       | 🌙 Dark-mode ready                    |
| 🔒 Secure CSRF & WebSocket auth    | 🚀 Docker & Render deploy setup      |

---

## 📸 Screenshots

**Login Page**

![Login Page](screenshots/login.PNG)

**Login Page**

![Signup Page](screenshots/signup.PNG)

**Chat Dashboard**

![Chat Dashboard](screenshots/home.PNG)

**Real-Time Messaging**

![Real-Time Chat](screenshots/realtime.PNG)


## 🛠️ Tech Stack

- **Python 3.11**
- **Django 5.2.1**
- **Django Channels 4**
- **Bootstrap 5**
- **SQLite (local)** / **PostgreSQL (Render)**
- **Redis (Upstash - prod channel layer)**
- **Docker + Daphne + Gunicorn**

---
## 📂 Project Structure
teamchat/
├── chat/
│   ├── migrations/
│   ├── templates/chat/
│   ├── static/chat/
│   ├── consumers.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── teamchat/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
├── templates/
│   └── base.html
├── static/
│   └── ...
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md

## ⚙️ How to Run Locally

### 1. Clone and set up environment
```bash
git clone https://github.com/Saad-SYEDK/TeamChat
cd teamchat
python -m venv venv
source venv/bin/activate
```

### 2. Install requirements
```bash
pip install -r requirements.txt
```
### 3.Apply migrations and create superuser (optional)
```bash
python manage.py migrate
python manage.py createsuperuser  # optional, for admin access
```
### 4. Run server
```bash
daphne -b 0.0.0.0 -p 8000 teamchat.asgi:application
```