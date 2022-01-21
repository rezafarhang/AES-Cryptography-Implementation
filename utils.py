from typing import List


class TextProcessor:

    @staticmethod
    def string_to_hex(txt: str) -> str:
        hex_txt = ''
        for character in txt:
            hex_txt += hex(ord(character))[-2:]
        return hex_txt

    @staticmethod
    def hex_to_string(hex_txt: str) -> str:
        txt = ''
        for index in range(0, len(hex_txt), 2):
            print(index)
            print(hex_txt[index] + hex_txt[index + 1])
            txt += chr(int(hex_txt[index] + hex_txt[index + 1], 16))
        return txt

    @staticmethod
    def hex_to_binary(hex_txt: str) -> str:
        bin_txt = ''
        for index in range(0, len(hex_txt), 2):
            bin_result = bin(int(hex_txt[index: index + 2], 16))[2:]
            bin_txt += ''.join('0' for _ in range(8 - len(bin_result))) + bin_result
        return bin_txt

    @staticmethod
    def binary_to_hex(bin_txt: str) -> str:
        hex_txt = ''
        for index in range(0, len(bin_txt), 8):
            hex_txt += hex(int(bin_txt[index: index + 8], 2))[2:]
        return hex_txt

    def unknown(self):
        # 2-3
        pass

    def hamming(self, x: int, y: int) -> int:
        # 2-4
        pass


class EncryptDecryption:
    def __init__(self, plain: str):
        self.plain = plain
        self.bytes_transform_table = []
        self.key = ""

    def sub_bytes_transform(self, value: List[list]) -> List[list]:
        pass

    def shift_rows(self, value: List[list]) -> List[list]:
        pass

    def mix_column(self, value: List[list]) -> List[list]:
        pass

    def add_round_key(self, value: List[list]) -> List[list]:
        pass

    def _key_expansion(self, value: List[list]) -> List[list]:
        pass
