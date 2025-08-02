from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('finance/edit/<int:id>/', views.edit_finance, name='edit_finance'),
    path('finance/delete/<int:id>/', views.delete_finance, name='delete_finance'),
    path('export/', views.export_csv, name='export_csv'),

]
