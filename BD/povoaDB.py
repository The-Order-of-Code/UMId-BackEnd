
# IMPORTS


import mysql.connector
from faker import Faker
import random

#

connection = mysql.connector.connect(host='localhost',
                                         database='fu',
                                         user='root',
                                         password='1234')#password mais segura do mundo
cursor=connection.cursor()

fake = Faker('pt_PT')
fake.unique.clear()

#Povoar tabela de Departamento

lista_cursos = ['fisica','informatica','mecanica',
                'enfermagem','arte','musica',
                'matematica','ingles','frances',
                'medicina','portugues','alemao',
                'desporto','biologia','geologia',
                'quimica','eletronica','filosofia'
 ]
n_cursos=18


query="INSERT INTO departamento (idDepartamento, nome) values(%s, %s)"
for i in range (n_cursos):
    variaveis= (i+1,lista_cursos[i])
    cursor.execute(query,variaveis)
    connection.commit()
    
#Povoar tabela de Curso
query="INSERT INTO curso (idcurso, nome,idDepartamento) values(%s, %s,%s)"
for i in range (n_cursos):
    variaveis= (i+1,lista_cursos[i],i+1)
    cursor.execute(query,variaveis)
    connection.commit()
    
#Povoar tabela de professor
query="INSERT INTO professor (idprofessor, nome, apelido, email,idDepartamento) values(%s, %s, %s, %s, %s)"
for i in range(100):
    nome=fake.first_name()
    apelido=fake.last_name()
    email=fake.ascii_email()
    idDepartamento=random.randint(1,n_cursos)
    variaveis=(i+1,nome,apelido,email,idDepartamento)
    cursor.execute(query,variaveis)
    connection.commit()
    
#Povoar tabela de aluno
query="INSERT INTO aluno"\
    " (idAluno, nome, apelido, email,numero,data_nascimento,ano_inscrito,Morada,Nacionalidade,trabalhador_estudante,idCurso)"\
    " values(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s)"
for i in range(1000):
    nome=fake.first_name()
    apelido=fake.last_name()
    email=fake.ascii_email()
    numero=random.randint(7000,9000)
    data_de_nascimento=fake.date_of_birth(minimum_age=17,maximum_age=25)
    ano_inscrito=fake.date_of_birth(minimum_age=1,maximum_age=6)
    morada=fake.address()
    nacionalidade=fake.country()
    trabalhador=fake.boolean(chance_of_getting_true=20)
    idcurso=random.randint(1,n_cursos)
    variaveis=(i+1,nome,apelido,email,numero,data_de_nascimento,ano_inscrito,morada,nacionalidade,trabalhador,idcurso)
    cursor.execute(query,variaveis)
    connection.commit()



connection.close()