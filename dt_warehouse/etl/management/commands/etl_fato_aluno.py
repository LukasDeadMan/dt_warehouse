# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from etl.dao import DAO

from datawarehouse.models import Aluno, Sexo, Curso, Campus, Etnia, OrigemEscolar


class Command(BaseCommand):

    def handle(self, *args, **options):

        daoPostgres = DAO('postgres')
        daoMysql = DAO('mysql')

        sql = "select distinct trim(PF.cpf), trim(PF.sexo), trim(ECC.descricao), trim(S.nome) from pessoa_fisica PF \
               inner join edu_aluno EA on EA.pessoa_fisica_id = PF.pessoa_ptr_id \
               inner join edu_cursocampus ECC on ECC.id = EA.curso_campus_id \
               inner join edu_diretoria ED on ED.id = ECC.diretoria_id \
               inner join setor S on S.id = ED.setor_id \
               where PF.cpf is not null \
               order by 1;"
        bdPostgres = daoPostgres.get_connection()
        c = bdPostgres.cursor()

        bdMysql = daoMysql.get_connection()

        c.execute(sql)
        dadosPostgres = c.fetchall()

        dadosMysql = get_list(bdMysql)

        print(('Número de registros encontrados: {}').format(len(dadosPostgres)))
        print(('Número de registros encontrados: {}').format(len(dadosMysql)))

        conta_criados = 0
        conta_atualizados = 0
        if len(dadosPostgres) > 0:

            for d in dadosPostgres:
                cpf_aluno = d[0]
                sexo_descricao = d[1]
                curso_nome = d[2]
                campus_nome = d[3]
                origemEscolar_descricao = 'Não Declarado'
                etnia_descricao = 'Não Declarada'

                index = search(dadosMysql, cpf_aluno)
                if index:
                    origemEscolar_descricao = dadosMysql[index[0]][1]
                    etnia_descricao = dadosMysql[index[0]][2]

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

                origemEscolar_obj = None
                if origemEscolar_descricao:
                    origemEscolar_obj = OrigemEscolar.objects.get(descricao=origemEscolar_descricao)

                etnia_obj = None
                if etnia_descricao:
                    etnia_obj = Etnia.objects.get(descricao=etnia_descricao)

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
        bdPostgres.close()
        bdMysql.close()


def get_list(bd2):

    sql = "SELECT DISTINCT TRIM(VC.cpf), TRIM(VA.alternativa), TRIM(T1.alternativa) FROM vestibular.alternativas VA \
           INNER JOIN vestibular.respostas VR ON VR.alternativas_idalternativas = VA.idalternativas \
           INNER JOIN vestibular.candidatos VC ON VC.idalunos = VR.alunos_idalunos \
           INNER JOIN (SELECT DISTINCT VC.cpf, VA.alternativa FROM vestibular.alternativas VA \
			           INNER JOIN vestibular.respostas VR ON VR.alternativas_idalternativas = VA.idalternativas \
			           INNER JOIN vestibular.candidatos VC ON VC.idalunos = VR.alunos_idalunos \
			           WHERE VA.perguntas_idperguntas = 31 AND VC.cpf IS NOT NULL \
			           GROUP BY VC.cpf, VA.alternativa) AS T1 ON T1.cpf = VC.cpf \
           WHERE VA.perguntas_idperguntas = 3 AND VC.cpf IS NOT NULL \
           GROUP BY TRIM(VC.cpf), TRIM(VA.alternativa), TRIM(T1.alternativa) \
           ORDER BY TRIM(VC.cpf);"
    c = bd2.cursor()

    c.execute(sql)
    return c.fetchall()


def search(dadosMysql, cpf_aluno):
    return [(dadosMysql.index(x)) for x in dadosMysql if cpf_aluno in x]
