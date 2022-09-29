from django.core.exceptions import ValidationError
from django.db import models

SEXO_CHOICE = (
    ('m', 'Masculino'),
    ('f', 'Feminino')
)


# Create your models here.

class Diretor(models.Model):
    nome = models.CharField('Nome', max_length=100)
    sobrenome = models.CharField('Sobrenome', max_length=100)
    sexo = models.CharField(choices=SEXO_CHOICE, max_length=1)

    class Meta:
        verbose_name = 'Diretor'
        verbose_name_plural = 'Diretores'

    def __str__(self):
        return self.nome


class Cidade(models.Model):
    nome = models.CharField('Cidade', max_length=100)
    populacao = models.PositiveIntegerField('População')
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE, related_name='cidades')

    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    def __str__(self):
        return self.nome


class Estado(models.Model):
    nome = models.CharField('Estado', max_length=80)
    sigla = models.CharField('Estado Sigla', max_length=2)

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.nome


class Materia(models.Model):
    nome = models.CharField('Nome', max_length=100)

    class Meta:
        verbose_name = 'Matéria'
        verbose_name_plural = 'Matérias'

    def __str__(self):
        return self.nome


class Professor(models.Model):
    nome = models.CharField('Nome', max_length=100)
    sobrenome = models.CharField('Sobrenome', max_length=100)
    sexo = models.CharField(choices=SEXO_CHOICE, max_length=1)
    materias = models.ManyToManyField(Materia, blank=True, related_name='professores')

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self):
        return self.nome


class Escola(models.Model):
    nome = models.CharField('Nome', max_length=100)
    aberta_em = models.DateField('Aberta em')
    bairro = models.CharField('Bairro', max_length=100)
    diretor = models.OneToOneField(Diretor, on_delete=models.CASCADE, related_name='escolas')
    professores = models.ManyToManyField(Professor, blank=True, related_name='escolas')
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, related_name='escolas')

    class Meta:
        verbose_name = 'Escola'
        verbose_name_plural = 'Escolas'

    def __str__(self):
        quantidade_alunos = self.alunos.count()
        quantidade_professores = self.professores.count()
        return f'{self.nome} | {quantidade_alunos} Alunos | {quantidade_professores} Professores'


class Aluno(models.Model):
    nome = models.CharField('Nome', max_length=100)
    sobrenome = models.CharField('Nome', max_length=100)
    nascimento = models.DateField('Nascimento')
    rg = models.CharField('RG', max_length=20)
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True, blank=True, related_name='alunos')
    sexo = models.CharField(choices=SEXO_CHOICE, max_length=1)
    aprovado = models.BooleanField('Aprovado', default=False)

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'


class Aula(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='aulas')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, blank=True, null=True, related_name='aulas')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='aulas')
    alunos = models.ManyToManyField(Aluno, blank=True, related_name='aulas')


    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    def __str__(self):
        return f'{self.id} | {self.escola.nome} | {self.professor.nome if self.professor else ""}'

    def save(self, *args, **kwargs):
        if self.professor:
            if self.escola not in self.professor.escolas.all():
                raise ValidationError(f"O Professor não tem contrato com a escola: {self.escola.nome}")

            if self.materia not in self.professor.materias.all():
                raise ValidationError(f"O Professor não ministra essa aula: {self.escola.nome}")

        return super(Aula, self).save()
