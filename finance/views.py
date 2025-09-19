from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from .models import Transaction, Category, Budget, Card
from .forms import TransactionForm, CategoryForm, BudgetForm, StatisticsForm, CardForm
from decimal import Decimal
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    currency = request.GET.get('currency', 'UZS')
    income = Transaction.objects.filter(user=request.user, type="income", currency=currency).aggregate(total=Sum("amount"))["total"] or 0
    expense = Transaction.objects.filter(user=request.user, type="expense", currency=currency).aggregate(total=Sum("amount"))["total"] or 0
    balance = sum(card.balance for card in Card.objects.filter(user=request.user, currency=currency))
    categories = Category.objects.all()
    cards = Card.objects.filter(user=request.user)

    # Byudjet ogohlantirishlari
    budgets = Budget.objects.filter(user=request.user, currency=currency)
    budget_warnings = []
    for budget in budgets:
        spent = Transaction.objects.filter(user=request.user, category=budget.category, type='expense', currency=currency).aggregate(total=Sum('amount'))['total'] or 0
        if spent > budget.amount:
            budget_warnings.append({
                'category': budget.category.name,
                'spent': spent,
                'budget': budget.amount
            })

    return render(request, "dashboard.html", {
        "income": income,
        "expense": expense,
        "balance": balance,
        "categories": categories,
        "cards": cards,
        "currency": currency,
        "budget_warnings": budget_warnings
    })

@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            card = transaction.card

            if transaction.type == "expense":
                if card.balance >= transaction.amount:
                    card.balance -= transaction.amount
                else:
                    messages.error(request, "Kartada mablag‘ yetarli emas!")
                    return redirect("add_transaction")
            elif transaction.type == "income":
                card.balance += transaction.amount

            card.save()
            transaction.user = request.user
            transaction.currency = card.currency
            transaction.save()

            messages.success(request, "Tranzaksiya muvaffaqiyatli qo‘shildi!")
            return redirect("home")
    else:
        form = TransactionForm(request.user)

    return render(request, "add_transaction.html", {"form": form})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@login_required
def add_budget(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, "Byudjet muvaffaqiyatli qo‘shildi!")
            return redirect('home')
    else:
        form = BudgetForm()
    return render(request, 'add_budget.html', {'form': form, 'categories': categories})

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})

@login_required(login_url='login')
def update_profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        image = request.FILES.get('image')

        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, "Bu username allaqachon band.")
            return redirect('update-profile')

        user.username = username
        user.email = email
        user.save()

        if image:
            profile.image = image
            profile.save()

        messages.success(request, "Profil muvaffaqiyatli yangilandi.")
        return redirect('profile')

    return render(request, 'account/edit_profile.html', {
        'user': user,
        'profile': profile
    })

@login_required(login_url='login')
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Parolingiz muvaffaqiyatli o'zgartirildi!")
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if 'old_password' in field:
                        messages.error(request, "Hozirgi parolingiz xato kiritildi!")
                    elif 'new_password2' in field:
                        messages.error(request, "Yangi parollar mos kelmadi!")
                    else:
                        messages.error(request, f"Xato: {error}")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'account/change_password.html')

def about(request):
    return render(request, 'account/about.html')

@login_required
def card_list(request):
    cards = Card.objects.filter(user=request.user)
    return render(request, 'card_list.html', {'cards': cards})

@login_required
def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            messages.success(request, "Karta muvaffaqiyatli qo‘shildi!")
            return redirect('card-list')
    else:
        form = CardForm()
    return render(request, 'add_card.html', {'form': form})

@login_required
def transfer_money(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)
    categories = Category.objects.all()

    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        operation = request.POST.get('operation')
        category_id = request.POST.get('category')
        category = None
        if category_id:
            category = Category.objects.get(id=category_id)

        if operation == 'income':
            card.balance += amount
            Transaction.objects.create(
                user=request.user,
                type='income',
                amount=amount,
                currency=card.currency,
                card=card,
                date=datetime.today(),
                category=category,
                note=f"Kartaga kirim: {card.card_number[-4:]}"
            )
        elif operation == 'expense':
            if card.balance >= amount:
                card.balance -= amount
                Transaction.objects.create(
                    user=request.user,
                    type='expense',
                    amount=amount,
                    currency=card.currency,
                    card=card,
                    date=datetime.today(),
                    category=category,
                    note=f"Kartadan chiqim: {card.card_number[-4:]}"
                )
            else:
                messages.error(request, "Kartada mablag' yetarli emas!")
                return redirect('card-list')

        card.save()
        messages.success(request, "Amaliyot muvaffaqiyatli bajarildi!")
        return redirect('card-list')

    return render(request, 'transfer_money.html', {'card': card, 'categories': categories})

@login_required
def category_detail(request, cat_id):
    category = get_object_or_404(Category, id=cat_id)
    currency = request.GET.get('currency', 'UZS')
    transactions = Transaction.objects.filter(user=request.user, category=category, currency=currency).order_by('-date')
    total_income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'category_detail.html', {
        'category': category,
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'currency': currency
    })

@login_required
def statistics(request):
    form = StatisticsForm(request.POST or None)
    if request.POST.get("start_date"):
        start_date = datetime.strptime(request.POST["start_date"], "%Y-%m-%d").date()
    else:
        start_date = (timezone.now() - timedelta(days=7)).date()

    if request.POST.get("end_date"):
        end_date = datetime.strptime(request.POST["end_date"], "%Y-%m-%d").date()
    else:
        end_date = timezone.now().date()

    period_type = request.POST.get("period_type", "WEEKLY")
    currency = request.POST.get("currency", "UZS")

    transactions = Transaction.objects.filter(
        user=request.user,
        date__range=[start_date, end_date],
        currency=currency
    )

    income = transactions.filter(type="income").aggregate(total=Sum("amount"))["total"] or 0
    expense = transactions.filter(type="expense").aggregate(total=Sum("amount"))["total"] or 0
    balance = income - expense

    stats = []
    if period_type == "WEEKLY":
        days_count = (end_date - start_date).days + 1
        for i in range(days_count):
            day = start_date + timedelta(days=i)
            day_income = transactions.filter(type="income", date=day).aggregate(total=Sum("amount"))["total"] or 0
            day_expense = transactions.filter(type="expense", date=day).aggregate(total=Sum("amount"))["total"] or 0
            stats.append({
                "date": day,
                "income": day_income,
                "expense": day_expense,
                "balance": day_income - day_expense,
            })
    elif period_type == "MONTHLY":
        start_month = start_date.replace(day=1)
        end_month = end_date.replace(day=1)
        current = start_month
        while current <= end_month:
            next_month = (current + timedelta(days=32)).replace(day=1)
            month_income = transactions.filter(type="income", date__range=[current, next_month - timedelta(days=1)]).aggregate(total=Sum("amount"))["total"] or 0
            month_expense = transactions.filter(type="expense", date__range=[current, next_month - timedelta(days=1)]).aggregate(total=Sum("amount"))["total"] or 0
            stats.append({
                "date": current,
                "income": month_income,
                "expense": month_expense,
                "balance": month_income - month_expense,
            })
            current = next_month
    elif period_type == "YEARLY":
        start_year = start_date.year
        end_year = end_date.year
        for year in range(start_year, end_year + 1):
            year_start = datetime(year, 1, 1).date()
            year_end = datetime(year, 12, 31).date()
            year_income = transactions.filter(type="income", date__range=[year_start, year_end]).aggregate(total=Sum("amount"))["total"] or 0
            year_expense = transactions.filter(type="expense", date__range=[year_start, year_end]).aggregate(total=Sum("amount"))["total"] or 0
            stats.append({
                "date": year_start,
                "income": year_income,
                "expense": year_expense,
                "balance": year_income - year_expense,
            })

    context = {
        "form": form,
        "income": income,
        "expense": expense,
        "balance": balance,
        "stats": stats,
        "start_date": start_date,
        "end_date": end_date,
        "period_type": period_type,
        "currency": currency,
        "currencies": ["UZS", "USD", "EUR"],
    }
    return render(request, "statistics.html", context)

@login_required
def card_list(request):
    cards = Card.objects.filter(user=request.user)
    return render(request, 'card_list.html', {'cards': cards})

@login_required
def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            messages.success(request, "Karta muvaffaqiyatli qo‘shildi!")
            return redirect('card-list')
    else:
        form = CardForm()
    return render(request, 'add_card.html', {'form': form})