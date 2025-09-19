from django.contrib import admin
from .models import Transaction, Category, Budget, Diagnosis , Card

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']
    search_fields = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'amount', 'currency', 'category', 'date']
    list_filter = ['type', 'currency', 'category']
    search_fields = ['note']

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['category', 'limit_amount', 'start_date', 'end_date']
    list_filter = ['category']
    search_fields = ['category__name']

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'created_at']
    search_fields = (['message'])

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_number', 'balance']
    search_fields = ['user']
