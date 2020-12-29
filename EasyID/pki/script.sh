#!/bin/bash


sudo apt-get install golang-go golang-cfssl postgresql tmux -y


sudo sed '$ a host    db_cfssl      u_cfssl        127.0.0.1/32            scram-sha-256' nano /etc/postgresql/12/main/pg_hba.conf


sudo service postgresql restart


sudo -u postgres psql postgres -f create_user.sql


sudo -u postgres psql "host=localhost port=5432 dbname=db_cfssl user=u_cfssl password=yR5rS6eO4rG3eI3vI3fT3wY2tJ6uP9jOgQ1fK2xC4qX5rN0gR9iZ1lI6lP1hV9jK" -f create_tables.sql


cd CA;

cfssl gencert -initca ca-csr.json -loglevel=0| cfssljson -bare ca -

cfssl gencert -ca ca.pem -ca-key ca-key.pem -config ca-config.json -profile="ocsp" ocsp.csr.json| cfssljson -bare server-ocsp -


cfssl serve -address=0.0.0.0 -port=8888 -db-config=db-config.json -loglevel=0  -ca-key=ca-key.pem -ca=ca.pem -config=ca-config.json -responder=server-ocsp.pem -responder-key=server-ocsp-key.pem



