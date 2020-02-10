from django.urls import path
from . import views
from .views import NewsArticlePredictionFormView

urlpatterns = [
    path("train/", views.train, name="newstraining-train"),
    path(
        "predict/",
        NewsArticlePredictionFormView.as_view(),
        name="newsarticles-prediction",
    ),
]
