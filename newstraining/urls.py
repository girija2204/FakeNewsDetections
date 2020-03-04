from django.urls import path
from . import views
from .views import NewsArticlePredictionFormView, NewsArticleTrainingFormView

urlpatterns = [
    path("train/", NewsArticleTrainingFormView.as_view(), name="newstraining-train"),
    # path("train/", views.train, name="newstraining-train"),
    path(
        "predict/",
        NewsArticlePredictionFormView.as_view(),
        name="newsarticles-prediction",
    ),
    # path("predict/detail",NewsArticlePredictionDetailView.as_view(),name="detail")
    path("ajax/load-job-codes/",views.load_job_codes,name="ajax_load_job_codes"),
]
