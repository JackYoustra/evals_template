from abc import ABC, abstractmethod
from evals.cipher import walnut53_encode, walnut53_decode


class EncodingScheme(ABC):
    @abstractmethod
    def encode(self, text: str) -> str:
        pass

    @abstractmethod
    def decode(self, text: str) -> str:
        pass


class IdentityEncoding(EncodingScheme):
    def encode(self, text: str) -> str:
        return text

    def decode(self, text: str) -> str:
        return text


class Walnut53Encoding(EncodingScheme):
    def encode(self, text: str) -> str:
        return walnut53_encode(text)

    def decode(self, text: str) -> str:
        return walnut53_decode(text)


# You can add more encoding schemes here as needed


def get_encoding_scheme(scheme_name: str) -> EncodingScheme:
    schemes = {
        "identity": IdentityEncoding(),
        "walnut53": Walnut53Encoding(),
        # Add more schemes here as they are implemented
    }
    return schemes.get(scheme_name, IdentityEncoding())
