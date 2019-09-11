from django.shortcuts import render

# Create your views here.

from datawarehouse.models import Aluno

from django.db.models import Count

from django.http import HttpResponse

from io import BytesIO
import base64

def index(request):
    alunos_sexo = Aluno.objects.all().values('sexo__descricao').annotate(total=Count('*')).order_by('sexo__descricao)')

    #import pdb; pdb.set_trace()

    labels_sexo = []
    valores_sexo = []
    for alunos_sexo in alunos_sexo:
        labels_sexo.append(alunos_sexo['sexo_descricao'])
        valores_sexo.append(alunos_sexo['total'])
    context = {'alunos_sexo' : alunos_sexo}

    figl, ax_sexo = plt.subplots(figsize = (10, 4))
    ax_sexo.pie(valores_sexo, labels = labels_sexo, autopct = '%1.1f%%', startang = 90)



    return render(request, 'datawarehouse/index.html', context)
