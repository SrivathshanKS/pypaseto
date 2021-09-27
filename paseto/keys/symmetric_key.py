from paseto.protocols.protocol import Protocol
from paseto.protocols.v3 import ProtocolVersion3
from paseto.protocols.v4 import ProtocolVersion4
from paseto.protocols.v2 import ProtocolVersion2
import secrets
from Cryptodome.Protocol.KDF import HKDF
from Cryptodome.Hash import SHA384


class SymmetricKey:
    INFO_ENCRYPTION = b"paseto-encryption-key"
    INFO_AUTHENTICATION = b"paseto-auth-key-for-aead"

    def __init__(self, key_material: bytes, protocol: str):
        self.key = key_material
        if not protocol:
            protocol = ProtocolVersion4
        self.protocol = protocol

    @classmethod
    def generate(cls, protocol=None):
        if not protocol:
            protocol = ProtocolVersion4
        return cls(
            key_material=secrets.token_bytes(protocol.symmetric_key_byte_length),
            protocol=protocol,
        )

    @classmethod
    def v3(cls, key_material) -> "SymmetricKey":
        return cls(key_material=key_material, protocol=ProtocolVersion3)

    @classmethod
    def v4(cls, key_material) -> "SymmetricKey":
        return cls(key_material=key_material, protocol=ProtocolVersion4)

    def encode(self):
        return b64encode(self.key)

    @classmethod
    def from_encoded_string(cls, encoded: str, protocol: Protocol) -> "SymmetricKey":
        return cls(key_material=b64decode(encoded), protocol=protocol)

    def splitV2(self, salt: bytes = None) -> list:
        pass

    def splitV3(self, salt: bytes = None) -> list:
        tmp = HKDF(self.key, 48, self.INFO_ENCRYPTION + salt, SHA384, 1)
        enc_key = tmp[:32]
        nonce = tmp[33:]
        auth_key = HKDF(self.key, 48, self.INFO_AUTHENTICATION + salt, SHA384, 1)
        return enc_key, auth_key, nonce

    def splitV4(self, salt: bytes = None) -> list:
        pass
