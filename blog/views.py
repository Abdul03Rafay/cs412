from .models import Article
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse
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
class CreateArticleView(CreateView): 
    '''A view to handle creation of a new Article.
    (1) display the HTMl form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''
    
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"
    
class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''
    
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
    
        # calling the superclass method
        context = super().get_context_data()
        
        # find/add the article to the context data
        # retrive the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        
        # add this article into the context dictionary:
        context['article'] = article
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the new object to the Django database. 
        We need to add the foreign key (of the Article). to the Comment object before saving it to the database.'''
        
        #instrument our code to display form fields:
        print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        #attach this article to the comment
        form.instance.article = article # set the FK
        
        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        
        
        # create and return a URL:
        # return reverse('show_all')
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('article', kwargs={'pk':pk})
    
   
    