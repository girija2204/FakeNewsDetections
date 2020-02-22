from django.urls import re_path
from .views import (
    NewsArticlesListView,
    NewsArticlesCreateView,
    NewsArticlesDetailView,
    NewsArticlesDeleteView,
    NewsArticlesUpdateView,
)

urlpatterns = [
    re_path(r'^$', NewsArticlesListView.as_view(), name='portal-home'),
    re_path(r'^new/', NewsArticlesCreateView.as_view(), name='newsarticles-create'),
    re_path(
        r'^news/<int:pk>/', NewsArticlesDetailView.as_view(), name='newsarticles-detail'
    ),
    re_path(
        r'^news/<int:pk>/delete/',
        NewsArticlesDeleteView.as_view(),
        name='newsarticles-delete',
    ),
    re_path(
        r'^news/<int:pk>/update/',
        NewsArticlesUpdateView.as_view(),
        name='newsarticles-update',
    ),
]
