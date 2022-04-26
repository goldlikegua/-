from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('msg', views.msg),
    path('msg_other', views.msg_other),
    path('get_code', views.get_code),
    path('update_user', views.update_user)
]
