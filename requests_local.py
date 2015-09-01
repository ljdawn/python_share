#! /usr/bin/env python

"""
this file used for web testing
"""

import io
import json
import requests
from M2Crypto import EVP, RSA, X509
import base64

req = requests.session()
payload = json.dumps({"user_id":30541,"agency_id":13244,"exp":"2018-09-09"})
key_file = "/home/Asa/ssh/id_rsa"
private_key = EVP.load_key(key_file)
private_key.reset_context(md='sha1')
private_key.sign_init()
private_key.sign_update(payload)
signature = base64.b64encode(private_key.sign_final())

headers = {"payload":payload, "token":signature}
url = "http://192.168.1.81:8004%s"
jwt_url = "https://agency-stage.nixle.com/api/publication_jwt/30541/"

def jwt_request(url):
    req = requests.session()
    req.get(url, headers = headers)
    print req.content

def request(url):
    req = requests.session()
    file = io.open("README.rst", "rb")
    files = {"file":file}
    request = req.post(url%("api/user/agencies/"), files=files, stream = True)
    print request.content

if __name__ == 'main':
    pass
