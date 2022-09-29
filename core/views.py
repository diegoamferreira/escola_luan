from django.shortcuts import render
from django.views.generic import ListView

from core.models import Aluno


# Create your views here.


class AlunoListView(ListView):
    model = Aluno
    template_name = 'core/aluno_list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = super(AlunoListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(nome__icontains=search)
        return queryset


