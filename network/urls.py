
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>",views.profile, name="profile"),
    path("following/<int:id>",views.following, name="following"),

    #API routes
    
    path("edit/<int:id>",views.edit_post, name="edit_post"),
    path("toggle_like/<int:id>",views.toggle_like, name="toggle_like"),
    path("toggle_following/<int:id>",views.toggle_following, name="toggle_following"),
]
