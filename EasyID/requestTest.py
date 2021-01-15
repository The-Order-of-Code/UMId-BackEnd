import json
import requests
from base64 import b64encode

username = "a82142"
password = "lourenco1234"

csr = "-----BEGIN CERTIFICATE REQUEST-----\n" \
      "MIIBJTCBzAIBADBqMQswCQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTEW\n" \
      "MBQGA1UEBxMNU2FuIEZyYW5jaXNjbzEUMBIGA1UEChMLZXhhbXBsZS5jb20xGDAW\n" \
      "BgNVBAMTD3d3dy5leGFtcGxlLmNvbTBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IA\n" \
      "BFt/Nxf9z/4/3HVoP93NJD2GYSOHClTYhcbTAR8pWINN3T5SSL2PQTxkqcQP3s4z\n" \
      "0Jl/SmROVKtvoCl8+J3dJqSgADAKBggqhkjOPQQDAgNIADBFAiEAz1xsa9caHgvf\n" \
      "tds/jp739DLYH2+Ai9V30PGs1Onpo9YCIDwHI79FJESXh40MhH55jik2ZKmccgyz\n" \
      "dGf0h1QsoyRJ\n" \
      "-----END CERTIFICATE REQUEST-----\n"
userUsername = "pedro"
attributes = ["fullName", "first_name", "birthdate", "course.designation"]

api = "cafeteria/addTickets" 
# api = "general/attributes"
# api = "general/all"


credentials = username + ":" + password
base64 = b64encode(credentials.encode('utf-8')).decode('utf-8')
headers = {"Authorization": "Basic " + base64, 'Content-Type': 'application/json'}

data = {"employeeUsername": username, "token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImE4MjEzNCIsInR5cGUiOiJTZW5oYSBjb21wbGV0YSIsImRhdGUiOnRydWUsImRlYnVnZGF0ZSI6IjIwNDEtMTEtMjVUMDE6Mjg6MzEuMTY0NTAxWiJ9.jNjNwQfvq4VbNR6dqbFV67gqE1i24tctJOpM756DoNYZXa-97ohQBWqaI8MN7GEsrUUNmeN00HabN2Z9ofauiQ" }
# data = { 
#       "username": username, 
#       "tickets": [
#       {
#             "ticketType": "Senha completa",
#             "amount": 2
#       },
#       {
#             "ticketType": "Senha completa",
#             "dates": [
#                   "2041-11-25T01:28:31.164501Z",
#                   "2021-11-25T01:28:31.164501Z"
#             ]
#       }
#       ]
# }
# data = { "csr": csr }

session = requests.session()
# response = session.post("http://192.168.1.5:8000/" + api + "/",
# 						data=json.dumps(data),
# 						headers=headers)

response1 = session.post("http://192.168.1.5:8000/cafeteria/validateTicket",
						data=json.dumps(data),
						headers=headers)

# response = session.post("http://192.168.1.5:8000/" + api ,
# 						data=json.dumps(data),
# 						headers=headers)
print(response1.text)