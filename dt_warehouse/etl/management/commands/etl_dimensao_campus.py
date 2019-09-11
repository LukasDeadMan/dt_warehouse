# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from etl.dao import DAO

from datawarehouse.models import Campus


class Command(BaseCommand):

    def handle(self, *args, **options):

        dao = DAO('postgres')

        sql = "SELECT DISTINCT TRIM(S.nome) FROM setor S \
               INNER JOIN edu_diretoria ED ON ED.setor_id = S.id \
               INNER JOIN edu_cursocampus ECC ON ECC.diretoria_id = ED.id \
               ORDER BY TRIM(S.nome);"
        bd = dao.get_connection()
        c = bd.cursor()

        c.execute(sql)
        dados = c.fetchall()
        print(('Número de registros encontrados: {}').format(len(dados)))

        conta_criados = 0
        conta_atualizados = 0
        if len(dados) > 0:
            for d in dados:
                campus_nome = d[0]  # type: string

                # TRATAMENTOS DE DADOS NECESSÁRIOS
                campus_nome = campus_nome.replace('CÂMPUS', 'CAMPUS')

                # TRANSFORMAÇÃO E PREPARAÇÃO DE DADOS PARA INJETAR NO DATAWAREHOUSE
                campus_nome = campus_nome.title()


                # INSERT DOS DADOS NA TABELA DO DATAWAREHOUSE
                obj, created = Campus.objects.update_or_create(
                    nome = campus_nome
                )

                if created:
                    conta_criados += 1
                else:
                    conta_atualizados += 1

        print(('Número de registros INSERIDOS: {}').format(conta_criados))
        print(('Número de registros ATUALIZADOS: {}').format(conta_atualizados))
        bd.close()
