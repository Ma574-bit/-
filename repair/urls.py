from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('report/', views.report_repair, name='report'),
    path('repairs/', views.repair_list, name='repair_list'),
    path('repairs/<int:repair_id>/', views.repair_detail, name='repair_detail'),
]
