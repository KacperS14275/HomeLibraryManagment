from django.shortcuts import render, get_object_or_404
from .models import Book, Author, Publisher, Series, Genre, Topic

def index(request):
    # Pobieramy dane dla Scenariusza 1
    context = {
        'all_books': Book.objects.all(),
        'favorite_books': Book.objects.filter(is_favorite=True),
        'genres': Genre.objects.all(),
        'topics': Topic.objects.all(),
    }
    return render(request, 'manage_books/index.html.jinja', context)

def book(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    return render(request, 'manage_books/book.html.jinja', {'book': book_obj})

def author(request, author_id):
    author_obj = get_object_or_404(Author, id=author_id)
    return render(request, 'manage_books/author.html.jinja', {'author': author_obj})

def publisher(request, publisher_id):
    pub_obj = get_object_or_404(Publisher, id=publisher_id)
    return render(request, 'manage_books/publisher.html.jinja', {'publisher': pub_obj})

def series(request, series_id):
    series_obj = get_object_or_404(Series, id=series_id)
    return render(request, 'manage_books/series.html.jinja', {'series': series_obj})

def note(request, note_id):
    # To zazwyczaj służy do edycji notatki, ale na razie wyświetlamy
    return render(request, 'manage_books/note.html.jinja', {'note_id': note_id})