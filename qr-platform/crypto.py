import ed25519


class EDDSAVerifier:

    def __init__(self, data, signature, pub_key):
        self.signature = signature.encode('utf8')
        self.data = data.encode('utf8')
        self.eddsa_public_key = ed25519.VerifyingKey(pub_key.encode('utf8'), encoding="hex")

    def is_verified(self):
        try:
            self.eddsa_public_key.verify(self.signature, self.data, encoding='hex')
            return True
        except:
            return False
