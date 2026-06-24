from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import (
    AuthorForm,
    BookForm,
    CategoryForm,
    GenreForm,
    NoteForm,
    PublisherForm,
    RegisterForm,
    SeriesForm,
    TopicForm,
)
from .models import Author, Book, Category, Genre, Note, Publisher, Series, Topic


def _apply_book_filters(queryset, request):
    genre_ids = request.GET.getlist('genre')
    topic_ids = request.GET.getlist('topic')
    search = request.GET.get('q', '').strip()

    if genre_ids:
        queryset = queryset.filter(genres__id__in=genre_ids).distinct()
    if topic_ids:
        queryset = queryset.filter(topics__id__in=topic_ids).distinct()
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) | Q(isbn__icontains=search)
        )
    return queryset


def index(request):
    all_books = _apply_book_filters(Book.objects.all().order_by('title'), request)
    favorite_books = Book.objects.filter(is_favorite=True).order_by('title')
    read_books = Book.objects.filter(is_read=True).order_by('title')
    genres = Genre.objects.all()
    topics = Topic.objects.all()
    selected_genres = [int(g) for g in request.GET.getlist('genre') if g.isdigit()]
    selected_topics = [int(t) for t in request.GET.getlist('topic') if t.isdigit()]
    return render(request, 'manage_books/index.html.jinja', {
        'books': all_books,
        'favorite_books': favorite_books,
        'read_books': read_books,
        'genres': genres,
        'topics': topics,
        'selected_genres': selected_genres,
        'selected_topics': selected_topics,
        'search_query': request.GET.get('q', ''),
    })


def book_detail(request, book_id):
    book = get_object_or_404(
        Book.objects.prefetch_related('authors', 'genres', 'topics', 'notes'),
        pk=book_id,
    )
    note_form = NoteForm() if request.user.is_authenticated else None
    return render(request, 'manage_books/book.html.jinja', {
        'book': book,
        'note_form': note_form,
    })


@login_required
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Książka została dodana.')
            return redirect('book', book_id=book.pk)
    else:
        form = BookForm()
    return render(request, 'manage_books/book_form.html.jinja', {
        'form': form,
        'title': 'Dodaj nową książkę',
    })


@login_required
def book_edit(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Książka została zaktualizowana.')
            return redirect('book', book_id=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'manage_books/book_form.html.jinja', {
        'form': form,
        'title': 'Edytuj książkę',
        'book': book,
    })


@login_required
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Książka została usunięta.')
        return redirect('index')
    return render(request, 'manage_books/confirm_delete.html.jinja', {
        'object': book,
        'object_label': f'książkę „{book.title}"',
        'cancel_url': reverse('book', kwargs={'book_id': book.pk}),
    })


@login_required
@require_POST
def book_toggle_read(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.is_read = not book.is_read
    book.save()
    return redirect('book', book_id=book.pk)


@login_required
@require_POST
def book_toggle_favorite(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.is_favorite = not book.is_favorite
    book.save()
    return redirect('book', book_id=book.pk)


@login_required
def book_add_note(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.book = book
            note.save()
            messages.success(request, 'Notatka została dodana.')
            return redirect('book', book_id=book.pk)
    return redirect('book', book_id=book.pk)


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    books = author.books.all().order_by('title')
    return render(request, 'manage_books/author.html.jinja', {
        'author': author,
        'books': books,
    })


def publisher_detail(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    books = publisher.book_set.all().order_by('title')
    return render(request, 'manage_books/publisher.html.jinja', {
        'publisher': publisher,
        'books': books,
    })


def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    books = series.book_set.all().order_by('publication_date')
    return render(request, 'manage_books/series.html.jinja', {
        'series': series,
        'books': books,
        'books_count': books.count(),
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Konto zostało utworzone. Witaj!')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'manage_books/register.html.jinja', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'manage_books/login.html.jinja'
    redirect_authenticated_user = True


def logout_view(request):
    logout(request)
    messages.info(request, 'Wylogowano pomyślnie.')
    return redirect('index')


# --- Dictionary management ---

def _entity_form_view(request, model, form_class, list_url_name, entity_label, pk=None):
    instance = get_object_or_404(model, pk=pk) if pk else None

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            action = 'zaktualizowano' if instance else 'dodano'
            messages.success(request, f'{entity_label} została {action}.')
            if request.POST.get('next'):
                return redirect(request.POST['next'])
            return redirect(list_url_name)
    else:
        form = form_class(instance=instance)

    title = f'Edytuj {entity_label.lower()}' if instance else f'Dodaj {entity_label.lower()}'
    next_url = request.GET.get('next', '')
    return render(request, 'manage_books/entity_form.html.jinja', {
        'form': form,
        'title': title,
        'list_url': list_url_name,
        'next_url': next_url,
    })


def _handle_entity_delete(request, model, pk, list_url_name, entity_label):
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, f'{entity_label} została usunięta.')
        return redirect(list_url_name)
    return render(request, 'manage_books/confirm_delete.html.jinja', {
        'object': obj,
        'object_label': f'{entity_label.lower()} „{obj}"',
        'cancel_url': reverse(list_url_name),
    })


@login_required
def author_list(request):
    authors = Author.objects.all().order_by('last_name', 'first_name')
    return render(request, 'manage_books/entity_list.html.jinja', {
        'items': authors,
        'title': 'Autorzy',
        'add_url': 'author_add',
        'edit_url_name': 'author_edit',
        'delete_url_name': 'author_delete',
        'detail_type': 'author',
    })


@login_required
def author_add(request):
    return _entity_form_view(request, Author, AuthorForm, 'author_list', 'Autora')


@login_required
def author_edit(request, pk):
    return _entity_form_view(request, Author, AuthorForm, 'author_list', 'Autora', pk=pk)


@login_required
def author_delete(request, pk):
    return _handle_entity_delete(request, Author, pk, 'author_list', 'Autor')


@login_required
def publisher_list(request):
    publishers = Publisher.objects.all().order_by('name')
    return render(request, 'manage_books/entity_list.html.jinja', {
        'items': publishers,
        'title': 'Wydawcy',
        'add_url': 'publisher_add',
        'edit_url_name': 'publisher_edit',
        'delete_url_name': 'publisher_delete',
        'detail_type': 'publisher',
    })


@login_required
def publisher_add(request):
    next_url = request.GET.get('next', 'publisher_list')
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wydawca został dodany.')
            return redirect(request.POST.get('next', 'publisher_list'))
    else:
        form = PublisherForm()
    return render(request, 'manage_books/entity_form.html.jinja', {
        'form': form,
        'title': 'Dodaj wydawcę',
        'list_url': 'publisher_list',
        'next_url': next_url,
    })


@login_required
def publisher_edit(request, pk):
    return _entity_form_view(request, Publisher, PublisherForm, 'publisher_list', 'Wydawcę', pk=pk)


@login_required
def publisher_delete(request, pk):
    return _handle_entity_delete(request, Publisher, pk, 'publisher_list', 'Wydawca')


@login_required
def series_list(request):
    items = Series.objects.all().order_by('name')
    return render(request, 'manage_books/entity_list.html.jinja', {
        'items': items,
        'title': 'Serie',
        'add_url': 'series_add',
        'edit_url_name': 'series_edit',
        'delete_url_name': 'series_delete',
        'detail_type': 'series',
    })


@login_required
def series_add(request):
    return _entity_form_view(request, Series, SeriesForm, 'series_list', 'Serię')


@login_required
def series_edit(request, pk):
    return _entity_form_view(request, Series, SeriesForm, 'series_list', 'Serię', pk=pk)


@login_required
def series_delete(request, pk):
    return _handle_entity_delete(request, Series, pk, 'series_list', 'Seria')


@login_required
def genre_list(request):
    items = Genre.objects.all().order_by('name')
    return render(request, 'manage_books/entity_list.html.jinja', {
        'items': items,
        'title': 'Gatunki',
        'add_url': 'genre_add',
        'edit_url_name': 'genre_edit',
        'delete_url_name': 'genre_delete',
        'detail_type': None,
    })


@login_required
def genre_add(request):
    return _entity_form_view(request, Genre, GenreForm, 'genre_list', 'Gatunek')


@login_required
def genre_edit(request, pk):
    return _entity_form_view(request, Genre, GenreForm, 'genre_list', 'Gatunek', pk=pk)


@login_required
def genre_delete(request, pk):
    return _handle_entity_delete(request, Genre, pk, 'genre_list', 'Gatunek')


@login_required
def topic_list(request):
    items = Topic.objects.all().order_by('name')
    return render(request, 'manage_books/entity_list.html.jinja', {
        'items': items,
        'title': 'Tematy',
        'add_url': 'topic_add',
        'edit_url_name': 'topic_edit',
        'delete_url_name': 'topic_delete',
        'detail_type': None,
    })


@login_required
def topic_add(request):
    return _entity_form_view(request, Topic, TopicForm, 'topic_list', 'Temat')


@login_required
def topic_edit(request, pk):
    return _entity_form_view(request, Topic, TopicForm, 'topic_list', 'Temat', pk=pk)


@login_required
def topic_delete(request, pk):
    return _handle_entity_delete(request, Topic, pk, 'topic_list', 'Temat')


@login_required
def category_list(request):
    items = Category.objects.all().order_by('name')
    return render(request, 'manage_books/entity_list.html.jinja', {
        'items': items,
        'title': 'Działy',
        'add_url': 'category_add',
        'edit_url_name': 'category_edit',
        'delete_url_name': 'category_delete',
        'detail_type': None,
    })


@login_required
def category_add(request):
    return _entity_form_view(request, Category, CategoryForm, 'category_list', 'Dział')


@login_required
def category_edit(request, pk):
    return _entity_form_view(request, Category, CategoryForm, 'category_list', 'Dział', pk=pk)


@login_required
def category_delete(request, pk):
    return _handle_entity_delete(request, Category, pk, 'category_list', 'Dział')


@login_required
def author_add_quick(request):
    next_url = request.GET.get('next', 'book_add')
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autor został dodany.')
            return redirect(request.POST.get('next', 'book_add'))
    else:
        form = AuthorForm()
    return render(request, 'manage_books/entity_form.html.jinja', {
        'form': form,
        'title': 'Dodaj autora',
        'list_url': 'author_list',
        'next_url': next_url,
    })
