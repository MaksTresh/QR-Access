from config_lab import LAB
import ed25519


class EDDSASigner:
    edDsa_private_key = ed25519.SigningKey(LAB['EDDRSA_PRIVATE_KEY'], encoding="hex")

    def __init__(self, data):
        self.data = data

    def get_signed_data(self):
        return EDDSASigner.edDsa_private_key.sign(self.data.encode('utf8'), encoding='hex')
