from django.urls import path
from . import views

urlpatterns = [
    path('index/<int:id>', views.index),
    path('add_plate', views.add_plate),
    path('msg', views.plate_msg),
    path('delete_plate', views.delete_plate),
    path('save_plate', views.save_plate)
]