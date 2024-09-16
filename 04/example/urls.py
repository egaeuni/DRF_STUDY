from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('books', BookViewSet)

urlpatterns = [
    path("hello/", HelloAPI),
    path("fbv/books/", booksAPI),
    path('fbv/book/<int:bid>/', bookAPI),
    path('cbv/books/', BooksAPI.as_view()),
    path('cbv/book/<int:bid>/', BookAPI.as_view()),
    path('mixins/books/', BooksAPIMixins.as_view()),
    path('mixins/book/<int:bid>/', BookAPIMixins.as_view()),
    path('generics/books/', BooksAPIGenerics.as_view()),
    path('generics/book/<int:bid>/', BookAPIGenerics.as_view()),
    ]

urlpatterns += router.urls