from ca import CA
from .config import Config
import json


def getUserHashCertificate(userDict, csr):

    user = json.dumps(userDict, sort_keys=True)
    hostname = Config.hostname
    port = Config.port
    username = Config.username
    path_key = Config.path_key
    commands_refresh_OCSP = Config.commands_refresh_OCSP
    command_sign_userdict = Config.command_sign_userdict
    profile = Config.profile

    ca = CA(hostname, port, username, path_key)

    # Signed certificate
    user_cert = ca.cfssl_sign(csr, profile)
    # Refresh OCSP Responder
    ca.ssh(commands_refresh_OCSP)

    # Sign userDict with CA private key
    user_hash = ca.ssh(f"{command_sign_userdict} {user}")

    return user_hash, user_cert


# TESTES
csr = "-----BEGIN CERTIFICATE REQUEST-----\n" \
      "MIIBJTCBzAIBADBqMQswCQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTEW\n" \
      "MBQGA1UEBxMNU2FuIEZyYW5jaXNjbzEUMBIGA1UEChMLZXhhbXBsZS5jb20xGDAW\n" \
      "BgNVBAMTD3d3dy5leGFtcGxlLmNvbTBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IA\n" \
      "BFt/Nxf9z/4/3HVoP93NJD2GYSOHClTYhcbTAR8pWINN3T5SSL2PQTxkqcQP3s4z\n" \
      "0Jl/SmROVKtvoCl8+J3dJqSgADAKBggqhkjOPQQDAgNIADBFAiEAz1xsa9caHgvf\n" \
      "tds/jp739DLYH2+Ai9V30PGs1Onpo9YCIDwHI79FJESXh40MhH55jik2ZKmccgyz\n" \
      "dGf0h1QsoyRJ\n" \
      "-----END CERTIFICATE REQUEST-----\n"


user = {
    "user": {
        "portrait": "",
        "username": "",
        "password": "",
        "firstName": "",
        "fullName": "",
        "birthDate": "",
    },
    "course": {
          "designation": "",
          "teachingResearchUnits": ""
     },
    "number": None,
    "year": None,
    "academicYear": None,
}

print(getUserHashCertificate(user, csr))
