from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from django.views.generic import View, ListView, DetailView
from .models import Movie, Actor,Genre,Rating
from .forms import ReviewForm, RaitingForm
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
    paginate_by = 3

class MovieDetailView(GenreYear,DetailView):
    """ Информация про фильм """
    model = Movie
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = self.get_client_ip(self.request)
        instance = Rating.objects.get(movie_id =  context["movie"].id, ip = ip )
        context["star_form"] = RaitingForm()
        print(instance.star.value)
        context['checked_id'] = instance.star.value

        return context

    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split('.')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

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
    paginate_by = 3

    def get_queryset(self):
        queryset = Movie.objects.filter(Q(year__in = self.request.GET.getlist('year')) | Q(genres__in = self.request.GET.getlist('genre'))).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year"] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        context["ganre"] =''.join([f'year={x}&' for x in self.request.GET.getlist('ganre')])
        return context
    

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

class AddRatingStar(View):
    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split('.')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RaitingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id = int(request.POST.get("movie")),
                defaults = {'star_id':int(request.POST.get('star'))}
            )
            return JsonResponse({"checked_id":request.POST.get('star')},status=201) #HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class Search(ListView):
    paginate_by = 2

    def get_queryset(self, *args, **kwargs):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = f'q={self.request.GET.get("q")}'
        return context
    
