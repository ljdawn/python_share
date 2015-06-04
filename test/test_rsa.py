"""
    jwt version -- python_jwt
"""
import jwt, Crypto.PublicKey.RSA as RSA, datetime
key = RSA.generate(2048)
priv_pem = key.exportKey()
pub_pem = key.publickey().exportKey()
payload = { 'foo': 'bar', 'wup':90,}
priv_key = RSA.importKey(priv_pem)
pub_key = RSA.importKey(pub_pem)
priv_key = open("ssh/id_rsa", "r")
token = jwt.generate_jwt(payload, priv_key,
                         'RS256',datetime.timedelta(minutes=5))
header, claims = jwt.verify_jwt(token, pub_key, ['RS256'])
print header
print claims
for k in payload: assert claims[k] == payload[k]
