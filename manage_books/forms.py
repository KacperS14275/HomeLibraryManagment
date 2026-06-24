from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Author, Book, Category, Genre, Note, Publisher, Series, Topic

INPUT_CLASS = 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-400'


class RegisterForm(UserCreationForm):
  email = forms.EmailField(required=True)

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']


class BookForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = [
      'title', 'isbn', 'publication_date', 'pages', 'cover', 'language',
      'publisher', 'series', 'category', 'authors', 'genres', 'topics',
    ]
    widgets = {
      'title': forms.TextInput(attrs={'class': INPUT_CLASS}),
      'isbn': forms.TextInput(attrs={'class': INPUT_CLASS}),
      'publication_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASS}),
      'pages': forms.NumberInput(attrs={'class': INPUT_CLASS}),
      'cover': forms.Select(attrs={'class': INPUT_CLASS}),
      'language': forms.Select(attrs={'class': INPUT_CLASS}),
      'publisher': forms.Select(attrs={'class': INPUT_CLASS}),
      'series': forms.Select(attrs={'class': INPUT_CLASS}),
      'category': forms.Select(attrs={'class': INPUT_CLASS}),
      'authors': forms.CheckboxSelectMultiple,
      'genres': forms.CheckboxSelectMultiple,
      'topics': forms.CheckboxSelectMultiple,
    }


class NoteForm(forms.ModelForm):
  class Meta:
    model = Note
    fields = ['content']
    widgets = {
      'content': forms.Textarea(attrs={'rows': 4, 'class': 'w-full border rounded px-3 py-2'}),
    }


class AuthorForm(forms.ModelForm):
  class Meta:
    model = Author
    fields = ['first_name', 'last_name', 'nationality', 'title', 'alias']


class PublisherForm(forms.ModelForm):
  class Meta:
    model = Publisher
    fields = ['name', 'country', 'founded_year', 'website', 'email']
    widgets = {
      'founded_year': forms.NumberInput(attrs={'min': 1000, 'max': 2100}),
    }


class SeriesForm(forms.ModelForm):
  class Meta:
    model = Series
    fields = ['name', 'description']
    widgets = {
      'description': forms.Textarea(attrs={'rows': 3}),
    }


class GenreForm(forms.ModelForm):
  class Meta:
    model = Genre
    fields = ['name']


class TopicForm(forms.ModelForm):
  class Meta:
    model = Topic
    fields = ['name', 'description']
    widgets = {
      'description': forms.Textarea(attrs={'rows': 3}),
    }


class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ['name']
