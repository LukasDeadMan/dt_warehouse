from django.shortcuts import render

# Create your views here.

from datawarehouse.models import Aluno

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np

@login_required
def index(request):

    alunos_etnia = Aluno.get_list('etnia__descricao')
    labels_etnia = []
    values_etnia = []
    titulo = 'Gráfico de Alunos por Etnia'
    for aluno in alunos_etnia:
        labels_etnia.append(aluno['etnia__descricao'])
        values_etnia.append(aluno['total'])

    grafico_etnia = get_bar_graphic(labels_etnia, values_etnia, titulo)


    alunos_origemEscolar = Aluno.get_list('origemEscolar__descricao')
    labels_origemEscolar = []
    values_origemEscolar = []
    titulo = 'Gráfico de Alunos por Origem Escolar'
    for aluno in alunos_origemEscolar:
        aluno['origemEscolar__descricao'] = aluno['origemEscolar__descricao'].replace('A maior', 'Maior')
        labels_origemEscolar.append(aluno['origemEscolar__descricao'])
        values_origemEscolar.append(aluno['total'])

    grafico_origemEscolar = get_donut_pie_graphic(labels_origemEscolar, values_origemEscolar, titulo)

    alunos_sexo = Aluno.get_list('sexo__descricao')
    labels_sexo = []
    values_sexo = []
    titulo = 'Gráfico de Alunos por Sexo'
    for aluno in alunos_sexo:
        if (aluno['sexo__descricao'] == 'M'):
            aluno['sexo__descricao'] = 'Masculino'
        else:
            aluno['sexo__descricao'] = 'Feminino'
        labels_sexo.append(aluno['sexo__descricao'])
        values_sexo.append(aluno['total'])

    grafico_sexo = get_label_graphic(labels_sexo, values_sexo, titulo)


    alunos_campus = Aluno.get_list('campus__nome')
    labels_campus = []
    values_campus = []
    titulo = 'Gráfico de Alunos por Campus'
    for aluno in alunos_campus:
        aluno['campus__nome'] = aluno['campus__nome'].replace(' Avançado', '')
        labels_campus.append(aluno['campus__nome'])
        values_campus.append(aluno['total'])

    grafico_campus = get_pie_graphic(labels_campus,values_campus, titulo)

    alunos_curso = Aluno.get_list('curso__nome')

    context = {'alunos_sexo': alunos_sexo,
               'grafico_sexo': grafico_sexo,
               'alunos_etnia': alunos_etnia,
               'grafico_etnia': grafico_etnia,
               'alunos_origemEscolar': alunos_origemEscolar,
               'grafico_origemEscolar': grafico_origemEscolar,
               'alunos_campus': alunos_campus,
               'grafico_campus': grafico_campus,
               'alunos_curso': alunos_curso
              }

    return render(request, 'datawarehouse/index.html', context)




def get_donut_pie_graphic(labels, values, titulo):
    fig, ax = plt.subplots(figsize=(10, 4), subplot_kw=dict(aspect="equal"))

    ax.axis('equal')
    wedges, texts = ax.pie(values, wedgeprops=dict(width=0.5), startangle=-40)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")
    ax.set_title(titulo)
    ax.legend(wedges, labels,
              title="Origem Escolar",
              loc="center left",
              bbox_to_anchor=(0.762, 0, 0.5, 1))

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        value = round(values[i]/sum(values)*100,1)
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(str(value)+'%', xy=(x, y), xytext=(1.35 * np.sign(x), 1.3 * y),
                    horizontalalignment=horizontalalignment, **kw)


    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def get_pie_graphic(labels, values, titulo):
    fig1, ax = plt.subplots(figsize=(10, 4))
    ax.pie(values, labels=labels, autopct='%1.1f%%',
                startangle=90)
    ax.axis('equal')
    ax.set_title(titulo)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def get_label_graphic(labels, values, titulo):
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(pct / 100. * np.sum(allvals))
        if absolute in allvals:
            return "{:.1f}%\n{}".format(pct, absolute)
        else:
            return "{:.1f}%\n{}".format(pct, absolute+1)

    wedges, texts, autotexts = ax.pie(values, autopct=lambda pct: func(pct, values),
                                      textprops=dict(color="w"), startangle=90)

    ax.legend(wedges, labels,
              title="Campus",
              loc="center left",
              bbox_to_anchor=(0.763, 0, 0.5, 1))

    plt.setp(autotexts, size=10, weight="bold")

    ax.set_title(titulo)
    ax.axis('equal')
    ax.set_title(titulo)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def get_bar_graphic(labels, values, titulo):

    if(len(labels)<10):
        leng = len(labels)
    else:
        leng = 10

    x = np.arange(leng)  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, values, width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Quantidade')
    ax.set_title(titulo)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)

    fig.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic