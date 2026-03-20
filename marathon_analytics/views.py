from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from . models import Result
 
class ResultsListView(ListView):
    '''View to display marathon results'''
 
    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 50
 
    def get_queryset(self):
        
        # start with entire queryset
        results = super().get_queryset().order_by('place_overall')
 
 
        # filter results by these field(s):
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            if city:
                results = results.filter(city=city)
                
        return results