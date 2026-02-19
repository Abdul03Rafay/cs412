#File: blog/urls.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/19/2026
# Description: Python file to define/map URL patterns.

from django.urls import path
from .views import * #all the views

urlpatterns = [
    # map the URL (empty string) to the view
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name='show_all'),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),
    path('article/create', CreateArticleView.as_view(), name="create_article"),
    #path('create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
]
