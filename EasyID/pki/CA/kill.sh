#!/bin/sh

kill $(lsof -t -i:8889)

cfssl ocsprefresh -db-config db-config.json -ca ca.pem -responder server-ocsp.pem -responder-key server-ocsp-key.pem
cfssl ocspdump -db-config db-config.json > ocsp.db
cfssl ocspserve -address 0.0.0.0 -port 8889 -responses ocsp.db -db-config db-config.json
