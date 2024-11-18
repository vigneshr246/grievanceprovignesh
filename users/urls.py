from django.urls import path
from users import views # type: ignore

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('process-input/', views.login_page, name='login_form'),
    path('register/', views.register_page, name='registration_form'),
    path('forget/', views.forget_page, name='forget_form'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    ]
