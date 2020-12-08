import datetime
import mysql.connector
import pyodbc
import sqlalchemy as sal
from sqlalchemy import MetaData, Table, Column, Integer, String, Sequence, create_engine, select, and_, insert, func
from psycopg2 import *
import datetime
import mysql.connector
from pypika import Query


engine = create_engine('postgresql://andre:manchester00@localhost/test')
metadata = MetaData(bind=None)
table = Table('car', metadata, autoload=True, autoload_with=engine)

#stmt = select([table.c.price, table.c.make]).where(and_(table.c.make == 'Honda', table.c.price == 76181.75))
stmt = select([table.c.price, table.c.make])
stmt = stmt.where(table.c.make == 'Honda')
stmt = stmt.where(table.c.price == 76181.75)

connection = engine.connect()

results = connection.execute(stmt).fetchall()
print(results)
connection.close()
'''
for i in result.fetchall():
        print(i[3])'''


class ConfigForm():
    def __init__(self):
        pass

    def get_login(self, usuario, senha, nome=False):
        engine = create_engine(f'postgresql://{usuario}:{senha}@localhost/aabb')
        conn = engine.connect()
        self.config = [usuario, senha]
        return self.config


    def get_results(self, nome=False, matri=False, time=False, situacao=False, sexo=False, cpf=False, config=False):
        self.config = config
        
        engine = create_engine(f'postgresql://{self.config[0]}:{self.config[1]}@localhost/aabb')
        metadata = MetaData(bind=None)
        table = Table('clientes_aabb', metadata, autoload=True, autoload_with=engine)
        stmt = select([table])


        if situacao != '':
            stmt = stmt.where(table.c.situacao == situacao)
        if cpf != '':
            stmt = stmt.where(table.c.cpf == cpf)
        if sexo != '':
            stmt = stmt.where(table.c.gender == sexo)
        if nome != '':
            stmt = stmt.where(table.c.first_name.contains(nome))

        stmt = stmt.limit(15).order_by(table.c.id.asc())
        connection = engine.connect()
        query = connection.execute(stmt).fetchall()
        connection.close()

        lista_controle = []
        lista = []
        for row in query:
            lista_controle.append(row[0])
            lista_controle.append(row[1] + " " + row[2])
            lista_controle.append(row[5])
            lista_controle.append(row[3])
            lista_controle.append(row[4])
            lista_controle.append(row[6])
            lista_controle.append(row[0])
            lista.append(lista_controle)
            lista_controle = []
        print(lista)
        return lista



    def inserir(self,c_matclien,c_nomclien, c_cpfclien, c_sexclien, c_timclien, c_endclien=''
                ,c_sitclien='', config=False):
        self.config = config
        
        engine = create_engine(f'postgresql://{self.config[0]}:{self.config[1]}@localhost/aabb')
        metadata = MetaData(bind=None)
        table = Table('clientes_aabb', metadata, autoload=True, autoload_with=engine)
        connection = engine.connect()

        stmt = select([func.max(table.c.id)])
        seq = connection.execute(stmt)
        seq = seq.fetchall()[0][0]

        stmt = insert(table).values(id=seq+1,first_name=c_nomclien, last_name='Silva',
                                    gender='Male', cpf=c_cpfclien,
                                    situacao='false', address='Some value')

        connection = engine.connect()
        connection.execute(stmt)
        connection.close()



    def editar(self, c_matclien,c_nomclien, c_cpfclien, c_sexclien, c_timclien, unique
                ,c_sitclien='', config=False):
        
        self.config = config
        engine = create_engine(f'postgresql://{self.config[0]}:{self.config[1]}@localhost/aabb')
        metadata = MetaData(bind=None)
        table = Table('clientes_aabb', metadata, autoload=True, autoload_with=engine)
    
        stmt = table.update().where(table.c.id == unique).values(first_name = c_nomclien, cpf=c_cpfclien,
                                                                 gender=c_sexclien, situacao=c_sitclien)

        connection = engine.connect()
        connection.execute(stmt)
        connection.close()

