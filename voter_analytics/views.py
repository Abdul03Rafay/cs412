# File: voter_analytics/views.py
# Author: Abdul Rafay (rafaya@bu.edu), 3/20/2026
# Description: Views for the voter_analytics app, including list and detail views.

from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Q, Count
import plotly.express as px
import plotly.offline as op

class VoterFilterMixin:
    '''Mixin to provide shared filtering logic and context data for voters.'''
    
    def get_queryset(self):
        '''Filter the queryset based on search criteria.'''
        queryset = Voter.objects.all()

        # filter by party affiliation
        party = self.request.GET.get('party')
        if party:
            queryset = queryset.filter(party_affiliation=party)

        # filter by min date of birth (year)
        min_year = self.request.GET.get('min_dob')
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=min_year)

        # filter by max date of birth (year)
        max_year = self.request.GET.get('max_dob')
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=max_year)

        # filter by voter score
        score = self.request.GET.get('voter_score')
        if score:
            queryset = queryset.filter(voter_score=score)

        # filter by elections voted in
        for election in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if self.request.GET.get(election):
                queryset = queryset.filter(**{election: True})

        return queryset

    def get_context_data(self, **kwargs):
        '''Provide unique party affiliations, years, and scores for the filtering form.'''
        context = super().get_context_data(**kwargs)
        
        # provide unique party affiliations for the dropdown
        context['parties'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        
        # provide range of years for DOB dropdowns
        context['years'] = range(1900, 2025)
        
        # provide voter scores (0-5)
        context['scores'] = range(6)
        
        return context

class VoterListView(VoterFilterMixin, ListView):
    '''View to display a list of voters with filtering options.'''
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

class VoterDetailView(DetailView):
    '''View to display details of a single voter.'''
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterGraphsView(VoterFilterMixin, ListView):
    '''View to display graphs of aggregate voter data.'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    # No pagination - graphs use the full queryset via get_queryset()

    def get_context_data(self, **kwargs):
        '''Generate graphs and add them to context.'''
        context = super().get_context_data(**kwargs)
        # Always work on the FULL filtered queryset (not paginated)
        voters = self.get_queryset()

        if not voters.exists():
            context['birth_year_graph'] = "<p>No data found for the selected criteria.</p>"
            context['party_graph'] = ""
            context['election_graph'] = ""
            return context

        # 1. Bar chart: Distribution of Voters by Year of Birth
        # Pre-aggregate at DB level: group by year, count per year
        year_counts = (voters
                       .values('date_of_birth__year')
                       .annotate(count=Count('id'))
                       .order_by('date_of_birth__year'))
        birth_years = [row['date_of_birth__year'] for row in year_counts]
        birth_counts = [row['count'] for row in year_counts]

        fig1 = px.bar(x=birth_years, y=birth_counts,
                      labels={'x': 'Year of Birth', 'y': 'Number of Voters'},
                      title='Distribution of Voters by Year of Birth')
        fig1.update_layout(xaxis_title="Year of Birth", yaxis_title="Number of Voters",
                           bargap=0.1)
        context['birth_year_graph'] = op.plot(fig1, output_type='div', include_plotlyjs='cdn')

        # 2. Pie chart: Distribution by Party Affiliation
        party_counts = (voters
                        .values('party_affiliation')
                        .annotate(count=Count('id'))
                        .order_by('-count'))
        parties = [p['party_affiliation'].strip() for p in party_counts]
        p_counts = [p['count'] for p in party_counts]

        fig2 = px.pie(names=parties, values=p_counts,
                      title='Voter Distribution by Party Affiliation')
        fig2.update_traces(textinfo='none')
        context['party_graph'] = op.plot(fig2, output_type='div', include_plotlyjs=False)

        # 3. Bar chart: Count of voters who participated in each election
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_labels = {
            'v20state': '2020 State',
            'v21town': '2021 Town',
            'v21primary': '2021 Primary',
            'v22general': '2022 General',
            'v23town': '2023 Town',
        }
        agg_kwargs = {field: Count('pk', filter=Q(**{field: True})) for field in election_fields}
        agg_results = voters.aggregate(**agg_kwargs)

        labels = [election_labels[f] for f in election_fields]
        values = [agg_results[f] for f in election_fields]

        fig3 = px.bar(x=labels, y=values,
                      labels={'x': 'Election', 'y': 'Number of Voters'},
                      title='Voter Participation by Election')
        fig3.update_layout(xaxis_title="Election", yaxis_title="Number of Voters")
        context['election_graph'] = op.plot(fig3, output_type='div', include_plotlyjs=False)

        return context
