from cfssl import cfssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import paramiko
import time


class CA:
    """ It provides connection to a remote CA server running CFSSL.

        Additional documentation is available at
        https://github.com/The-Order-of-Code/... CORRIGIR
        """
    def __init__(self, hostname, port, username, path_key, ssl=False):
        """ Initialize the CFSSL and paramiko's (SSHClient) object.
            Args:
                hostname (str): Host or IP of remote server.
                port (int): Port number of remote server.
                username (str): User of remote server.
                ssl (bool): Whether to use SSL.
                path_key (str): Path of ssh keys
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.ssl = ssl
        # initialize the cfssl
        self.pki = cfssl.CFSSL(self.hostname, self.port, self.ssl)
        # initialize the SSH client
        self.client = paramiko.SSHClient()
        # ssh private key
        self._k = paramiko.RSAKey.from_private_key_file(path_key)

    def ssh(self, commands):
        """ It provides connection to the ssh server to execute commands remotely.
            Args:
                commands (str): Commands to execute (separated by comma).
        """
        self.client.load_system_host_keys()
        # add to known hosts
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())

        print("connecting...")

        try:
            self.client.connect(hostname=self.hostname, username=self.username, pkey=self._k)
        except:
            print("[!] Cannot connect to the SSH Server")
            exit()

        print("connected")

        stdin, stdout, stderr = self.client.exec_command(commands)
        time.sleep(5)

        stdin.close()
        self.client.close()
        # print("OUTPUT: ", stdout.read())
        print("ERROR: ", stderr.read())
        print("connection closed")
        return stdout.read().decode()

    def cfssl_sign(self, csr, profile):
        """ It signs and returns a certificate.
            Args:
                csr(str): The CSR bytes to be signed (in PEM).
                profile (str): Specifying the signing profile for the signer.
            Returns:
                str: A PEM-encoded certificate that has been signed by the
                   server.
       """
        # Return signed certificate
        certificate = self.pki.sign(hosts=(), certificate_request=csr, profile=profile)
        return certificate

    def cfssl_info(self, label):
        """ It returns information about the CA, including the cert.
            Args:
                label(str): A string specifying the signer.
            Returns:
                dict: Mapping with three keys:
                        certificate (str): a PEM-encoded certificate of the signer.
                        usage (list of str): Key usages from the signing profile.
                        expiry (str): the expiry string from the signing profile.
        """

        return self.pki.info(label)

    def cfssl_revoke(self, certificate, reason):
        """ It provides certificate revocation.
            Args:
                certificate (str): The certificate to be revoked
                reason (str): Identifying why the certificate was revoked; see,
                    for example, ReasonStringToCode in the ocsp package or section
                    4.2.1.13 of RFC 5280. The "reasons" used here are the
                    ReasonFlag names in said RFC.
            Returns:
                The returned result is an empty dict.
        """
        # convert the certificate to bytes and create a cryptography certificate object
        cert_bytes = bytes(certificate, 'utf-8')
        cert = x509.load_pem_x509_certificate(cert_bytes, default_backend())
        # extract serial number from certificate
        serial = str(cert.serial_number)

        # convert the CA certificate to bytes create a cryptography certificate object

        # ca_cert = self.pki.info("CA")
        # ca_cert_bytes = bytes(ca_cert['certificate'], 'utf-8')

        with open("./ca.pem", 'rb') as f:
            ca_cert_bytes = f.read()
        issuer_cert = x509.load_pem_x509_certificate(ca_cert_bytes, default_backend())

        # extract Authority Key ID from certificate
        aki = x509.AuthorityKeyIdentifier.from_issuer_public_key(issuer_cert.public_key()).key_identifier.hex()
        resposta = self.pki.revoke(serial, aki, reason)
        return resposta


# Certificate revocation using OCSP server
# ca.cfssl_revoke(certificate, reason="superseded")
