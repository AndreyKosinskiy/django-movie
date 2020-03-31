from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from .models import Actor, Category, Genre, Movie, RatingStar, Reviews, Rating, MovieShots
from ckeditor_uploader.widgets import CKEditorUploadingWidget 
# Register your models here.





class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label = "Описание", widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Категории """
    list_display = ('id','name','url')
    list_display_links = ('name',)

class ReviewsInline(admin.TabularInline):
    """ Коментарии к фильму в админку фильма """
    model = Reviews
    extra = 1
    readonly_fields = ('name','email')

class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self,obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110">')

    get_image.short_description = "Изображение"

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """ Фильмы """
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category','year')
    search_fields = ('title','category__name' )
    inlines = [MovieShotsInline, ReviewsInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    readonly_fields = ('get_image',)
    fieldsets = (
        (None,{
            'fields':(('title','tagline'),)
        }),
        (None,{
            'fields':('description',('poster','get_image'))
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
    def get_image(self,obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110">')

    get_image.short_description = "Постер"

    def unpublish(self,request,queryset):
        """ Снять с публикации """
        row_update = queryset.update(draft = True)
        if row_update == 1:
            message_bit = ' 1 запись была обновлена'
        else:
            message_bit = f' {row_update} записи были обновлены'
        self.message_user(request,f'{message_bit}')

    def publish(self,request,queryset):
        """ Опубликовать """
        row_update = queryset.update(draft = False)
        if row_update == 1:
            message_bit = ' 1 запись была обновлена'
        else:
            message_bit = f' {row_update} записи были обновлены'
        self.message_user(request,f'{message_bit}')

    publish.short_description  = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description  = "Снять с публикации"
    unpublish.allowed_permissions = ('change', )


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """ Коментарии """
    list_display = ('name','email','parent','movie','id')
    readonly_fields = ('name','email')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """ Актеры и рижессеры """
    list_display = ('name','age','get_image')
    fields = ('name','age','get_image')
    readonly_fields = ('get_image',)
    def get_image(self,obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = "Изображение"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """ Жанры """
    fields = ('name','url')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """ Рейтинг """
    fields = ('ip','star','movie')

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """ Кадры из фильмов """
    fields = ('title','get_image','movie')

    def get_image(self,obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = "Изображение"

admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"