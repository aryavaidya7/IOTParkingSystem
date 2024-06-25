from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('slot_status/', views.slot_status, name='slot_status'),
    path('description/', views.description, name='description'),
    path('operate/', views.operate, name='operate'),
    path('control/<str:action>/', views.control_barrier, name='control_barrier'),
    path('get_slot_status/', views.get_slot_status, name='get_slot_status'),
    path('logout/', views.logout_view, name='logout'),
    ]
