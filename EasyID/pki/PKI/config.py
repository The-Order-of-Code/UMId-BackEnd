# Configuration file
class Config:
    # Hostname or IP of CA server
    hostname = ""
    # CFSSL port (default 8888)
    port = 8888
    # Username of SSH client
    username = ""
    # Path of SSH key (REMEMBER TO SET IT AS AN ENVIRONMENT VARIABLE)
    path_key = "/home/USERNAME/.ssh/id_rsa"

    commands_refresh_OCSP = """kill $(lsof -t -i:8889);
                  cd ca;
                  cfssl ocsprefresh -db-config db-pg.json -ca ca.pem -responder server-ocsp.pem -responder-key server-ocsp-key.pem;
                  cfssl ocspdump -db-config db-pg.json > ocsp.db;
                  cfssl ocspserve -address 0.0.0.0 -port 8889 -responses ocsp.db -db-config db-pg.json;"""

    command_sign_userdict = "python3 ~/ca/main.py"

    profile = "client"

    ca_cert = """-----BEGIN CERTIFICATE-----
            MIIB5TCCAYygAwIBAgIUMQ3w28mpkt5cLqjDQ13jAX0tbSMwCgYIKoZIzj0EAwIw
            UTELMAkGA1UEBhMCUFQxDjAMBgNVBAgTBUJyYWdhMQ4wDAYDVQQHEwVCcmFnYTEP
            MA0GA1UEChMGVW1pbmhvMREwDwYDVQQDEwh1bWluaG9DQTAeFw0yMDEyMDYyMTIx
            MDBaFw0yNTEyMDUyMTIxMDBaMFExCzAJBgNVBAYTAlBUMQ4wDAYDVQQIEwVCcmFn
            YTEOMAwGA1UEBxMFQnJhZ2ExDzANBgNVBAoTBlVtaW5obzERMA8GA1UEAxMIdW1p
            bmhvQ0EwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAATfMeJrZTzmK226UNf79sd4
            JUeBB2JMoKLmk/WWIJeTBhDaLUKX8DCvceYVEP276m1O+Q5p31XYDjHhyfDUTTij
            o0IwQDAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQU
            TCXQJx/xel3JskHlr6Mdi6ygz8swCgYIKoZIzj0EAwIDRwAwRAIgebImLgMpjscx
            jaAj2wSqBG7EJ7FHB5ZXqSHpEioT20ACIGcYz+JBbmgPb30FBM5niBuMgmSF5C++
            SlIp+18+Sp0W
            -----END CERTIFICATE-----"""
