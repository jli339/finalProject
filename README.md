#  Task Priority Prediction System

This is a Django-based web application designed to predict and manage task priorities in a manufacturing environment. It leverages a trained machine learning model to estimate task urgency and supports both single-task and batch-task predictions.

---

##  Project Structure

```
├── FinalProject/             # Main Django app
│   ├── migrations/           # Django migration files
│   ├── static/               # Static files (JS, CSS, etc.)
│   ├── templates/            # HTML templates
│   ├── views.py              # View logic
│   ├── models.py             # Managed models
│   └── unmanaged_models.py   # Unmanaged models (existing tables)
├── ml_models/                # Trained machine learning models
├── manage.py                 # Django project runner
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

##  Features

- User authentication system (login/logout)
- Batch task priority prediction
- Single task priority prediction
- View and manage:
  - Unassigned tasks
  - Assigned tasks
  - Historical tasks
- Priority scores and labels generated from ML model
- Admin panel for full data management

---

##  Getting Started

###  Clone and Setup

```bash
git clone https://github.com/jli339/finalProject.git
cd your-repo
```

###  Create virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 🔄 Apply migrations and load model/data

```bash
python manage.py makemigrations
python manage.py migrate
```

(Optional) Load initial data if provided:

```bash
python manage.py loaddata data_clean_project_only.json
python manage.py loaddata data_user_system.json
```

### 👤 Create superuser (admin)

```bash
python manage.py createsuperuser
```

### ▶️ Run the server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

##  ML Model Info

The priority prediction is powered by a trained ML model saved in the `ml_models/` folder. It receives task features and returns:

- A numerical **priority score**
- A **priority label** (`Not_High`, `High`)

---

##  Deployment Notes (Render)

- App is deployed on [Render](https://render.com)
- PostgreSQL is used in production (via `DATABASE_URL`)
- Static files are collected using:

```bash
python manage.py collectstatic --noinput
```

Make sure `STATIC_URL` and `STATIC_ROOT` are correctly set in `settings.py`.

---

##  Dependencies

- Django 5.x
- psycopg2
- pandas / numpy
- scikit-learn / xgboost
- dj-database-url

All dependencies are listed in `requirements.txt`.

---

## 📬 Contact

Maintained by **Jiahao Li**  
📧 Email: 838124877@qq.com  
🔗 GitHub: https://github.com/jli339/finalProject.git

---
