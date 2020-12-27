import sys
from sign import signer
import json
# user = {
#     "user": {
#         "portrait": "",
#         "username": "",
#         "password": "",
#         "firstName": "",
#         "fullName": "",
#         "birthDate": "",
#     },
#     "course": {
#           "designation": "",
#           "teachingResearchUnits": ""
#      },
#     "number": "None",
#     "year": "None",
#     "academicYear": "None",
# }


# my_dictionary = {k: v for k, v in user.items()}
# user = json.dumps(user, sort_keys=True)
# user = user.encode('utf-8')
data = sys.argv[1].encode('utf-8')
# print(type(user))
print(signer(data).hex())
