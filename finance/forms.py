from django import forms
from .models import Transaction, Category, Budget, Diagnosis , Card

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['card', 'category', 'type', 'amount', 'currency', 'note']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['card'].queryset = Card.objects.filter(user=user)
        else:
            self.fields['card'].queryset = Card.objects.none()
        self.fields['category'].queryset = Category.objects.all()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name' , 'icon']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'limit_amount', 'currency', 'start_date', 'end_date']
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full p-2 border rounded-md'}),
            'limit_amount': forms.NumberInput(attrs={'placeholder': 'Enter budget amount'}),
            'currency': forms.Select(choices=[('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')]),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['message']

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_holder', 'card_number', 'balance', 'currency', 'card_type']
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