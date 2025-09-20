from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class Category(models.Model):
    TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    icon = models.CharField(max_length=50, blank=True, null=True, default="fa-folder")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=[('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')], default='UZS')
    card_type = models.CharField(max_length=20, choices=[
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('uzcard', 'UzCard')
    ])

    def __str__(self):
        return f"{self.card_type} - **** **** **** {self.card_number[-4:]} ({self.currency})"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, choices=[('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')], default="UZS")
    note = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.type} - {self.amount} {self.currency}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    currency = models.CharField(
        max_length=3,
        choices=[('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')],
        default='UZS'
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user} - {self.category.name} - {self.limit_amount}"

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_income = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    total_expense = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Report {self.user} ({self.start_date} - {self.end_date})"


class Statistic(models.Model):
    PERIOD_CHOICES = [
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()
    total_income = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    total_expense = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user} - {self.period_type} ({self.period_start} - {self.period_end})"


class Diagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username