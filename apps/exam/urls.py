from django.conf.urls import url
from . import views

urlpatterns = [
	url(r"^$", views.index),
	url(r"^register$", views.register),
    url(r"^login$", views.login),
    url(r"^books$", views.books),
    url(r"^logout$", views.logout),
    url(r"^books/add$", views.addBooks),
    url(r"^create$", views.create),
    url(r'^books/(?P<no>\d+)/$', views.showBook),
    url(r"^addReview$", views.addReview),
    url(r'^users/(?P<id>\d+)/$', views.showUser),
    #url(r'^books/(?P<id>\d+)/addReview/books/(?P<id>\d+)/$', views.showBook)
]