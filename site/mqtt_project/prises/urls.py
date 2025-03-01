from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('toggle/<str:prise>/', views.toggle_prise, name='toggle_prise'),
    path('control_all0/', views.control_all0, name='control_all0'),
    path('control_all1/', views.control_all1, name='control_all1'),
    path('login/', views.login, name='login'),
    path('dash/', views.index, name='dash'),
    path('logout/', views.logout, name='logout'),
]
