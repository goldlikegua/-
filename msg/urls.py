from django.urls import path
from . import views
urlpatterns = [
    path('article', views.article),
    path('comment', views.add_comment),
    path('add_article', views.add_article),
    path('delete_article', views.delete_article),
    path('delete_comment', views.delete_comment),
    path('selected_article', views.selected_article),
    path('save_article', views.save_article)
]