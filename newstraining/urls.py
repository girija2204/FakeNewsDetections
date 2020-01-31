from django.urls import path
from . import views

urlpatterns = [path("train/", views.train, name="newstraining-train")]
