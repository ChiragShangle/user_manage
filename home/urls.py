from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('log', views.loginuser, name='log'),
    path('register', views.register, name='register'),
    path('edit', views.edit, name='edit'),
    path('change', views.change, name='change'),
    path('dash', views.dash, name='dash'),
    path('logout', views.logout_user, name='logout'),
    path('forgot', views.forgot, name='forgot'),
    path('change-password/<token>', views.ChangePassword, name="change-password"),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('token', views.token_send, name='token_send'),


]
