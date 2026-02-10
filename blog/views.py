from django.shortcuts import render
from .models import Article
from django.views.generic import ListView

# Create your views here.

class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'
