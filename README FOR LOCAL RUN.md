
# 🚀 FinalProject - Task Prioritization System

This is a Django-based web application designed for managing and prioritizing factory tasks. It integrates a machine learning model to predict task priority and supports full CRUD operations.

---

## 📦 Project Features

- Manage unassigned, assigned, and historical tasks
- Integrate ML model to predict task priority
- Push tasks through the workflow
- MySQL database backend
- Built with Django

---

## 💻 Local Setup Instructions

Follow these steps to set up and run the project locally.

### ✅ 1. Prerequisites

Make sure the following are installed:

- Python 3.x
- pip
- MySQL Server
- virtualenv (optional but recommended)
- MySQL client library (`mysqlclient` or `PyMySQL`)

```bash
# Install dependencies (example with mysqlclient)
pip install -r requirements.txt
```

---

### ✅ 2. Create and Configure the Database

Start MySQL and create a database:

```sql
CREATE DATABASE finalproject CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

(Optional) Create a new MySQL user:

```sql
CREATE USER 'youruser'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON finalproject.* TO 'youruser'@'localhost';
FLUSH PRIVILEGES;
```

Edit `settings.py` to match your database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finalproject',
        'USER': 'youruser',
        'PASSWORD': 'yourpassword',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}
```

---

### ✅ 3. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### ✅ 4. Start the Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧠 Model Integration (Optional)

If your project includes a trained ML model, ensure the model file is in the correct path and is loaded in your view or service layer before prediction. You can use `joblib`, `pickle`, or TensorFlow/PyTorch depending on your model type.

---

## 📝 License

This project is for educational and internal use. Feel free to fork and customize.

---

## 🙋‍♂️ Need Help?

Feel free to open an issue or contact the maintainer.
