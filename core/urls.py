from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='landing'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('account_setup',views.account_setup,name='account_setup'),
    path('edit-cycle/<int:cycle_id>/', views.edit_cycle, name='edit_cycle'),
    path('remove-cycle/<int:cycle_id>/', views.remove_listing, name='remove_cycle'),
    path('relist-cycle/<int:cycle_id>/', views.relist_cycle, name='relist_cycle'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('api/cycle-locations/', views.get_cycle_locations, name='cycle_locations'),

]

