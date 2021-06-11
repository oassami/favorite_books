from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    if 'logged_in' not in request.session:
        return redirect('/')
    all_books = Book.objects.all()
    context={'books_info': []}
    for book in all_books:
        uploaded_by = Book.objects.get(id=book.id).uploaded_by
        uploaded_by_full_name = uploaded_by.first_name + ' ' + uploaded_by.last_name
        book_title = '<a href="/books/'+str(book.id)+'">'+book.title+'</a>'
        try:
            User.objects.get(id=request.session['user_id']).like_books.get(id=book.id)
            liked_by_me = "this is one of your favorites"
        except:
            liked_by_me = '<a href="/books/favorite/'+str(book.id)+'">Add to Favotires</a>'
        context['books_info'].append([book_title, uploaded_by_full_name, liked_by_me])
    return render(request, 'books.html', context)

def add_book(request):
    request.session['title'] = request.POST['title']
    request.session['description'] = request.POST['description']
    errors = Book.objects.addValidation(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    this_user = User.objects.get(id=request.session['user_id'])
    this_book = Book.objects.create(title=request.POST['title'], desc=request.POST['description'], uploaded_by=this_user)
    this_book.favorites.add(this_user)
    del request.session['title']
    del request.session['description']
    return redirect('/books')

def clear_add(request):
    if 'title' in request.session:
        del request.session['title']
    if 'description' in request.session:
        del request.session['description']
    return redirect('/books')

def display(request, book_id):
    uploaded_by = Book.objects.get(id=book_id).uploaded_by
    all_favorties = Book.objects.get(id=book_id).favorites.all()
    try:
        Book.objects.get(id=book_id).favorites.get(id=request.session['user_id'])
        favored_it = True
        print('favored_it: True')
    except:
        favored_it = False
        print('favored_it: False')

    if uploaded_by.id == request.session['user_id']:
        log_user_uploaded= True
        print('log_user_uploaded: True')
    else:
        log_user_uploaded= False
        print('log_user_uploaded: False')
    context = {
        'this_book': Book.objects.get(id=book_id),
        'uploaded_by': uploaded_by,
        'all_favorites': all_favorties,
        'log_user_uploaded': log_user_uploaded,
        'favored_it': favored_it
    }
    
    return render(request, 'display.html', context)

def favorite(request, book_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_book = Book.objects.get(id=book_id)
    this_book.favorites.add(this_user)
    return redirect('/books')

def unfavorite(request, book_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_book = Book.objects.get(id=book_id)
    this_book.favorites.remove(this_user)
    return redirect(f'/books/{book_id}')

def update(request, book_id):
    errors = Book.objects.updateValidation(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/{book_id}')
    this_book = Book.objects.get(id=book_id)
    this_book.title=request.POST['title']
    this_book.desc=request.POST['description']
    this_book.save()
    return redirect(f'/books/{book_id}')

def delete(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_book.delete()
    return redirect('/books')