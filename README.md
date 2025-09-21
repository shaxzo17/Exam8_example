Finance App

Finance App – bu shaxsiy moliya boshqaruvi ilovasi bo‘lib, foydalanuvchi o‘z daromadlari va xarajatlarini kuzatishi, kategoriyalarga ajratishi va statistikani ko‘rishi mumkin. Django va Django REST Framework asosida yaratilgan.

🛠 Texnologiyalar

Python 3.11+

Django 4.2+

Django REST Framework

djangorestframework-simplejwt (JWT authentication)

SQLite (lokal DB, keyinchalik PostgreSQL ga o‘tish mumkin)

Tailwind CSS (frontend uchun)

⚡️ Xususiyatlar

Authentication & Authorization

JWT token bilan login/logout

Token refresh

Signup: email va phone number orqali 6 xonali tasdiqlash kodi

Profile update, password reset

Finance Management

Categories (Income / Expense)

Budgets

Transactions

Oxirgi 5 ta tranzaksiya

Income / Expense alohida filtrlash

Summary va daily stats (kunlik, start-end date oralig‘i)

API Endpoints
Base URL: /api/transactions/

/categories/ — GET, POST, PUT, DELETE (Categories CRUD)

/budgets/ — GET, POST, PUT, DELETE (Budgets CRUD)

/transactions/ — GET, POST, PUT, DELETE (Transactions CRUD)

/transactions/income/ — GET (faqat INCOME lar)

/transactions/expense/ — GET (faqat EXPENSE lar)

/transactions/summary/ — GET (Umumiy balans, income va expense)

/transactions/daily_stats/?date=YYYY-MM-DD — GET (tanlangan kun statistika)


⚡️ Ishlatish bo‘yicha qo‘llanma

Karta qo‘shish: My Cards → Add Card → Card raqami, holder va balans

Tranzaksiya qo‘shish: Transactions → Select Card → Category → Amount → Submit

Category qo‘shish: Dashboard → Add Category (+) → Name → Type


Hisobotlar: Dashboard → Umumiy balans, kunlik/oylik income va expense

🚀 Ishga tushirish (Git bilan)

Git repository linkini nusxalash
Loyiha GitHub yoki boshqa Git serverida joylashgan bo‘lsa, uning linkini nusxalash. Masalan, https://github.com/username/finance-app.git.

Repository-ni klonlash
Nusxalangan link yordamida loyihani lokal kompyuteringizga klonlash.

Virtual environment yaratish va faollashtirish

Loyiha uchun alohida Python muhiti yaratish.

Muhitni faollashtirish, shunda loyiha paketlari boshqa loyihalarga aralashmaydi.

Dependencies o‘rnatish

requirements.txt faylidan barcha kerakli paketlarni o‘rnatish.

Shu bilan loyihani ishlash uchun zarur kutubxonalar tayyor bo‘ladi.

Migratsiyalarni bajarish

Django modeli bilan bog‘liq barcha migratsiyalarni bajarish.

Shu orqali lokal ma’lumotlar bazasida barcha jadval va strukturalar yaratiladi.

Superuser yaratish

Admin panelga kirish va loyihani boshqarish uchun superuser yaratish.

Shu orqali kategoriyalar, kartalar va tranzaksiyalarni boshqarish mumkin bo‘ladi.

Serverni ishga tushirish

Django lokal serverini ishga tushirib, loyihani brauzer orqali ochish.

Brauzer orqali ishlatish

Foydalanuvchi sifatida login qilish.

Category qo‘shish, kartaga pul qo‘yish va tranzaksiyalarni kuzatish.

Dashboard va statistikani ko‘rish.
