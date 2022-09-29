from django.urls import path

from core.views import AlunoListView

urlpatterns = [
    path('', AlunoListView.as_view(), name='aluno_list'),
]
