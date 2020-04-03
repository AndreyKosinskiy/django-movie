from django.urls import path

from . import views

urlpatterns = [
    path('',views.MovieViews.as_view()),
    path('filter/', views.FilterListView.as_view(), name= 'filter'),
    path('jsonfilter/', views.JsonFilterListView.as_view(), name= 'json_filter'),
    path('<slug:slug>/',views.MovieDetailView.as_view(), name = 'movie_detail'),
    path('review/<int:pk>/',views.AddReview.as_view(), name = 'add_review'),
    path('actor/<str:slug>/',views.ActorDetailView.as_view(), name = 'actor_detail'),
]
