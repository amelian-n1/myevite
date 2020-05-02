from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('newEvent', views.newEvent),
    path('createEvent',views.createEvent),
    path('evite/<int:id>',views.evite),
    path('eventDetails/<int:id>', views.eventDetails),
    path('rsvp', views.rsvp),
    path('delete/<int:id>', views.delete),
    path('logout', views.logout),
]