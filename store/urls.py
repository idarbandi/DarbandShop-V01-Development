from . import views
from django.urls import path

app_name = "store"

urlpatterns = [
    path("", views.all_products, name="all_products")
]