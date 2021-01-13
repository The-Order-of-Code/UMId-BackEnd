from .ca import CA
from .config import Config
import json
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import jwt


hostname = Config.hostname
port = Config.port
username = Config.username
path_key = Config.path_key


def getUserHashCertificate(userDict, csr):
    """
    It provides the certificate and MSO of a given user.
        Args:
            userDict(dict): A dictionary structure with user's data to create the MSO.
            csr(str): A PEM-encoded Certificate Signing Request (CSR) to create the user's certificate.
        Returns:
            tuple:  mso (dict): The signed MSO structure.
                    user_cert (str): A PEM-encoded certificate of the user.
    """

    user_dict_ = str(userDict).rstrip().replace("'", '"')
    user = json.dumps(user_dict_)

    ca = CA(hostname, port, username, path_key)

    commands_refresh_OCSP_docker = Config.commands_refresh_OCSP_docker
    command_sign_userdict_docker = Config.command_sign_userdict_docker
    profile = Config.profile

    # Signed certificate
    user_cert = ca.cfssl_sign(csr, profile)
    cert_bytes = bytes(user_cert, 'utf-8')
    cert_loaded = x509.load_pem_x509_certificate(cert_bytes, default_backend())
    pub_key = cert_loaded.public_key().public_bytes(
                                            encoding=serialization.Encoding.PEM,
                                            format=serialization.PublicFormat.SubjectPublicKeyInfo
                                            )
    # with open("./certificate.pem", "r") as f:
        # certificate = f.read()
    # ca.cfssl_revoke(certificate, reason="superseded")

    # Refresh OCSP Responder
    ca.ssh(commands_refresh_OCSP_docker)

    # Sign userDict with CA private key
    user_hash = ca.ssh(f'{command_sign_userdict_docker} "{user}"')
    user_dict_ = str(user_hash).rstrip().replace("'", '"')
    mso = json.loads(user_dict_)

    return mso, user_cert, pub_key


def get_ca_cert(label):
    """ It returns the CA's certificate.
        Args:
            label(str): A string specifying the signer.
        Returns:
            str: certificate (str): a PEM-encoded certificate of the signer.
    """
    ca = CA(hostname, port, username, path_key)

    return ca.cfssl_info(label)['certificate']


def validate(pub_key, token):
    """
    It validates a JWT token.
        Args:
            pub_key(str): A public key to verify the JWT token.
            token(str): A JWT token to validate.
        Returns:
            bool: True: If the token is valid.
                  False: If the token is not valid.
    """

    try:
        if jwt.decode(token, pub_key, algorithms=["ES256"]):
            return True
        else:
            return False
    except:
        return False

    def payload(token):
        return jwt.decode(token, options={"verify_signature": False})



# csr = "-----BEGIN CERTIFICATE REQUEST-----\n" \
#       "MIIBCTCBsAIBADBOMQswCQYDVQQGEwJQVDEOMAwGA1UECAwFQnJhZ2ExDjAMBgNV\n" \
#       "BAcMBUJyYWdhMQ8wDQYDVQQKDAZVbWluaG8xDjAMBgNVBAMMBXRlc3QxMFkwEwYH\n" \
#       "KoZIzj0CAQYIKoZIzj0DAQcDQgAEMfoEtk4zQ4WNrG4beeuE4xGn1NsXuMNcx3DG\n" \
#       "AxybftgbdycKXMwJXXzoFDUBZ7RuNAgX36cb0PctaO29/eLrd6AAMAoGCCqGSM49\n" \
#       "BAMCA0gAMEUCIFR9nJN51ztRTZSWm1sNqzq8bDva0bsatXdBQgOYRGVUAiEA8w2D\n" \
#       "2zMeQPgeo6gUo0NUQ15EjQuPcEwXWv3di1NMZR4=\n" \
#       "-----END CERTIFICATE REQUEST-----\n"

csr = "-----BEGIN CERTIFICATE REQUEST-----\n" \
      "MIIBKDCBzgIBADBOMQswCQYDVQQGEwJQVDEOMAwGA1UECBMFQnJhZ2ExDjAMBgNV\n" \
      "BAcTBUJyYWdhMQ8wDQYDVQQKEwZVbWluaG8xDjAMBgNVBAMTBVRlc3QxMFkwEwYH\n" \
      "KoZIzj0CAQYIKoZIzj0DAQcDQgAEJsJA8WUUJcsg0bORw33FLluwD1Sa2DW4/F0S\n" \
      "FT4p75cFWrhWPx1goWmhzJXpv/qZc1dHZCHYhjn/0weEp9TRDKAeMBwGCSqGSIb3\n" \
      "DQEJDjEPMA0wCwYDVR0RBAQwAoIAMAoGCCqGSM49BAMCA0kAMEYCIQD1WwMzXl7c\n" \
      "ZWqCj5/ZbIH8SBSibtm8WjCuOb3RSt9zzgIhAOCqrkp/LE3AXycZXrTbn9AyoRnp\n" \
      "iOORHphhmiJr7A1c\n" \
      "-----END CERTIFICATE REQUEST-----\n"

user_test2 = {
    'userType': 'STUDENT',
    'username': 'a82144',
    'first_name': 'Filipa',
    'fullName': 'Parente',
    'birthdate': '1940-04-04',
    'picture': '/media/static/defaultAvatar.png' ,
    'course': {
      'id': 1,
      'designation': 'Mestrado Integrado em Engenharia Informática',
      'teachingResearchUnits': 'Escola de Engenharia'
    },
    'number': 82144,
    'year': 5,
    'academicYear': 5
  }

# print(get_ca_cert("CA"))


#print(getUserHashCertificate(user_test2, csr))
