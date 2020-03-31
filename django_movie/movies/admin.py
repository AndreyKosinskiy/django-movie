from django.contrib import admin
from .models import Actor, Category, Genre, Movie, RatingStar, Reviews, Rating, MovieShots
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','url')
    list_display_links = ('name',)

class ReviewsInline(admin.StackedInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name','email')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category','year')
    search_fields = ('title','category__name' )
    inlines = [ReviewsInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    fieldsets = (
        (None,{
            'fields':(('title','tagline'),)
        }),
        (None,{
            'fields':('description','poster')
        }),
        (None,{
            'fields':(('year','world_premiere','country'),)
        }),
        (None,{
            'fields':(('actors','diretors','genres','category'),)
        }),
        ("Actors",{
            'classes':('collapse',),
            'fields':(('budget','fees_in_usa','fees_in_world'),)
        }),
        ("Options",{
            'fields':(('url','draft'),)
        }),

    )

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name','email','parent','movie','id')
    readonly_fields = ('name','email')



@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    fields = ('name','age')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ('name','url')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    fields = ('ip','star','movie')

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    fields = ('title','image','movie')


admin.site.register(RatingStar)
