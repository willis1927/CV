from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("<int:listingID>", views.listing, name="listing"),
    path("amend", views.amend, name="amend"),
    path("watch", views.watch, name="watch"),
    path("removewatch", views.removewatch, name="removewatch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/", views.bid, name="bid"),
    path("close", views.close, name="close"),
    path("comment", views.comment, name="comment")
    ]
