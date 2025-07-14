from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("campadmin", views.campadmin, name="campadmin"),
    path("add_campsite", views.add_campsite, name="add_campsite"),
    path("site/<int:siteID>", views.site, name="site"),
    path("add_plot", views.add_plot, name="add_plot"),
    path("site/delete/<int:plotID>", views.delete_plot, name="delete_plot"),
    path("closesite/<int:siteID>", views.close_site, name="close_site"),
    path('book', views.book, name="book"),
    path('book/<str:type>/<int:id>/', views.book, name="book"),
    path('view_bookings/<int:siteID>', views.view_bookings, name="view_bookings"),
    path("search", views.search, name = "search"),
    path("facility", views.facility, name="facility"),
    path("accountadmin", views.accountadmin, name="accountadmin"),
    path("updatepassword", views.updatepassword, name="updatepassword")
    
]