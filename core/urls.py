from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    #path('logout/', views.logout_view, name='logout'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
]

