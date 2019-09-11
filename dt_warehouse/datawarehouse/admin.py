from django.contrib import admin
from datawarehouse.models import Etnia, Sexo, OrigemEscolar, Campus, Curso, Aluno

# Register your models here.
admin.site.register(Etnia)
admin.site.register(Sexo)
admin.site.register(OrigemEscolar)
admin.site.register(Campus)
admin.site.register(Curso)
admin.site.register(Aluno)
