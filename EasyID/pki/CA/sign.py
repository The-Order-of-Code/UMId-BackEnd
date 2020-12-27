# from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import os


def signer(data):
    """ It signs a message with the CA private key with ECDSA algorithm.
        Args:
            data (bytes): Message to sign.
        Returns:
            bytes: A signature of the message that has been signed by the
               server.
    """
    # SET CA PRIVATE KEY AS AN ENVIRONMENT VARIABLE
    path = os.environ.get('CA_PRIVATE_KEY_PATH')
    with open(path, 'rb') as f:
        ca_private_bytes = f.read()

    # Serialize private key
    loaded_private_key = serialization.load_pem_private_key(
        ca_private_bytes, password=None, backend=default_backend())

    signature = loaded_private_key.sign(data, ec.ECDSA(hashes.SHA256()))

    return signature


def verifier(signature, data, public_key):
    """ It verifies a signature with ECDSA algorithm.
        Args:
            signature (bytes): Signature to verify.
            data (bytes): Message to sign.
            public_key (EllipticCurvePublicKey): Public key to verify the signature.
    """
    try:
        public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
    except:
        print("The signature verification failed.")


# with open("./ca.pem", 'rb') as f:
#     ca_cert = f.read()
#
# cert = x509.load_pem_x509_certificate(ca_cert, default_backend())
# public = cert.public_key()
# #
# print(type(public))
# data = b"Test"
# print(verifier(signer(data), data, public))
