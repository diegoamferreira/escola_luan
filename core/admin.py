from django import forms
from django.contrib import admin

from core.models import *

# Register your models here.
Models = (Diretor, Estado, Cidade, Materia, Professor, Escola, Aluno)

admin.site.register(Models)


# def update_factory(escola):
#     class UpdateForm(forms.ModelForm):
#         professor = forms.ModelChoiceField(
#             queryset=Professor.objects.filter(escolas=escola)
#         )
#         alunos = forms.ModelMultipleChoiceField(
#             queryset=Aluno.objects.filter(escola=escola)
#         )
#     return UpdateForm


# def alunos_factory(escola):
#     class AlunoForm(forms.ModelForm):
#         alunos = forms.ModelChoiceField(
#             queryset=Aluno.objects.filter(escola=escola)
#         )
#
#     return AlunoForm


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'escola', 'materia')
    list_filter = ['id', 'escola', 'materia']

    # raw_id_fields = ["alunos"]

    # exclude = ("alunos",)

    def get_form(self, request, obj, **kwargs):
        form = super(AulaAdmin, self).get_form(request, obj, **kwargs)
        escola = obj.escola
        if escola:

            form.base_fields['alunos'].queryset = Aluno.objects.filter(
                escola=escola
            )

            filtros_professores = {'escolas': escola}
            if obj.materia:
                filtros_professores['materias'] = obj.materia

            print(filtros_professores)

            form.base_fields['professor'].queryset = Professor.objects.filter(
                **filtros_professores
            )

            qs_materias = Materia.objects.filter(
                professores__escolas=escola
            ).distinct().order_by('nome')
            form.base_fields['materia'].queryset = qs_materias
            form.base_fields['materia'].help_text = f'Matérias conhecidas pelos professores: {qs_materias.count()}'
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["escola"]
        else:
            return []

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     print('self')
    #     print(self.get_object())
    #     if db_field.name == "professor":
    #         kwargs["queryset"] = Professor.objects.filter()
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
