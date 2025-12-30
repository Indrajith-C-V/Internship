from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('apply/<int:pk>/', views.apply_internship, name='apply_internship'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_users/', views.admin_users, name='admin_users'),
    path('admin_internships/', views.admin_internships, name='admin_internships'),
    path('admin_applications/', views.admin_applications, name='admin_applications'),
    path('admin_internship_add/', views.internship_add, name='internship_add'),
    path('admin_internship_edit/<int:pk>/', views.internship_edit, name='internship_edit'),
    path('admin_internship_delete/<int:pk>/', views.internship_delete, name='internship_delete'),
    path('admin_internship_detail/<int:pk>/', views.admin_internship_detail, name='admin_internship_detail'),
    path('admin_user_delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('admin_application_approve/<int:pk>/', views.application_approve, name='application_approve'),
    path('admin_application_reject/<int:pk>/', views.application_reject, name='application_reject'),
    path('admin_application_detail/<int:pk>/', views.admin_application_detail, name='admin_application_detail'),
]