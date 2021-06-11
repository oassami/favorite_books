from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add_book),
    path('clear', views.clear_add),
    path('<int:book_id>', views.display),
    path('favorite/<int:book_id>', views.favorite),
    path('unfavorite/<int:book_id>', views.unfavorite),
    path('update/<int:book_id>', views.update),
    path('delete/<int:book_id>', views.delete),
]
