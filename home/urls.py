from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('login', views.loginuser, name='login'),
    path('register', views.register, name='register'),
    path('edit', views.edit, name='edit'),
    path('change', views.change, name='change'),
    path('dash', views.dash, name='dash'),
    path('logout', views.logout_user, name='logout'),
    path('forgot', views.forgot, name='forgot'),

]
