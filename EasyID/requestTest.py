import json
import requests
from base64 import b64encode

username = "username"
password = "pass"
csr = "-----BEGIN CERTIFICATE REQUEST-----\n" \
      "MIIBJTCBzAIBADBqMQswCQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTEW\n" \
      "MBQGA1UEBxMNU2FuIEZyYW5jaXNjbzEUMBIGA1UEChMLZXhhbXBsZS5jb20xGDAW\n" \
      "BgNVBAMTD3d3dy5leGFtcGxlLmNvbTBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IA\n" \
      "BFt/Nxf9z/4/3HVoP93NJD2GYSOHClTYhcbTAR8pWINN3T5SSL2PQTxkqcQP3s4z\n" \
      "0Jl/SmROVKtvoCl8+J3dJqSgADAKBggqhkjOPQQDAgNIADBFAiEAz1xsa9caHgvf\n" \
      "tds/jp739DLYH2+Ai9V30PGs1Onpo9YCIDwHI79FJESXh40MhH55jik2ZKmccgyz\n" \
      "dGf0h1QsoyRJ\n" \
      "-----END CERTIFICATE REQUEST-----\n" \

credentials = username + ":" + password
base64 = b64encode(credentials.encode('utf-8')).decode('utf-8')
headers = {"Authorization": "Basic " + base64}

session = requests.session()
response = session.post("http://127.0.0.1:8000/general/all/",
						data={"csr": csr},
						headers=headers)
print(response.text)