#! /usr/bin/env python

"""
this file used for web testing
"""

import json
import requests
from M2Crypto import EVP, RSA, X509
import base64

req = requests.session()
payload = json.dumps({"user_id":123,"agency_id":"NONE","exp":"2015-09-09"})
key_file = "~/Asa/ssh/id_rsa"
private_key = EVP.load_key(key_file)
private_key.reset_context(md='sha1')
private_key.sign_init()
private_key.sign_update(payload)
signature = base64.b64encode(key.sign_final())

headers = {"payload":payload, "token":signature}
url = "" # TODO this is ur url testing
res = req.post("http://192.168.1.81:8004%s"%(url), headers = headers)
