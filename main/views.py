from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages

# Create your views here.
def index(request):
    # context={
    #     'title': 'Главная страница',
    #     'values': ['some', 'hi', 123]
    # }
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')