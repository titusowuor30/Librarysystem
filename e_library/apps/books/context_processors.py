from .models import Genre

def menu_genres(request):
    genres = Genre.objects.all()
    return {'menu_genres': genres}

