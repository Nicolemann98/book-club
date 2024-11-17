from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_newsletter, name='send_newsletter'),
    path('view/', views.view_newsletters, name='view_newsletters'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('unsubscribe/', views.unsubscribe_newsletter, name='unsubscribe_newsletter'),
]
