from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from .models import Movie
from .forms import ReviewForm
# Create your views here.

class MovieViews(ListView):
    """ Вывов списка фильмов """
    model = Movie
    queryset = Movie.objects.filter(draft=False)

class MovieDetailView(DetailView):
    """ Информация про фильм """
    model = Movie
    slug_field = 'url'

class AddReview(View):
    """ Отзыв """
    def post(self, request, pk):
        movie = Movie.objects.get(id = pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())
