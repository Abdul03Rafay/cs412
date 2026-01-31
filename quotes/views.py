# views.py
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.

import random

Quotes = [
    {"text": "Stay hungry. Stay foolish.", "author": "Steve Jobs"},
    {"text": "The people who are crazy enough to think they can change the world are the ones who do.", "author": "Steve Jobs"},
    {"text": "Think Different.", "author": "Steve Jobs"},
    {"text": "Your time is limited, so don’t waste it living someone else’s life.", "author": "Steve Jobs"},
    {"text": "Focusing is about saying No.", "author": "Steve Jobs"},
    {"text": "The only way to do great work is to love what you do. If you haven’t found it yet, keep looking. Don’t settle.", "author": "Steve Jobs"},
    {"text": "Don’t let the noise of others’ opinions drown out your own inner voice.", "author": "Steve Jobs"},
    {"text": "Deciding what not to do is as important as deciding what to do.", "author": "Steve Jobs"},
    {"text": "Creativity is just connecting things.", "author": "Steve Jobs"},
    {"text": "Follow your heart and your intuition. They somehow already know what you truly want to become. Everything else is secondary.", "author": "Steve Jobs"},
    {"text": "Design is not just what it looks like and feels like. Design is how it works.", "author": "Steve Jobs"},
    {"text": "Learn continually. There’s always “one more thing” to learn.", "author": "Steve Jobs"}
]

Images = [ 
          "Steve1.jpg",
          "Steve2.jpg",
          "Steve3.jpg",
          "Steve4.jpg",
          "Steve5.jpg",
          "Steve6.jpg",
          "Steve7.jpg",
          "Steve8.jpg",
          "Steve9.jpg",
          "Steve10.jpg",
          "Steve11.jpg",
]

def quote(request: HttpRequest) -> HttpResponse:
    '''
    Define a view to handle the 'quote.html' template.
    '''
    random_quote = random.choice(Quotes)
    random_image = random.choice(Images)
    
    template = 'quotes/quote.html'
    
    context = {
        'quote': random_quote['text'],
        'author': random_quote['author'], 
        'image_path': random_image,
    }
    
    return render(request, template, context)

def about(request: HttpRequest) -> HttpResponse:
    '''Define a view to show the 'about.html' template.'''
    
    template = 'quotes/about.html'
    
    return render(request, template)

def show_all(request: HttpRequest) -> HttpResponse:
    '''Define a view to show the 'show_all.html' template.'''
    
    template = 'quotes/show_all.html'
    
    context = {'quotes': Quotes, 'images': Images} 
    
    return render(request, template, context)