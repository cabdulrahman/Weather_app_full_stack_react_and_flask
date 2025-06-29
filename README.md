# 🌦️ Full Stack Weather App

A full-stack weather application that allows users to:
- Search for real-time weather by city
- Register and log in
- Add favorite cities
- View saved favorites

## 🛠️ Tech Stack

- **Frontend:** React (Vite)
- **Backend:** Flask + Flask-JWT-Extended
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** JWT
- **API:** OpenWeatherMap API

---

## 🚀 Features

### ✅ Public
- View weather in any city
- User-friendly UI with instant feedback

### 🔐 Authenticated
- Register & Log In (JWT-based auth)
- Add cities to favorites
- View list of favorite cities

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Weather_app_full_stack_react_and_flask.git
cd Weather_app_full_stack_react_and_flask

### Backend setup
cd my-weather-app/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade
python seed.py  
python app.py

### Frontend setup
cd ../frontend/my-weather-app
npm install
npm run dev


By Cabdulrahman

Licence 
This project is licenced under the MIT licence
