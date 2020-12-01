from django.db import models

class TipoUtilizador(models.Model):
    idtipoutilizador = models.AutoField(primary_key=True)
    designacao = models.CharField(max_length=45)

class Curso(models.Model):
    idcurso = models.AutoField(primary_key=True)
    designacao = models.CharField(max_length=45)

class Utilizador(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=45)
    numero_de_estudante = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    data_de_nascimento = models.DateField()
    maior_de_idade = models.BooleanField()
    ano_inscrito = models.IntegerField()
    idtipoutilizador = models.ForeignKey(TipoUtilizador, on_delete=models.CASCADE, related_name='tipoutilizador', db_column='idtipoutilizador')
    idcurso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='curso', db_column='idcurso')

class Sala(models.Model):
    idsala = models.AutoField(primary_key=True)
    numero_de_sala = models.CharField(max_length=45)
    ocupacao = models.IntegerField()

class Senha(models.Model):
    idsenha = models.AutoField(primary_key=True)
    designacao = models.CharField(max_length=45)
    preco = models.FloatField()

class ListaReservas(models.Model):
    idlistareservas = models.AutoField(primary_key=True)
    idutilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='utilizadorlr', db_column='idutilizador')
    idsala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='salalr', db_column='idsala')
    inicio = models.DateTimeField()
    fim = models.DateTimeField()

    class Meta:
        unique_together = (('idutilizador', 'idsala'),)

class ListaCompras(models.Model):
    idlistacompras = models.AutoField(primary_key=True)
    idutilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='utilizadorlc', db_column='idutilizador')
    idsenha = models.ForeignKey(Senha, on_delete=models.CASCADE, related_name='senhalc', db_column='idsenha')
    quantidade = models.IntegerField()

    class Meta:
        unique_together = (('idutilizador', 'idsenha'),)