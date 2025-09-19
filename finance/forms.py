from django import forms
from .models import Transaction, Category, Budget, Diagnosis , Card

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['card', 'category', 'type', 'amount', 'currency', 'note']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['card'].queryset = Card.objects.filter(user=user)
        self.fields['category'].queryset = Category.objects.all()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'icon']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'limit_amount', 'currency']
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full p-2 border rounded-md'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter budget amount'}),
            'currency': forms.Select(choices=[('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')]),
        }
class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['message']

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_number', 'balance', 'currency', 'card_type']
        widgets = {
            'card_number': forms.TextInput(attrs={'placeholder': 'Enter card number (16 digits)'}),
            'balance': forms.NumberInput(attrs={'placeholder': 'Enter balance'}),
            'currency': forms.Select(choices=[('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')]),
            'card_type': forms.Select(choices=[('Visa', 'Visa'), ('MasterCard', 'MasterCard'), ('Uzcard', 'Uzcard')]),
        }
class StatisticsForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    period_type = forms.ChoiceField(choices=[
        ('WEEKLY', 'Haftalik'),
        ('MONTHLY', 'Oylik'),
        ('YEARLY', 'Yillik')
    ], required=False)
    currency = forms.ChoiceField(choices=[
        ('UZS', 'UZS'),
        ('USD', 'USD'),
        ('EUR', 'EUR')
    ], required=False)