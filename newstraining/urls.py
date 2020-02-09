from django.urls import path
from . import views
from .views import NewsArticlePredictionView

urlpatterns = [
    path("train/", views.train, name="newstraining-train"),
    path(
        "predict/", NewsArticlePredictionView.as_view(), name="newsarticles-prediction"
    ),
]
