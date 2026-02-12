from .models import Article
from django.views.generic import ListView, DetailView
import random

# Create your views here.
class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Article
    template_name = 'blog/show_all.html' ## reusing same template
    context_object_name = 'articles'
class ArticleView(DetailView):
    '''Display single article.'''
    model = Article
    template_name = 'blog/article.html' ## reusing same template
    context_object_name = 'article'
class RandomArticleView(DetailView):
    '''Display randomly selected single article.'''
    model = Article
    template_name = 'blog/article.html' ## reusing same template
    context_object_name = 'article'
    
    def get_object(self):
        '''Return one Article object chosen at random.'''
        all_articles = Article.objects.all()
        return random.choice(all_articles)