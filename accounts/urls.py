from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:pk>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete_view, name='user_delete'),
]
