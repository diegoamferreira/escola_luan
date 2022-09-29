import random

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
import requests
import pandas as pd
import numpy as np

from core.models import Aluno, Professor, Diretor, Estado, Cidade, Escola, Aula, Materia
from utils.progress_bar import progressbar

fake = Faker()

materias = [
    'Matemática',
    'Biografia',
    'Inglês',
    'Química',
    'Espanhol',
    'Biologia',
    'Gramática',
    'Filosofia',
    'História',
    'Educação Física',
    'Geografia',
    'História da América',
    'História do Brasil',
    'História Geral',
    'Geografia do Brasil',
    'Italiano',
    'Português',
    'Literatura',
    'Física',
    'Artes',
    'Redação',
    'Sociologia',
    'Curiosidades',
    'Dicas de estudo',
    'Saúde e bem-estar',
    'Acordo Ortográfico',
]

estados = [
    Estado(nome="Acre", sigla="AC"),
    Estado(nome="Alagoas", sigla="AL"),
    Estado(nome="Amapá", sigla="AP"),
    Estado(nome="Amazonas", sigla="AM"),
    Estado(nome="Bahia", sigla="BA"),
    Estado(nome="Ceará", sigla="CE"),
    Estado(nome="Espírito Santo", sigla="ES"),
    Estado(nome="Goiás", sigla="GO"),
    Estado(nome="Maranhão", sigla="MA"),
    Estado(nome="Mato Grosso", sigla="MT"),
    Estado(nome="Mato Grosso do Sul", sigla="MS"),
    Estado(nome="Minas Gerais", sigla="MG"),
    Estado(nome="Pará", sigla="PA"),
    Estado(nome="Paraíba", sigla="PB"),
    Estado(nome="Paraná", sigla="PR"),
    Estado(nome="Pernambuco", sigla="PE"),
    Estado(nome="Piauí", sigla="PI"),
    Estado(nome="Rio de Janeiro", sigla="RJ"),
    Estado(nome="Rio Grande do Norte", sigla="RN"),
    Estado(nome="Rio Grande do Sul", sigla="RS"),
    Estado(nome="Rondônia", sigla="RO"),
    Estado(nome="Roraima", sigla="RR"),
    Estado(nome="Santa Catarina", sigla="SC"),
    Estado(nome="São Paulo", sigla="SP"),
    Estado(nome="Sergipe", sigla="SE"),
    Estado(nome="Tocantins", sigla="TO"),
    Estado(nome="Distrito Federal", sigla="DF"),
]

cities_list = requests.get(
    'https://gist.githubusercontent.com/letanure/3012978/raw/9ceb73206fce1cbed434564e006e0ad8c16b5102/estados-cidades2.json').json()[
    'cities']


def change_id(_id):
    if _id == 11:
        return 21
    if _id == 12:
        return 1
    if _id == 13:
        return 4
    if _id == 14:
        return 22
    if _id == 15:
        return 13
    if _id == 16:
        return 3
    if _id == 17:
        return 26
    if _id == 21:
        return 9
    if _id == 22:
        return 17
    if _id == 23:
        return 6
    if _id == 24:
        return 19
    if _id == 25:
        return 14
    if _id == 26:
        return 16
    if _id == 27:
        return 2
    if _id == 28:
        return 25
    if _id == 29:
        return 5
    if _id == 31:
        return 12
    if _id == 32:
        return 7
    if _id == 33:
        return 18
    if _id == 35:
        return 24
    if _id == 41:
        return 15
    if _id == 42:
        return 23
    if _id == 43:
        return 20
    if _id == 50:
        return 11
    if _id == 51:
        return 10
    if _id == 52:
        return 8
    if _id == 53:
        return 27


def get_city_and_fill():
    data = requests.get(
        'https://gist.githubusercontent.com/letanure/3012978/raw/9ceb73206fce1cbed434564e006e0ad8c16b5102/estados-cidades2.json').json()
    df = pd.DataFrame(data['cities'])
    df['estado_id'] = df['state_id'].apply(change_id)
    df['nome'] = df.apply(lambda x: x['nome'] if isinstance(x['nome'], str) else x['name'], axis=1)
    df['populacao'] = np.random.randint(10000, 1000000, size=len(df))
    cities = df[['estado_id', 'nome', 'populacao']].to_dict('records')
    bulk_list = [Cidade(**x) for x in cities]
    return bulk_list


def get_diretor():
    nome = fake.first_name()
    sobrenome = fake.first_name()
    data = dict(
        nome=nome,
        sobrenome=sobrenome,
        sexo=random.choice(['m', 'f']),
    )
    return data


# def get_cidade():
#     nome = fake.local_latlng('BR')[2]
#     populacao = random.randint(10000, 1000000)
#     data = dict(
#         nome=nome,
#         populacao=populacao,
#         estado_id=random.randint(1, 15)
#     )
#     return data
#
#
# def get_estado():
#     nome = fake.local_latlng('BR')[4].split('/')[1]
#     sigla = nome[:2]
#     data = dict(
#         nome=nome,
#         sigla=sigla,
#     )
#     return data


def get_aluno():
    nome = fake.first_name()
    sobrenome = fake.first_name()
    nascimento = fake.date()
    rg = fake.ssn()
    data = dict(
        nome=nome,
        sobrenome=sobrenome,
        nascimento=nascimento,
        rg=rg,
        sexo=random.choice(['m', 'f']),
        escola_id=random.randint(1, 1000),
        aprovado=random.choice([True, False])
    )
    return data


def get_professor():
    nome = fake.first_name()
    sobrenome = fake.first_name()
    data = dict(
        nome=nome,
        sobrenome=sobrenome,
        sexo=random.choice(['m', 'f']),
    )
    return data


def get_escola(idx):
    nome = fake.domain_word().upper()
    aberta_em = fake.date()
    bairro = fake.first_name().title()
    diretor_id = idx
    cidade_id = random.randint(1, 5600)
    data = dict(
        nome=nome,
        aberta_em=aberta_em,
        bairro=bairro,
        diretor_id=diretor_id,
        cidade_id=cidade_id,
    )
    return data


def get_aula():
    escolas = list(Escola.objects.all().values_list('pk', flat=True))
    escola_id = random.choice(escolas)

    materias = list(Materia.objects.filter(professores__escolas=escola_id).distinct().values_list('pk', flat=True))
    # professor_id = random.randint(1, 100)
    data = dict(
        escola_id=escola_id,
        materia_id=random.choice(materias),
        # professor_id=professor_id
    )
    return data


def create_escolas(qtd):
    aux_list = []
    for i in range(qtd):
        data = get_escola(i + 1)
        obj = Escola(**data)
        aux_list.append(obj)
    Escola.objects.bulk_create(aux_list)


def create_objects(title, fx, objc, qtd=100):
    aux_list = []
    for _ in progressbar(range(qtd), title):
        data = fx()
        obj = objc(**data)
        aux_list.append(obj)
    objc.objects.bulk_create(aux_list)


def set_escolas_professor(professor_por_escola=8):
    escolas = Escola.objects.all()
    professores = list(Professor.objects.values_list('id', flat=True))
    for escola in escolas:
        professores_aleatorios = random.sample(professores, professor_por_escola)
        escola.professores.set(professores_aleatorios)


def set_materias_professor(materias_por_professor=3):
    professores = Professor.objects.all()
    materias = list(Materia.objects.values_list('id', flat=True))
    for prof in professores:
        materias_aleatorias = random.sample(materias, materias_por_professor)
        prof.materias.set(materias_aleatorias)


# create_objects('Alunos', get_aluno, Aluno)
# create_objects('Professor', get_professor, Professor)
# create_objects('Diretor', get_diretor, Diretor)
# create_objects('Estado', get_estado, Estado, 10)
# create_objects('Cidade', get_cidade, Cidade, 300)


class Command(BaseCommand):
    help = 'Create data.'

    def handle(self, *args, **options):
        for x in materias:
            Materia.objects.create(nome=x)

        Estado.objects.bulk_create(estados)
        Cidade.objects.bulk_create(get_city_and_fill())

        create_objects('Diretor', get_diretor, Diretor, 2000)
        create_escolas(1000)
        create_objects('Professor', get_professor, Professor, 2000)
        # create_objects('Escola', get_escola, Escola, 2000)
        # create_objects('Cidade', get_cidade, Cidade, 500)
        # create_objects('Estado', get_estado, Estado, 15)
        create_objects('Alunos', get_aluno, Aluno, 200000)
        set_materias_professor(materias_por_professor=5)
        set_escolas_professor(professor_por_escola=12)
        create_objects('Aula', get_aula, Aula, 8000)
