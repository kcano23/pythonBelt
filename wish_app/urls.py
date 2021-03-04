from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('wishes',views.wishes),
    path('logout',views.logout),
    path('login',views.login),
    path('wishes/new',views.newWish),
    path('wished/<int:userid>',views.wished),
    path('delete/<int:wishid>',views.delete),
    path('edit/<int:wishid>',views.edit),
    path('update/<int:wishid>',views.update),
    path('grant/<int:wishid>',views.grant),
    path('like/<int:wishid>',views.like),
    path('stats', views.stats),
]