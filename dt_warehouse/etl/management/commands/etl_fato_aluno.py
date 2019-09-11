# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from etl.dao import DAO

from datawarehouse.models import Aluno, Sexo, Curso, Campus, Etnia, OrigemEscolar


class Command(BaseCommand):

    def handle(self, *args, **options):

        dao = DAO('postgres')

        sql = "select distinct trim(PF.cpf), trim(PF.sexo), trim(ECC.descricao), trim(S.nome) from pessoa_fisica PF \
               inner join edu_aluno EA on EA.pessoa_fisica_id = PF.pessoa_ptr_id \
               inner join edu_cursocampus ECC on ECC.id = EA.curso_campus_id \
               inner join edu_diretoria ED on ED.id = ECC.diretoria_id \
               inner join setor S on S.id = ED.setor_id \
               where PF.cpf is not null \
               order by 1;"
        bd = dao.get_connection()
        c = bd.cursor()

        c.execute(sql)
        dados = c.fetchall()
        print(('Número de registros encontrados: {}').format(len(dados)))

        conta_criados = 0
        conta_atualizados = 0
        if len(dados) > 0:

            for d in dados:
                cpf_aluno = d[0]
                sexo_descricao = d[1]
                curso_nome = d[2]
                campus_nome = d[3]
                etnia_descricao = get_etnia(cpf_aluno)
                origemEscolar_descricao = get_origem_escolar(cpf_aluno)


                # TRATAMENTOS DE DADOS NECESSÁRIOS
                curso_nome = curso_nome.title()
                campus_nome = campus_nome.replace('CÂMPUS', 'CAMPUS')
                campus_nome = campus_nome.title()

                # TRANSFORMAÇÃO E PREPARAÇÃO DE DADOS PARA INJETAR NO DATAWAREHOUSE
                sexo_obj = None
                if sexo_descricao:
                    sexo_obj = Sexo.objects.get(descricao=sexo_descricao)

                curso_obj = None
                if curso_nome:
                    curso_obj = Curso.objects.get(nome=curso_nome)

                campus_obj = None
                if campus_nome:
                    campus_obj = Campus.objects.get(nome=campus_nome)

                etnia_obj = None
                if etnia_descricao:
                    etnia_obj = Etnia.objects.get(descricao=etnia_descricao)

                origemEscolar_obj = None
                if origemEscolar_descricao:
                    origemEscolar_obj = OrigemEscolar.objects.get(descricao=origemEscolar_descricao)

                # INSERT DOS DADOS NA TABELA DO DATAWAREHOUSE
                obj, created = Aluno.objects.update_or_create(
                    cpf=cpf_aluno,
                    defaults={
                        'sexo': sexo_obj,
                        'curso': curso_obj,
                        'campus': campus_obj,
                        'etnia': etnia_obj,
                        'origemEscolar': origemEscolar_obj,
                    }
                )

                if created:
                    conta_criados += 1
                else:
                    conta_atualizados += 1

        print(('Número de registros INSERIDOS: {}').format(conta_criados))
        print(('Número de registros ATUALIZADOS: {}').format(conta_atualizados))
        bd.close()


def get_etnia(cpf_aluno):
    dao = DAO('mysql')

    sql = "SELECT TRIM(VA.alternativa) FROM vestibular.alternativas VA \
           INNER JOIN vestibular.respostas VR on VR.alternativas_idalternativas = VA.idalternativas \
           INNER JOIN vestibular.candidatos VC on VC.idalunos = VR.alunos_idalunos \
           where VA.perguntas_idperguntas = 31 and VC.cpf = '" + cpf_aluno + "' \
           order by 1 desc;"

    bd = dao.get_connection()
    c = bd.cursor()

    c.execute(sql)
    dados = c.fetchall()
    bd.close()

    if len(dados) > 0:
        return dados[0][0]

    return 'Não Declarada'




def get_origem_escolar(cpf_aluno):
    dao = DAO('mysql')

    sql = "SELECT TRIM(VA.alternativa) FROM vestibular.alternativas VA \
                    INNER JOIN vestibular.respostas VR on VR.alternativas_idalternativas = VA.idalternativas \
                    INNER JOIN vestibular.candidatos VC on VC.idalunos = VR.alunos_idalunos \
                    where VA.perguntas_idperguntas = 3 and VC.cpf = '" + cpf_aluno + "'\
                    order by 1 desc \
                    limit 1;"
    bd = dao.get_connection()
    c = bd.cursor()

    c.execute(sql)
    dados = c.fetchall()
    bd.close()

    if len(dados) > 0:
        return dados[0][0]

