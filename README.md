# Finance App

**Finance App** — bu shaxsiy moliya boshqaruvi ilovasi bo‘lib, foydalanuvchi o‘z daromadlari va xarajatlarini kuzatishi, kategoriyalarga ajratishi va statistikani ko‘rishi mumkin.  
Loyiha **Django** va **Django REST Framework** asosida yaratilgan.

---

## 🛠 Texnologiyalar

- Python 3.11+
- Django 4.2+
- Django REST Framework
- Tailwind CSS (frontend uchun)

---

## ⚡️ Xususiyatlar

### Authentication & Authorization
- JWT token bilan login/logout
- Token refresh
- Signup: email va telefon orqali 6 xonali tasdiqlash kodi
- Profile update va password reset

### Finance Management
- Categories (Income / Expense)
- Budgets
- Transactions
- Oxirgi 5 ta tranzaksiya
- Income / Expense bo‘yicha filtrlar
- Summary va daily stats (kunlik va start-end date oralig‘ida)

---

## 🧩 Loyihaning tuzilishi
- finance/ — Django app: models, views, forms, serializers, templates
- static/ — CSS, JS, icons
- media/ — Profile images
- templates/ — Base template
- requirements.txt — Project dependencies
- manage.py — Django entry point

---

## 🚀 Ishga tushirish (step-by-step)

1. **Git repository linkini nusxalash**  
   Loyiha GitHub yoki boshqa Git serverida joylashgan bo‘lsa, linkini nusxalash.

2. **Repository-ni klonlash**  
   Nusxalangan link yordamida loyihani lokal kompyuteringizga klonlash.  

   ```bash
   git clone <repository-link>
   cd finance-app

    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux / Mac
    source .venv/bin/activate

    pip install -r requirements.txt
    
    python manage.py makemigrations
    python manage.py migrate

    python manage.py createsuperuser
  
    python manage.py runserver
