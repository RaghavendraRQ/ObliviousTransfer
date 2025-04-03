from damgard_jurik import (
    keygen as dj_keygen,
    PublicKey as DJPublicKey,
    PrivateKeyRing as DJPrivateKeyRing,
    EncryptedNumber as DJEncryptedNumber
)


class EncryptedNumber:
    def __init__(self, dj_encrypted_number: DJEncryptedNumber):
        self._dj_number = dj_encrypted_number

    @property
    def public_key(self):
        return PublicKey(self._dj_number.public_key)

    def __repr__(self):
        return f"EncryptedNumber({self._dj_number.ciphertext})"


class PublicKey:
    def __init__(self, dj_public_key: DJPublicKey):
        self._dj_pk = dj_public_key
        self.n = dj_public_key.n

    def encrypt(self, m: int, s: int = 1) -> EncryptedNumber:
        return EncryptedNumber(self._dj_pk.encrypt(m, s))

    def encrypt_list(self, m_list: list, s: int = 1) -> list:
        return [EncryptedNumber(self._dj_pk.encrypt(m, s)) for m in m_list]


class PrivateKeyRing:
    def __init__(self, dj_private_key_ring: DJPrivateKeyRing):
        self._dj_pkr = dj_private_key_ring

    def decrypt(self, c: EncryptedNumber) -> int:
        return self._dj_pkr.decrypt(c._dj_number)

    def decrypt_list(self, c_list: list) -> list:
        return [self.decrypt(c) for c in c_list]


def keygen(n_bits: int = 1024, s: int = 1, threshold: int = 3, n_shares: int = 3):
    dj_pub, dj_priv = dj_keygen(
        n_bits=n_bits,
        s=s,
        threshold=threshold,
        n_shares=n_shares
    )
    return PublicKey(dj_pub), PrivateKeyRing(dj_priv)