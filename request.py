#! /usr/bin/env python

"""
this file used for web testing
"""

import json
import requests
import rsa

req = requests.session()
key_file = open("../id_rsa","r")
pri_key = "".join(key_file.readlines())
key_file.close()

payload = json.dumps({"username":123, "password":123})
signature = rsa.sign(payload, pri_key, "SHA-1")
headers = {"payload":payload, "token":signature}
res = req.post("http://127.0.0.1:8001", headers = headers)

print res
