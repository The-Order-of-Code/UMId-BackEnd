
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
query="INSERT INTO professor (idprofessor, nome, apelido, email,data_nascimento,"\
    "Nacionalidade,Morada, foto, idDepartamento)" \
    "values(%s, %s, %s, %s, %s,%s, %s, %s, %s)"
for i in range(100):
    nome=fake.first_name()
    apelido=fake.last_name()
    email=fake.ascii_email()
    data_nascimento=fake.date_of_birth(minimum_age=30,maximum_age=60)
    idDepartamento=random.randint(1,n_cursos)
    Nacionalidade=fake.country()
    Morada=fake.address()
    foto="./imagens/img"+str(random.randint(0,9))
    variaveis=(i+1,nome,apelido,email,data_nascimento,Nacionalidade,Morada,foto,idDepartamento)
    cursor.execute(query,variaveis)
    connection.commit()

#povoar tabela de funcionário
lista_descricao=["cantina","biblioteca","bar","atendimento","secretaria","repografia","limpeza"]
query="INSERT INTO Funcionario (idFuncionario, descricao, nome, apelido, email,"\
    "morada,Nacionalidade,data_nascimento, foto)" \
    "values(%s, %s, %s, %s, %s,%s, %s, %s, %s)"
for i in range(50):
    descricao=fake.word(ext_word_list=lista_descricao)
    nome=fake.first_name()
    apelido=fake.last_name()
    email=fake.ascii_email()
    data_nascimento=fake.date_of_birth(minimum_age=30,maximum_age=60)
    Nacionalidade=fake.country()
    Morada=fake.address()
    foto="./imagens/img"+str(random.randint(0,9))
    variaveis=(i+1,descricao,nome,apelido,email,Morada,Nacionalidade,data_nascimento,foto)
    cursor.execute(query,variaveis)
    connection.commit()
    
    
#Povoar tabela de aluno
query="INSERT INTO aluno"\
    " (idAluno, nome, apelido, email,numero,data_nascimento,ano_inscricao,"\
    "Morada,Nacionalidade,trabalhador_estudante,foto,ano_inscrito,idCurso)"\
    " values(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
for i in range(1000):
    nome=fake.first_name()
    apelido=fake.last_name()
    email=fake.ascii_email()
    numero=fake.unique.random_int(6000,9000)
    data_de_nascimento=fake.date_of_birth(minimum_age=17,maximum_age=25)
    ano_inscricao=fake.date_of_birth(minimum_age=1,maximum_age=6)
    morada=fake.address()
    nacionalidade=fake.country()
    trabalhador=fake.boolean(chance_of_getting_true=20)
    foto="./imagens/img"+str(random.randint(0,9))
    ano_inscrito=random.randint(1,3)
    idcurso=random.randint(1,n_cursos)
    variaveis=(i+1,nome,apelido,email,numero,data_de_nascimento,ano_inscricao,morada,nacionalidade,trabalhador,foto,ano_inscrito,idcurso)
    cursor.execute(query,variaveis)
    connection.commit()



connection.close()