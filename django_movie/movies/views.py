from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View, ListView, DetailView
from .models import Movie, Actor,Genre
from .forms import ReviewForm
from django.db.models import Q
# Create your views here.


class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")

class MovieViews(GenreYear,ListView):
    """ Вывов списка фильмов """
    model = Movie
    queryset = Movie.objects.filter(draft=False)

class MovieDetailView(GenreYear,DetailView):
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
            if request.POST.get('parent',None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())

class ActorDetailView(DetailView):
    """ Детали Актёра или режиссера """
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'

class FilterListView(GenreYear,ListView):
    """ Фильтр Фильмов """
    def get_queryset(self):
        queryset = Movie.objects.filter(Q(year__in = self.request.GET.getlist('year')) | Q(genres__in = self.request.GET.getlist('genre')))
        return queryset

class JsonFilterListView(ListView):
    """ Фильтр Фильмов """
    model = Movie

    def get_queryset(self):
        queryset = Movie.objects.filter(Q(year__in = self.request.GET.getlist('year')) | 
                                        Q(genres__in = self.request.GET.getlist('genre'))
                                        ).distinct().values('title','tagline','url','poster')
        return queryset
    
    def get(self,request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({'movies':queryset}, safe=False)