# 💸 Django Finance Tracker with Gemini AI

A personal finance tracking web application built with **Django**, **MySQL**, and **Google Gemini AI** for intelligent monthly summaries. Users can securely log in, add income/expenses, filter/search by categories, and get a 50-word monthly insight using AI.

---

## 🚀 Features

- 🔐 User authentication (Sign up, Login, Logout)
- 💰 Add, update, and delete income & expenses
- 🔍 Filter by type, category, payment method, or search keyword
- 📅 Monthly income, expense, and balance summaries
- 🧠 AI-generated monthly summary using Gemini (50 words)
- 🎨 Clean, card-based UI with Tailwind-like playful design

---

## 🛠️ Tech Stack

- **Backend:** Django, Python, MySQL
- **Frontend:** HTML, CSS (raw, custom), Django Templates
- **AI Integration:** Google Gemini API
- **Other:** Django Auth, Bootstrap Icons

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/django-finance-tracker.git
cd django-finance-tracker
````

### 2. Create virtual environment & install requirements

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure database

Set up MySQL and update your `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Then run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the app

```bash
python manage.py runserver
```

---

## 🤖 Gemini AI Integration

### Step 1: Install SDK

```bash
pip install -U google-genai
```

### Step 2: Set your API key

Create a `.env` file or export in terminal:

```bash
export GOOGLE_API_KEY="your_gemini_api_key"
```

Or load it securely in your `settings.py`:

```python
import os
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
```

### Step 3: Call Gemini in views

```python
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)

def generate_monthly_summary(data):
    prompt = f"Summarize this finance data in 50 words:\n{data}"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()
```

You can pass a list of recent transactions to the function and display the result in the dashboard.

---

## 📂 Project Structure

```
tracker/
│
├── templates/
│   ├── tracker/
│   │   ├── dashboard.html
│   │   └── summary.html
│
├── static/
│   └── tracker/
│       ├── signup.css
│       └── style.css
│
├── models.py
├── views.py
├── forms.py
├── urls.py
└── ai_summary.py   # (for Gemini API call)
```

---


Sample entries:

* Income: Freelancing (\$800), Gift (\$200)
* Expense: Rent (\$300), Food (\$100), Internet (\$50)

---

## 📌 License

MIT License. Feel free to use and modify.

---

## ✨ Future Ideas

* 📊 Add charts using Chart.js or ApexCharts
* 📱 Mobile responsive design
* 🧠 Add budgeting suggestions using AI
* 🗂 Export reports (PDF/CSV)

---

> Built by Kazi Shah Hama [kazishahhamza01@gmail.com]
