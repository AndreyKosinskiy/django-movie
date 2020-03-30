from django.urls import path

from . import views

urlpatterns = [
    path('',views.MovieViews.as_view())
]
