from django.db import models


# Create your models here.
class Sexo(models.Model):
    descricao = models.CharField(u'Descrição', max_length=3, blank=False, null=False)

    def __str__(self):
        return self.descricao


class Etnia(models.Model):
    descricao = models.CharField(u'Descrição', max_length=30, blank=False, null=False, unique=True)

    def __str__(self):
        return self.descricao


class OrigemEscolar(models.Model):
    descricao = models.CharField(u'Descrição', max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.descricao


class Curso(models.Model):
    nome = models.CharField(u'Nome', max_length=200, blank=False, null=False, unique=True)

    def __str__(self):
        return self.nome


class Campus(models.Model):
    nome = models.CharField(u'Nome', max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    cpf = models.CharField(u'CPF', max_length=15, blank=False, null=False, primary_key=True)
    sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE, blank=True, null=True)
    etnia = models.ForeignKey(Etnia, on_delete=models.CASCADE, blank=True, null=True)
    origemEscolar = models.ForeignKey(OrigemEscolar, on_delete=models.CASCADE, blank=True, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, blank=True, null=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, blank=True, null=True)
