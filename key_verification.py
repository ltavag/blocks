#! /usr/bin/python

from OpenSSL import crypto
import pprint
import base64
"""

	1.Generate a private key
	lucky@luckyv1:~/.ssh$ ssh-keygen -t rsa -C registrar
						  Generating public/private rsa key pair.
						  Enter file in which to save the key (/home/lucky/.ssh/id_rsa): /home/lucky/.ssh/register
						  Enter passphrase (empty for no passphrase): 
						  Enter same passphrase again: 
						  Your identification has been saved in /home/lucky/.ssh/register.
						  Your public key has been saved in /home/lucky/.ssh/register.pub.
	2. Grab its public key
						  lucky@luckyv1:~/blocks$ openssl rsa -pubout -in ~/.ssh/register 
						  writing RSA key ... output below
	
"""

REGISTER_PRIV_KEY = "/home/lucky/.ssh/register"
REGISTRAR_PUB_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApwOGTyZQOBtd/wYwJCl4
hOkO7BBkejmRg5m/2/kovcek52nmVVsQsUIIDlIfcJPqcRL3iqGRpp+ukaSlrPeR
g69H6k4Nt2FYSK1Euf5vrNbj9EDSy9oVZ5YBaDtOJnuSc77AXK9VZ+GU4E1OqiHL
2GaY1w3X4IigvnNamwzvyqwCYg3TKGsnwmnePCaY+KTNLMspBgfn8iBiMoEkPbfO
cLOPcuCwGi7qCLwLZ5TP5nj2a/NjIJ91Ng4tV+uPKu7hroEu4ltH9Insnkx20Lao
AxFa0hPwphcIGJef9jggOdQBryQhV6jqPKYGbMrJNG0fP/GKdf2gbjEJyZj5odpe
IQIDAQAB
-----END PUBLIC KEY-----"""


def sign_with_private_key(val, keypath):
    with open(keypath, 'r') as f:
        priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
        return crypto.sign(priv_key,
                           val,
                           'sha256')


def verify_register_key(signed, val):
    """
            This function verifies that a certain val has
            been signed by the registration key 
    """
    pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, REGISTRAR_PUB_KEY)
    x509 = crypto.X509()
    x509.set_pubkey(pub_key)

    try:
        crypto.verify(x509, signed, val, 'sha256')
        return True
    except:
        return False


if __name__ == '__main__':
    s = sign_with_private_key('a', REGISTER_PRIV_KEY)
    # print base64.b64encode(s)
    # You'll need to base64 encode these guys if you want to pass them around in the blocks
    print verify_register_key(s, 'a')
