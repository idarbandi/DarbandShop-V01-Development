from django.urls import include, path
from . import views

app_name = "account"
urlpatterns = [
    path("register/", views.account_register, name="register"),
    path("activate/<slug:uidb64>/<slug:token>", views.account_activate, name="activate"),
    # user dashboard
    path("dashboard/", views.dashboard, name="dashboard")
]