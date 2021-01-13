import sys
import json
from new_sign import signer
from datetime import date

hash_alg = "SHA-256"
validity = 1

now = date.today()
now_iso = now.isoformat()
validUntil = date(now.year + validity, now.month, now.day).isoformat()

argument = " ".join(sys.argv[1:])

data = json.loads(argument)

userDict = {key: signer(str(data[key]).encode('utf-8')).hex() for key in data}

mso = {
  "digestAlgorithm": hash_alg,
  "valueDigests": {
    "user": userDict
  },
  "validityInfo": {
    "signed": now_iso,
    "validFrom": now_iso,
    "validUntil": validUntil
  }
}

print(mso)
