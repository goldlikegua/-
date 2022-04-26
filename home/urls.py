from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    #path('home', views.home_index),
    #path('home', views.home),
    path('home', views.selected_home),
    path('selected', views.selected_home),
    path('search', views.search)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)