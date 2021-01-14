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
    print(userDict)
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

# user_test2 = {
#     'userType': 'STUDENT',
#     'username': 'a82144',
#     'first_name': 'Filipa',
#     'fullName': 'Parente',
#     'birthdate': '1940-04-04',
#     'picture': '/media/static/defaultAvatar.png' ,
#     'course': {
#       'id': 1,
#       'designation': 'Mestrado Integrado em Engenharia Informática',
#       'teachingResearchUnits': 'Escola de Engenharia'
#     },
#     'number': 82144,
#     'year': 5,
#     'academicYear': 5
#   }

user_test2 = {
    'user': {
        'userType': 'STUDENT', 
        'publicKey': None, 
        'username': 'a82134', 
        'first_name': 'Filipa', 
        'fullName': 'Filipa Correia Parente', 
        'birthdate': '1997-12-12', 
        'picture': '/9j/4AAQSkZJRgABAQAAAQABAAD/4QBaRXhpZgAATU0AKgAAAAgAAgESAAMAAAABAAEAAIdpAAQAAAABAAAAJgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAoKADAAQAAAABAAAAyAAAAAAAAP/bAEMACQYHCAcGCQgHCAoKCQsNFg8NDAwNGxQVEBYgHSIiIB0fHyQoNCwkJjEnHx8tPS0xNTc6OjojKz9EPzhDNDk6N//bAEMBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIAKgAhgMBIgACEQEDEQH/xAAcAAAABwEBAAAAAAAAAAAAAAAAAQIDBAUGBwj/xAA3EAACAQMDAQcCBQIFBQAAAAABAgMABBEFEiExBhMiQVFhcRQyB4GRscFCoRUWI1JyQ2KS4fD/xAAZAQADAQEBAAAAAAAAAAAAAAABAgQDAAX/xAAmEQACAgICAgEDBQAAAAAAAAAAAQIRAyESMUFRE4GRoSJhcbHR/9oADAMBAAIRAxEAPwDruKIClUVYmgWKGKOjrgBUMUdCuOBijAoUoUQBAUdCjFccClDpRUoUQBgUMUoUK44ICjAoxR0TgAUKMUK44hmk0ZNNM4FIMLJot1MNLSe9rrCSd1GG96i9770BKK4FEsNSt6gckCoYlxWe7R9rLPR4iJH3SHoicsfj0FdZ1Wat7mGMZkkCj3qDP2g0u3OJbtBXFNY7balqLtskMMZPCp1I+apVuHmbc8rH5JzQ5B4noiy1zTb19lrdRyN6A1YrIh4DAmvNsV5JbyK8Mrq69Cpq20btVqtjfAtcu2TnDng1ykdwPQK0dU/Z/W4NXsluIjhukieamrbIPnToRiqOkZo6IBY5oUS0KJxWSSYqLLOAaEz9agTScmsLNUh5rjk0n6ioJk5oBqVsZInfUUXf8VFBpm9uFtraSdzhUGc1yZ1FX2t7TjSrburfDXMg8Iz9o9a5FqF9JPK8krtJI33MT+1Ttf1CS9u5ppCSzn9B5CqTILHgs3t0pkd0LgZmznp61Mt1MjDbknyp3R9GutVlIQDavXPAHzW30jsnHasrzuZG9+gpMmWMTWGFyM5a6dLMMhAfyNK1ixaIwsq4Krgkj3rokFhEv2rR3mkQ3cRSRMcfdU3z/qN/gSRk+yWsXGl3iyEkxZAdR6V2Kzu1miSVDlGGQR5iuL32m3GlzMAMxk8HyPz6VtPw81j6m3ksJSBJFyAT5VXiyJkmWDR0AN6UoGm0ziliqCaxwGhSRQrjrM/O3Wqyd+TU+5PWqqU+I1MylBA04ppkGlrShHs1n+21x3OhuATl3A/KrzNZD8SLlYtIiBON0uMfAopAObXs26TaOpGTUjS7Ka9nSGMfPHQVUxuZJct1c5+BW27Nz/SJmG1knkYbnKjpTZHxWh8aTezZ6Fp8VlZrFGvQcnHJNXCJnFZ2z7RQpIIbmzuYCeMuvBNaS3kWQAqcq3IqCUXeyyL0P28eW5FTXjATgc4qvl1Oz04g3blM+gzTS9qtLnLCNpTjz7sgUVDQHKwtRs47mFklUYIrJdn5YtP7VRbW2yBu7f0ZTW0luI54O8hYMjDqDXJJL8f5pmkU57uYj4rTAmmzPNTiei4jlc04Kg6PN9RYwS/74wf7VPAr0ls8xqnQYoUYoVwDLXJ61VynxGrC6brVXIfEalZUgA04DTINLBoBHCa5Z+KGod/qUVkjeGEeL/kef2xXS5pRGhYkcVxztPItxrN1cEghpDgU0ewMhaXad7cAkZboB6VsYI7yNxFEREqrxhc7j6VnuyiibVnB5CR5+TmujQwxyqMgZFZ5Z1IoxY7joqbXv306SS8Ybw5AXHJGTg/t+taDspd99CFn6jpVdqEKBdpOAeo9amdnl8bcYXoKxyTT2awhWmx/WZne52RwBiThSx4qrsNYuH79BZoVhJDbV9MeR+avNQ08XYDq5DKc4pVhpkaKQyAsep9a6EopbOcJXoTpqJIjSxAqHGSoPH6eVcd3ldXnO7JNw5P/AJGu8vHHBCxUBcDnj2rg0ETzak7AffIW/vmtMDtsyzLo9Ddh5++0G3y2So21pBXP/wAMr4PBcWm7lSGH8/xXQFq7G7RBkVSFr0oUVCnEMVcyVXu2SafuH5NRWPNRsrQoGjZ9qk02DVfrN+LGzeUnkDj5oBKvtXra2duYYz/rODk/7RXM7hmkdnPyPmpepXr3tyzux8R6nzpsRhbYuRwWx+dOlQtkzsmDDq5z/XEf3rpWlyA5BFcx0q5WPUbeY8BjtPsDxXRdOIWZSCQDU+fsqwOkL1aN3mDA5VRyo61J7P3QXwzQOpB496qr+7kttRdJEBiJyJTyPjFaKwCzWyyi8tACpbazEEVlxbRrZKkd5g7xI0bA4+al2NxHJBmQYcVV3epmBVWNFu2Y7QLc8j3JPlUi0VpIAy+Etz8UtcWOmmDW7xYNLu5s4CRH9Tx/NcsBht5XKfdwFNar8Q78WWmQWgbL3M4B91HJrDXRYFTnzwapxR1ZNmlbNx+H+o/S69bBj4JyYz8n/wCFdpjPlXnLTJ2hVJ1bDwShwfg13/Sbtbu0imU5DqD+dU4n4I8y8lkKFEKFUE5zuVsmmSaU5prdURYGWwKwfb++bvI7YE7V8RHqa20jhQSTXNO1kou9Sdo+dpxXR7OZQIe8kUeZOPin55jKO7j5AbGB8VDP+ju58QGf71baVCqrGzjLOcitJa2LEiXtu8FshfwueQB5Vr+yutfXWarKcXEWFf396zWpxu6uzZPpUvsfCQ8/UHIP9qzmouBrBtSN/HCt0QXwatbaztwwAUn8qotNuDE4WXOK01tdQqV5H61JtFiJkNnFEuQmCep/imby9gsLeSad1jijUlmPQCjnvc5EXibyFUHay2a40O5jbJZ1pe3sV3WjmHarXH17WDdglYUBWBT5DPX5JqYm24iIHLABwPcVTCxkVXGMbG546ZqztQRBJKGAeIgD3q90lSJKd2yRYSqHeI9GXA967J+HeofUaNFEz+OHwEfFcLkkKlJEOBuH5VuOxuvHTbwCQ4SXkr710XTFlG0dyjbK0KrNM1S3vIg8Einjlc8ihVSkiXgzEuajyyqgOT0o7iURoTjJPQVh+0euSRSmBXwx+7HlUdFZYa7ryxo8MDAuRywPSsXLMSzSEdTkZ86S8vfNuY+H9zTohaTxSeHjP/EUy0BlUqbpjv6EZqwspz30QbgBv0pgx73ZgMeQHtRbTnjruA49aa0wJbNGIRdWRIHIbafyqV2dtzDPKCD0FTuz1g76dIXXEu/kE9fX86ttOsNmSyFGJ/qGDUk5dovWOlY59PxvHNWllGhGTHziiggyu1hU+GAoKxsI5DEPQACoes7RaOz42gZ5qzjQ49qzHaSaa9AtrGOSZT1aNSR+tBJsK2ZnQdP/AMVmv4/CpkGFyOpGTWdureS1kaGZSjKenqK6DY9nL2306VoJUNyZUYBDkKV5xn1qB2m0ia6iguYEWSN1DDyK8nI/XNUQm72NkwpwTRiolURkzfbuAq2kgUrui5XlhjqOag6hbSQRNC6MrDDU7oV0VDpLkrtI5rVu0RVTosrLU7qEYEzA4+5DyfkUKjzWDSNn6dyDyDgihQtewcX6NvdyeH2BzXL9XRrvU55iQFLnB9q2uvaj4JLeBsv/ANRgPtHvWK2yXt8sEeQGOAf3NOKlYm3hy4SFTI/ketXn+GvFYyvOpMmOfarSzj0/R5ogMEom5mPJLeQpi+u77UI51tbYwRHrJJwcewpHJ2bqCSKBkjaSBIkAVchvehFbq105ABw4IxVjb2kdvaB5P6SfF74/9ipemaduiVmPLnj34ruWjoRuZrNDiWCcJKFZpYhKi+ROKvp4Z7mATTcGLgKR0Bqkji7rTba7yWa2POOoXzrRqivnvbkGKUBoyDxjqKwaPQtOJDtogXyRU4qOMVFtyvJU5HQVJRqzolap0IlVZcWzPsE33N6KOp/j86fmeew0wsigiQCOMcY54AHtUXdFLKySK2W6H/tHp8n9qetoHu7sSCU/RwnbEWPBP9R/inj1o0jGlb/kct7ORO4glmCGJN7gepqDJpUQ0+NIpujHAz6nP81YotsVu55ZmYnwg0xJDbGCBUkIJNMh7b0/6MxrvZ7Moldd/g27fL86pl7OLCj3NtEVaM52Hoa3WpwTjwxyBl20VqJUsJjLHuU8E4rldgaTVlNaNZXdtGVkMEqjDxuOnxQqddWdncwRsV7uQdSOM0K6rHjGbXn7GS7SQK9k0i+Eh1LbeARnnNZaztp01APCF3sTgnoAfOtZqcu+NogQMqWYn+kCslp0zm6d2GQhGPfmqJHl40ajQ7dbQmQp310xHjcZ28f2pjU7i4czJDwWPiepU1wEnljhJDSlcsevNRruLu0kd3CdAoPnmsS2fHVFU9tK6QWm7dI7lz6AeZP6VtLXTIIxbK0vAHTNQdI0bu7M3dy+HkYdTyF9K0CxWolgycjFF6R2KKu9+RFrBEtpcqsnihcnGeoqTp5tolaK4BZ7dlKbTkPG3II/ajhjsheXCE4VxUawkFvdpHt71EDIvrsPl+Rx+tI2kzbHb19fRZysjXDd1GUTqM0Z3FdqDLEVIf6i6tEcRBRGdrfFRJo5JWRYH2sx2AZ/WkadmfG5AkmeS3YNbHvZfBGcfaPapiiOOARSSbUgj2qinz86UI5QSJ2RI4FIz5k1HU2sNqTgu7nqfOnWjTT6QsvaRaaFCEl2p2U2UkttGUK4xRT3Me23iSD0zThuoZNQjEkOMLRBt735fZGvbVTLL3E/AGOtHbi5i0uTo6lsUqSK2mnmaOTb7ZpMUc0WlO0Um4GTpXeGxfSb9DbyQtFGJI9pxnkUKdeYd3GJ4eQvBxQrOUmnSNY8ktX9zmEcNzfmVGzChKq7edWkGhw2ljcRwlXVeNx6t50KFbT7ZJgS4pjOp2AguYfpn2MAC5PPt/NO2emI1+73M3e7U3AYwM0KFBdDZNM0XcQfQH/UJ5/mnGe1X6cgZ9eDQoUJs0gr/JIjNqdQ5XAK+9O21vaPJNsco6ncjA9DQoUL2NJUnvwh20ubiWYJI6pG52uVPBPrSbbR57fULy4efwREGNvXIoUKeMU9szyTcJ8V5/0VO0H0zPNKXd2pUk8KLBFFFzxzihQrNyaN4RUu/wBx9ruRr5NsHCjj+9KhvA1/IZoQQB50KFNyd/UCxx/Ayhs5I5pD4Sc+1E9s6aZCLeTIdyaFCjHaMpScZUvYJruS2CiWMHjjihQoUknsrxYYSgm0f//Z'}, 'course': {'id': 1, 'designation': 'Mestrado Integrado em Engenharia Informática', 'teachingResearchUnits': 'Escola de Engenharia'}, 
        'number': 82134, 
        'year': 5, 
        'academicYear': 5
    }

print(get_ca_cert("CA"))


#print("user test", getUserHashCertificate(user_test2["user"], csr))
