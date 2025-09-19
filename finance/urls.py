from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='home'),
    path('add-transaction/', add_transaction, name='add_transaction'),
    path('add-category/', add_category, name='add_category'),
    path('add-budget/', add_budget, name='add_budget'),
    path('add-card/', add_card, name='add-card'),
    path('card-list/', card_list, name='card-list'),
    path('statistics/', statistics, name='statistics'),
    path('transfer-money/<int:card_id>/', transfer_money, name='transfer_money'),
    path('category/<int:cat_id>/', category_detail, name='category_detail'),
    path('profile/', profile_view, name='profile'),
    path('update-profile/', update_profile_view, name='update-profile'),
    path('change-password/', change_password_view, name='change_password'),
    path('about/',about, name='about'),
]
