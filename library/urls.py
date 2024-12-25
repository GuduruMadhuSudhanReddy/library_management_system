from django.urls import path
from .views import *
urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('books/add/', add_book, name='add_book'),
    path('authors/', author_list, name='author_list'),
    path('authors/add/', add_author, name='add_author'),
    path('categories/', category_list, name='category_list'),
    path('categories/add/', add_category, name='add_category'),
    path('loan/', loan_book, name='loan_book'),
    path('return/', return_book, name='return_book'),
    path('loans/', loan_list, name='loan_list'),
    path('', library_list, name='library_list'),
    path('signup/', signup_view, name='signup_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('dashboard/',dashboard_view, name='dashboard_view')
]
