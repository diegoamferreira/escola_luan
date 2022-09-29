import random

from django.core.management.base import BaseCommand

from core.models import Professor, Materia, Escola


def set_escolas_professor():
    escolas = Escola.objects.all()
    professores = list(Professor.objects.values_list('id', flat=True))
    for escola in escolas:
        professores_aleatorios = random.sample(professores, 8)
        escola.professores.set(professores_aleatorios)


class Command(BaseCommand):
    help = 'Create data.'

    def handle(self, *args, **options):
        set_escolas_professor()
        print('Escola FINALIZADAS')
