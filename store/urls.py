from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Home page displaying all products
    path('', views.home, name='home'),

    # Product listing page
    path('products/', views.product_list, name='products'),

    # Product detail page with slug-based URL
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),

    # Add a product to the cart
]