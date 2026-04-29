from django.db import models
import pytz


class Book(models.Model):
    COVERS = [
        ('hardcover', 'Hardcover'),
        ('paperback', 'Paperback'),
        ('ebook', 'E-book'),
        ('audiobook', 'Audiobook'),
    ]

    LANGUAGES = [
        ('english', 'English'),
        ('spanish', 'Spanish'),
        ('french', 'French'),
        ('polish', 'Polish'),
        ('hebrew', 'Hebrew'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20)
    publication_date = models.DateField()
    pages = models.IntegerField()
    cover = models.ImageField(upload_to='covers/')
    language = models.CharField(max_length=50, choices=LANGUAGES)
    is_read = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    author = models.ManyToManyField('Author', related_name='books', blank=True)  # ✅ usunięto on_delete
    publisher = models.ForeignKey('Publisher', on_delete=models.RESTRICT)
    series = models.ForeignKey('Series', on_delete=models.RESTRICT, blank=True, null=True)
    genres = models.ManyToManyField('Genre', related_name='books', blank=True)   # ✅ usunięto on_delete
    topics = models.ManyToManyField('Topic', related_name='books', blank=True)   # ✅ usunięto on_delete
    # ✅ notes jest już zdefiniowane przez related_name w klasie Note — usuń to pole stąd


class Author(models.Model):
    TITLES = [
        ('mr', 'Mr.'),
        ('ms', 'Ms.'),
        ('dr', 'Dr.'),
        ('prof', 'Prof.'),
        ('ks', 'Ks.'),
        ('bp', 'Bp.'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=50)
    title = models.CharField(max_length=100, choices=TITLES, blank=True, null=True)
    # ✅ Nie definiuj tu books ani series — M2M wystarczy zdefiniować po jednej stronie
    series = models.ManyToManyField('Series', related_name='authors', blank=True)  # ✅ usunięto on_delete


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=2, choices=pytz.country_names.items())
    foundation_year = models.IntegerField()
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    # ✅ ManyToOneField nie istnieje — relacja Publisher->Book jest przez ForeignKey w Book


class Genre(models.Model):
    name = models.CharField(max_length=50)
    # ✅ M2M zdefiniowane już w Book, nie trzeba tu powtarzać


class Series(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # ✅ Relacje do Book i Author już zdefiniowane po ich stronie


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # ✅ M2M zdefiniowane już w Book


class Note(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='notes')  # ✅ usunięto duplikat
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()