from django.shortcuts import render, redirect

def index(request):
    if 'logged-in' not in request.session:
        return redirect('/')
    return render(request, 'books.html')
