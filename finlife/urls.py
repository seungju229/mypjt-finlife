from django.urls import path
from . import views

app_name= 'finlife'
urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products),
    path('deposit-products/', views.deposit_products),
    path('deposit-products-options/<str:fin_prdt_cd>/', views.deposit_products_options),
    path('deposit-products/top_rate/', views.top_rate),
]
