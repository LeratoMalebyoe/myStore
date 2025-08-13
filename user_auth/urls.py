from django.urls import path
from . import views

app_name = 'user_auth'

urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('signup/',         views.signup,            name='signup'),
    path('authenticate/', views.authenticate_user, name='authenticate_user'),
    path('logout/',         views.user_logout,       name='logout'),
    path('profile/',        views.show_user,      name='profile'),
]
