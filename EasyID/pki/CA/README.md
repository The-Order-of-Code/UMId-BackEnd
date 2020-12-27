## 1. Instalar dependências:

```
sudo apt-get install golang-go golang-cfssl -y
```

## 2. Instalar e configurar Postgresql:


```
sudo apt install postgresql -y
```

### 2.1 Configurar Postgresql para acesso remoto


```
sudo nano /etc/postgresql/12/main/pg_hba.conf
```

Adicionar a linha abaixo no final do ficheiro (MODIFICAR):

```
host    db_cfssl      u_cfssl        127.0.0.1/32            scram-sha-256
```

Reiniciar servidor Postgresql:
```
sudo service postgresql restart
```

## 3. Criar base de dados e tabelas para armazenar certificados

```
sudo su - postgres 
psql
```

```
CREATE USER u_cfssl WITH PASSWORD 'yR5rS6eO4rG3eI3vI3fT3wY2tJ6uP9jOgQ1fK2xC4qX5rN0gR9iZ1lI6lP1hV9jK';
CREATE DATABASE db_cfssl OWNER u_cfssl;
\q
```

```
psql --host=localhost --dbname=db_cfssl --username=u_cfssl
```

```
CREATE TABLE certificates (
  serial_number            bytea NOT NULL,
  authority_key_identifier bytea NOT NULL,
  ca_label                 bytea,
  status                   bytea NOT NULL,
  reason                   int,
  expiry                   timestamptz,
  revoked_at               timestamptz,
  pem                      bytea NOT NULL,
  PRIMARY KEY(serial_number, authority_key_identifier)
);
```

```
CREATE TABLE ocsp_responses (
  serial_number            bytea NOT NULL,
  authority_key_identifier bytea NOT NULL,
  body                     bytea NOT NULL,
  expiry                   timestamptz,
  PRIMARY KEY(serial_number, authority_key_identifier),
  FOREIGN KEY(serial_number, authority_key_identifier) REFERENCES certificates(serial_number, authority_key_identifier)
);
\q
```

## 4. Configurar o CFSSL:
```
mkdir ca; cd ca
```

Copiar os ficheiros de configuração (ca-csr.json, ca-config.json, ocsp.csr.json, db-config.json)

Criar CA
```
cfssl gencert -initca ca-csr.json -loglevel=0| cfssljson -bare ca -
```

Criar certificado OCSP e assinar com o CA:
```
cfssl gencert -ca ca.pem -ca-key ca-key.pem -config ca-config.json -profile="ocsp" ocsp.csr.json| cfssljson -bare server-ocsp -
```

Correr servidor CA:
```
cfssl serve -address=0.0.0.0 -port=8888 -db-config=db-config.json -loglevel=0  -ca-key=ca-key.pem -ca=ca.pem -config=ca-config.json -responder=server-ocsp.pem -responder-key=server-ocsp-key.pem
```

Criar base de dados do OCSP:
```
cfssl ocspsign -ca ca.pem -responder server-ocsp.pem -responder-key server-ocsp-key.pem -cert ca.pem | cfssljson -bare -stdout >> ocsp.db
```

Atualizar o servidor do OCSP:
```
cfssl ocsprefresh -db-config db-config.json -ca ca.pem -responder server-ocsp.pem -responder-key server-ocsp-key.pem
```

Gerar resposta OCSP:
```
cfssl ocspdump -db-config db-config.json > ocsp.db
```

Correr servidor OCSP:
```
cfssl ocspserve -address 0.0.0.0 -port 8889 -responses ocsp.db -db-config db-config.json
```
