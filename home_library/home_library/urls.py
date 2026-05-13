"""
URL configuration for home_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from manage_books import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:book_id>/', views.book, name='book'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('publisher/<int:publisher_id>/', views.publisher, name='publisher'),
    path('series/<int:series_id>/', views.series, name='series'),
    path('note/<int:note_id>/', views.note, name='note')
]
