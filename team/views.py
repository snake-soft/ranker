from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse

from .models import Team


class TeamList(ListView):
    model = Team


class TeamDetails(DetailView):
    model = Team


class TeamCreate(CreateView):
    model = Team
    fields = ['teamname', 'players']

    def get_initial(self):
        self.success_url = reverse('team-list')
        # self.success_url = self.request.path
        initial = super(CreateView, self).get_initial()
        initial = initial.copy()

        if 'players' in self.request.GET:
            initial['players'] = [int(x) for x in self.request.GET['players'].split(',')]
        return initial

    def post(self, request):
        return super().post(request)
