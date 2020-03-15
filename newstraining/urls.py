from django.urls import path
from . import views
from .views import NewsArticlePredictionFormView, NewsArticleTrainingFormView,RunDetailsListView

urlpatterns = [
    path("train/", NewsArticleTrainingFormView.as_view(), name="newstraining-train"),
    path("predict/",NewsArticlePredictionFormView.as_view(),name="newsarticles-prediction"),
    path("ajax/load-job-codes/",views.load_job_codes,name="ajax_load_job_codes"),
    path("recent_run_detail/",RunDetailsListView.as_view(),name="newstraining-rundetails"),
]