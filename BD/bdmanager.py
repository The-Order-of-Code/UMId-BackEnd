import mysql.connector

#######################################
#PREENCHER ISTO COM OS VOSSOS DADOS!!!#
#######################################
cnx = mysql.connector.connect(host="", user="", password="", database="bd_umid")



#########
#Scripts#
#########



############
#Utilizador#
############

def getUtilizador(numero_de_estudante):

	query = """ SELECT idutilizador FROM Utilizador WHERE numero_de_estudante = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_estudante, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT nome, numero_de_estudante, username, password, email, data_de_nascimento, maior_de_idade, ano_inscrito FROM Utilizador WHERE idutilizador = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	result2 = cursor.fetchone()
	cursor.close()

	return result2

def insertUser(nome, numero_de_estudante, username, password, email, data_de_nascimento, maior_de_idade, ano_inscrito, tipoutilizador, curso):

	query = """ SELECT idtipoutilizador FROM TipoUtilizador WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (tipoutilizador, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT idcurso FROM Curso WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (curso, ))
	result2 = cursor.fetchone()
	cursor.close()

	query = "INSERT INTO `Utilizador` (`nome`, `numero_de_estudante`, `username`, `password`, `email`, `data_de_nascimento`, `maior_de_idade`, `ano_inscrito`, `idtipoutilizador`, `idcurso`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (nome, numero_de_estudante, username, password, email, data_de_nascimento, maior_de_idade, ano_inscrito, result1[0], result2[0]))
	cnx.commit()
	cursor.close()

def deleteUser(numero_de_estudante):

	query = """ SELECT idutilizador FROM Utilizador WHERE numero_de_estudante = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_estudante, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = "DELETE FROM `ListaReservas` WHERE idutilizador = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	cnx.commit()
	cursor.close()

	query = "DELETE FROM `ListaCompras` WHERE idutilizador = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	cnx.commit()
	cursor.close()

	query = "DELETE FROM `Utilizador` WHERE idutilizador = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	cnx.commit()
	cursor.close()

def editUser(nome, numero_de_estudante, username, password, email, data_de_nascimento, maior_de_idade, ano_inscrito, tipoutilizador, curso):

	query = """ SELECT idtipoutilizador FROM TipoUtilizador WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (tipoutilizador, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT idcurso FROM Curso WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (curso, ))
	result2 = cursor.fetchone()
	cursor.close()

	query = """ SELECT idutilizador FROM Utilizador WHERE numero_de_estudante = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_estudante, ))
	result3 = cursor.fetchone()
	cursor.close()

	query = "UPDATE `Utilizador` SET nome = %s, numero_de_estudante = %s, username = %s, password = %s, email = %s, data_de_nascimento = %s, maior_de_idade = %s, ano_inscrito = %s, idtipoutilizador = %s, idcurso = %s WHERE idutilizador = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (nome, numero_de_estudante, username, password, email, data_de_nascimento, maior_de_idade, ano_inscrito, result1[0], result2[0], result3[0]))
	cnx.commit()
	cursor.close()



#######
#Curso#
#######

def insertCurso(newdesignacao):

	query = "INSERT INTO `Curso` (`designacao`) VALUES (%s) "
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (newdesignacao, ))
	cnx.commit()
	cursor.close()

def deleteCurso(designacao):

	query = """ SELECT idcurso FROM Curso WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (designacao, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = "DELETE FROM `Utilizador` WHERE idcurso = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	cnx.commit()
	cursor.close()

	query = "DELETE FROM `Curso` WHERE idcurso = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	cnx.commit()
	cursor.close()

def editCurso(olddesignacao, newdesignacao):

	query = """ SELECT idcurso FROM Curso WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (olddesignacao, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = "UPDATE `Curso` SET designacao = %s WHERE idcurso = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (newdesignacao, result1[0]))
	cnx.commit()
	cursor.close()



################
#TipoUtilizador#
################

def insertTipoUtilizador(newdesignacao):

	query = "INSERT INTO `TipoUtilizador` (`designacao`) VALUES (%s) "
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (newdesignacao, ))
	cnx.commit()
	cursor.close()

def deleteTipoUtilizador(designacao):

	query = """ SELECT idtipoutilizador FROM TipoUtilizador WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (designacao, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = "DELETE FROM `Utilizador` WHERE idtipoutilizador = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	cnx.commit()
	cursor.close()

	query = "DELETE FROM `TipoUtilizador` WHERE idtipoutilizador = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	cnx.commit()
	cursor.close()

def editTipoUtilizador(olddesignacao, newdesignacao):

	query = """ SELECT idtipoutilizador FROM TipoUtilizador WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (olddesignacao, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = "UPDATE `TipoUtilizador` SET designacao = %s WHERE idtipoutilizador = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (newdesignacao, result1[0]))
	cnx.commit()
	cursor.close()



######
#Sala#
######

def getSala(numero_de_sala):

	query = """ SELECT idsala FROM Sala WHERE numero_de_sala = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_sala, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT numero_de_sala, ocupacao FROM Sala WHERE idsala = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	result2 = cursor.fetchone()
	cursor.close()

	return result2

def insertSala(numero_de_sala, ocupacao):

	query = "INSERT INTO `Sala` (`numero_de_sala`, `ocupacao`) VALUES (%s,%s) "
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_sala, ocupacao))
	cnx.commit()
	cursor.close()

def deleteSala(numero_de_sala):

	query = """ SELECT idsala FROM Sala WHERE numero_de_sala = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_sala, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = "DELETE FROM `ListaReservas` WHERE idsala = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	cnx.commit()
	cursor.close()

	query = "DELETE FROM `Sala` WHERE idsala = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	cnx.commit()
	cursor.close()

def editSala(oldnumero_de_sala, newnumero_de_sala, ocupacao):

	query = """ SELECT idsala FROM Sala WHERE numero_de_sala = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (oldnumero_de_sala, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = "UPDATE `Sala` SET numero_de_sala = %s, ocupacao = %s WHERE idsala = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (newnumero_de_sala, ocupacao, result1[0]))
	cnx.commit()
	cursor.close()



#######
#Senha#
#######

def getSenha(designacao):

	query = """ SELECT idsenha FROM Senha WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (designacao, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT designacao, preco FROM Senha WHERE idsenha = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	result2 = cursor.fetchone()
	cursor.close()

	return result2

def insertSenha(designacao, preco):

	query = "INSERT INTO `Senha` (`designacao`, `preco`) VALUES (%s,%s) "
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (designacao, preco))
	cnx.commit()
	cursor.close()

def deleteSenha(designacao):

	query = """ SELECT idsenha FROM Senha WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (designacao, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = "DELETE FROM `ListaCompras` WHERE idsenha = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	cnx.commit()
	cursor.close()

	query = "DELETE FROM `Senha` WHERE idsenha = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], ))
	cnx.commit()
	cursor.close()

def editSenha(olddesignacao, newdesignacao, preco):

	query = """ SELECT idsenha FROM Senha WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (olddesignacao, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = "UPDATE `Senha` SET designacao = %s, preco = %s WHERE idsenha = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (newdesignacao, preco, result1[0]))
	cnx.commit()
	cursor.close()



###############
#ListaReservas#
###############

def getReserva(numero_de_sala, numero_de_estudante):

	query = """ SELECT idsala FROM Sala WHERE numero_de_sala = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_sala, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT idutilizador FROM Utilizador WHERE numero_de_estudante = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_estudante, ))
	result2 = cursor.fetchone()
	cursor.close()

	query = """ SELECT inicio, fim FROM ListaReservas WHERE idsala = %s AND idutilizador = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], result2[0]))
	result3 = cursor.fetchone()
	cursor.close()

	return result3

def insertReserva(numero_de_sala, numero_de_estudante, horai, horaf):

	query = """ SELECT idsala FROM Sala WHERE numero_de_sala = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_sala, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT idutilizador FROM Utilizador WHERE numero_de_estudante = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_estudante, ))
	result2 = cursor.fetchone()
	cursor.close()

	query = "INSERT INTO `ListaReservas` (`idutilizador`, `idsala`, `inicio`, `fim`) VALUES (%s,%s,%s,%s) "
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result2[0], result1[0], horai, horaf))
	cnx.commit()
	cursor.close()

def deleteReserva(numero_de_sala, numero_de_estudante):

	query = """ SELECT idsala FROM Sala WHERE numero_de_sala = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_sala, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT idutilizador FROM Utilizador WHERE numero_de_estudante = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_estudante, ))
	result2 = cursor.fetchone()
	cursor.close()

	query = "DELETE FROM `ListaReservas` WHERE idsala = %s AND idutilizador = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], result2[0]))
	cnx.commit()
	cursor.close()

def editReserva(numero_de_sala, numero_de_estudante, horai, horaf):

	query = """ SELECT idsala FROM Sala WHERE numero_de_sala = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_sala, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT idutilizador FROM Utilizador WHERE numero_de_estudante = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_estudante, ))
	result2 = cursor.fetchone()
	cursor.close()

	query = "UPDATE `ListaReservas` SET inicio = %s, fim = %s WHERE idsala = %s AND idutilizador = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (horai, horaf, result1[0], result2[0]))
	cnx.commit()
	cursor.close()



##############
#ListaCompras#
##############

def getCompra(designacao, numero_de_estudante):

	query = """ SELECT idsenha FROM Senha WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (designacao, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT idutilizador FROM Utilizador WHERE numero_de_estudante = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_estudante, ))
	result2 = cursor.fetchone()
	cursor.close()

	query = """ SELECT quantidade FROM ListaCompras WHERE idsenha = %s AND idutilizador = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], result2[0]))
	result3 = cursor.fetchone()
	cursor.close()

	return result3[0]

def insertCompra(designacao, numero_de_estudante, quantidade):

	query = """ SELECT idsenha FROM Senha WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (designacao, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT idutilizador FROM Utilizador WHERE numero_de_estudante = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_estudante, ))
	result2 = cursor.fetchone()
	cursor.close()

	query = "INSERT INTO `ListaCompras` (`idutilizador`, `idsenha`, `quantidade`) VALUES (%s,%s,%s) "
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result2[0], result1[0], quantidade))
	cnx.commit()
	cursor.close()

def deleteCompra(designacao, numero_de_estudante):

	query = """ SELECT idsenha FROM Senha WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (designacao, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT idutilizador FROM Utilizador WHERE numero_de_estudante = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_estudante, ))
	result2 = cursor.fetchone()
	cursor.close()

	query = "DELETE FROM `ListaCompras` WHERE idsenha = %s AND idutilizador = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (result1[0], result2[0]))
	cnx.commit()
	cursor.close()

def editCompra(designacao, numero_de_estudante, quantidade):

	query = """ SELECT idsenha FROM Senha WHERE designacao = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (designacao, ))
	result1 = cursor.fetchone()
	cursor.close()

	query = """ SELECT idutilizador FROM Utilizador WHERE numero_de_estudante = %s """
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (numero_de_estudante, ))
	result2 = cursor.fetchone()
	cursor.close()

	query = "UPDATE `ListaCompras` SET quantidade = %s WHERE idsenha = %s AND idutilizador = %s"
	cursor = cnx.cursor(prepared=True)
	cursor.execute(query, (quantidade, result1[0], result2[0]))
	cnx.commit()
	cursor.close()



########
#Testes#
########



###################################
#Utilizador (testado com sucesso!)#
###################################

#print(getUtilizador(20));
#insertUser("Gajo",20,"vvv","123","gajo@ola.com","2020-01-01",0,7,"Aluno","MIEI");
#deleteUser(20);
#editUser("Gajas",20,"vvv","123","gajas@ola.com","2020-01-01",0,7,"Aluno","LEI");


##############################
#Curso (testado com sucesso!)#
##############################

#insertCurso("LEI");
#deleteCurso("LEI");
#editCurso("LEI","MIEI");


#######################################
#TipoUtilizador (testado com sucesso!)#
#######################################

#insertTipoUtilizador("Admin");
#deleteTipoUtilizador("Admin");
#editTipoUtilizador("Admin","Aluno");


#############################
#Sala (testado com sucesso!)#
#############################

#print(getSala(1));
#insertSala(1,20);
#deleteSala(1);
#editSala(1,2,33);


##############################
#Senha (testado com sucesso!)#
##############################

#print(getSenha("Normal"));
#insertSenha("Normal",20);
#deleteSenha("Normal");
#editSenha("Normal","Erva",33);


######################################
#ListaReservas (testado com sucesso!)#
######################################

#print(getReserva(1,20))
#insertReserva(1,20,'2020-01-01 00:00:00','2020-01-01 20:00:00');
#deleteReserva(1,20);
#editReserva(1,20,'2020-01-01 20:00:00','2020-01-01 00:00:00');


#####################################
#ListaCompras (testado com sucesso!)#
#####################################

#print(getCompra("Normal",20))
#insertCompra("Normal",20,20);
#deleteCompra("Normal",20);
#editCompra("Normal",20,33);