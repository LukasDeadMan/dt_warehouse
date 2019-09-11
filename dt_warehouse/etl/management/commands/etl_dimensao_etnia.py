# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from etl.dao import DAO

from datawarehouse.models import Etnia


class Command(BaseCommand):

    def handle(self, *args, **options):

        dao = DAO('mysql')

        sql = "SELECT DISTINCT TRIM(VA.alternativa) FROM vestibular.alternativas VA \
               WHERE VA.perguntas_idperguntas = 31 \
               ORDER BY TRIM(VA.alternativa);"
        bd = dao.get_connection()
        c = bd.cursor()

        c.execute(sql)
        dados = c.fetchall()
        print(('Número de registros encontrados: {}').format(len(dados)))

        conta_criados = 0
        conta_atualizados = 0
        if len(dados) > 0:
            for d in dados:
                print(d)
                etnia_descricao = d[0]


                # INSERT DOS DADOS NA TABELA DO DATAWAREHOUSE
                obj, created = Etnia.objects.update_or_create(
                    descricao = etnia_descricao
                )

                if created:
                    conta_criados += 1
                else:
                    conta_atualizados += 1

        print(('Número de registros INSERIDOS: {}').format(conta_criados))
        print(('Número de registros ATUALIZADOS: {}').format(conta_atualizados))
        bd.close()
