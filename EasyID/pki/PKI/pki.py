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

    userDict["user"].pop("publicKey")
    new_dict = userDict["user"]
    userDict.pop("user")
    new_dict.update(userDict)
    user_dict_ = str(new_dict).rstrip().replace("'", '"')
    
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
