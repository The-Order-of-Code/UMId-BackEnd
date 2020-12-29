#!/bin/bash

cd CA;
cfssl ocspsign -ca ca.pem -responder server-ocsp.pem -responder-key server-ocsp-key.pem -cert ca.pem | cfssljson -bare -stdout >> ocsp.db

cfssl ocspdump -db-config db-config.json > ocsp.db


cfssl ocspserve -address 0.0.0.0 -port 8889 -responses ocsp.db -db-config db-config.json
