# -*- coding: utf-8 -*-
from django.conf import settings

class DAO():

    def __init__(self, sgbd=None):

        self.connection = None
        if not sgbd:
            # tomando como padrão o SGBD Postgres
            self.sgbd = 'postgres'
            self.database = settings.ACADEMICO['DATABASE_NAME']
            self.user = settings.ACADEMICO['DATABASE_USER']
            self.password = settings.ACADEMICO['DATABASE_PASSWORD']
            self.host = settings.ACADEMICO['DATABASE_HOST']
            self.port = settings.ACADEMICO['DATABASE_PORT']
        else:
            self.sgbd = sgbd
            if self.sgbd == 'postgres':
                self.database = settings.ACADEMICO['DATABASE_NAME']
                self.user = settings.ACADEMICO['DATABASE_USER']
                self.password = settings.ACADEMICO['DATABASE_PASSWORD']
                self.host = settings.ACADEMICO['DATABASE_HOST']
                self.port = settings.ACADEMICO['DATABASE_PORT']
            elif self.sgbd == 'mysql':
                self.database = settings.VESTIBULAR['DATABASE_NAME']
                self.user = settings.VESTIBULAR['DATABASE_USER']
                self.password = settings.VESTIBULAR['DATABASE_PASSWORD']
                self.host = settings.VESTIBULAR['DATABASE_HOST']
                self.port = settings.VESTIBULAR['DATABASE_PORT']

    def get_connection(self):
        if self.sgbd == 'postgres':
            """Conexão com Postgres"""
            import psycopg2
            return psycopg2.connect(
                                    "dbname='%s' user='%s' host='%s' password='%s'" % \
                                    (self.database, self.user, self.host, self.password))

        elif self.sgbd == 'mysql':
            """Conexão com MYSql"""
            import pymysql
            return pymysql.connect(
                                   host=self.host,
                                   user=self.user,
                                   passwd=self.password,
                                   db=self.database)

        else:
            print ('Erro ao definir sgbd para conexao')
            return None

