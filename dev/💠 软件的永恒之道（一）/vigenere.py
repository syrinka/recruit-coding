from typing import Iterator


class Vigenere(object):
    """维吉尼亚密码加解密

    适用于加解密 [a-z] 范围内的明文

    Usage:

    engima = Vigenere(key)
    cipher = engima.encrypt(plain)
    decrypted = engima.decrypt(cipher)
    """

    # chr(97) == 'a'
    # a~z == 97~122, 将其对齐到 0~25
    _bias = 97

    def _cycle_key(self) -> Iterator[int]:
        """轮转密钥"""
        while True:
            yield from iter(self._key)

    def __init__(self, key: str) -> None:
        """
        @param key : 密钥
        """
        self._key = [ord(i) - self._bias for i in key]

    def encrypt(self, plain: str) -> str:
        """加密方法

        C = P + K (mod 26)

        @param plain : 明文
        @return cipher : 密文
        """
        cycle = self._cycle_key()
        cipher = []
        for p in plain:
            p = ord(p) - self._bias
            k = next(cycle)
            c = (p + k) % 26
            cipher.append(c)
        return ''.join(chr(c + self._bias) for c in cipher)

    def decrypt(self, cipher: str) -> str:
        """解密方法

        P = C - K (mod 26)

        @param cipher : 密文
        @return plain : 明文
        """
        cycle = self._cycle_key()
        plain = []
        for c in cipher:
            c = ord(c) - self._bias
            k = next(cycle)
            p = (c - k) % 26
            plain.append(p)
        return ''.join(chr(c + self._bias) for c in plain)


if __name__ == '__main__':
    key = 'hezelnut'
    plain = 'heavenascensiondio'

    engima = Vigenere(key)
    cipher = engima.encrypt(plain)
    decrypted = engima.decrypt(cipher)

    print('plain:', plain)
    print('cipher:', cipher)
    print('same:', plain == decrypted)
