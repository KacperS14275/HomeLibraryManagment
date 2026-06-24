from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('book/add/', views.book_add, name='book_add'),
    path('book/<int:book_id>/', views.book_detail, name='book'),
    path('book/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('book/<int:book_id>/toggle-read/', views.book_toggle_read, name='book_toggle_read'),
    path('book/<int:book_id>/toggle-favorite/', views.book_toggle_favorite, name='book_toggle_favorite'),
    path('book/<int:book_id>/add-note/', views.book_add_note, name='book_add_note'),

    path('author/<int:author_id>/', views.author_detail, name='author'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/add/', views.author_add, name='author_add'),
    path('authors/add-quick/', views.author_add_quick, name='author_add_quick'),
    path('authors/<int:pk>/edit/', views.author_edit, name='author_edit'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),

    path('publisher/<int:publisher_id>/', views.publisher_detail, name='publisher'),
    path('publishers/', views.publisher_list, name='publisher_list'),
    path('publishers/add/', views.publisher_add, name='publisher_add'),
    path('publishers/<int:pk>/edit/', views.publisher_edit, name='publisher_edit'),
    path('publishers/<int:pk>/delete/', views.publisher_delete, name='publisher_delete'),

    path('series/<int:series_id>/', views.series_detail, name='series'),
    path('series/', views.series_list, name='series_list'),
    path('series/add/', views.series_add, name='series_add'),
    path('series/<int:pk>/edit/', views.series_edit, name='series_edit'),
    path('series/<int:pk>/delete/', views.series_delete, name='series_delete'),

    path('genres/', views.genre_list, name='genre_list'),
    path('genres/add/', views.genre_add, name='genre_add'),
    path('genres/<int:pk>/edit/', views.genre_edit, name='genre_edit'),
    path('genres/<int:pk>/delete/', views.genre_delete, name='genre_delete'),

    path('topics/', views.topic_list, name='topic_list'),
    path('topics/add/', views.topic_add, name='topic_add'),
    path('topics/<int:pk>/edit/', views.topic_edit, name='topic_edit'),
    path('topics/<int:pk>/delete/', views.topic_delete, name='topic_delete'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
