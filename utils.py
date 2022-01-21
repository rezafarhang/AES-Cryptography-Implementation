from typing import List
import numpy as np


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

    def hex_to_binary(self, value) -> str:
        # 2-2
        pass

    @staticmethod
    def symbolic_parsing(hexadecimal: str) -> list:
        binary = TextProcessor.hex_to_binary(hexadecimal)
        symbolic_result = []
        for index, character in enumerate(binary[::-1]):
            if character == '1':
                symbolic_result.append(index)
        return symbolic_result

    @staticmethod
    def hamming(x: str, y: str) -> int:
        distance = 0
        for i in range(31, -1, -1):
            x_bit = int(x, 2) >> i & 1
            y_bit = int(y, 2) >> i & 1
            distance += not (x_bit == y_bit)
        return distance
        pass


class EncryptDecryption:
    def __init__(self, plain: str):
        self.plain = plain
        self.bytes_transform_table = []
        self.key = ""

    def sub_bytes_transform(self, value: List[list]) -> List[list]:
        pass

    @staticmethod
    def shift_rows(value: List[list]) -> List[list]:
        shifted_list = [list(np.roll(value[0], 0)), list(np.roll(value[1], 1)),
                        list(np.roll(value[2], 2)), list(np.roll(value[3], 3))]
        return shifted_list

    def mix_column(self, value: List[list]) -> List[list]:
        pass

    def add_round_key(self, value: List[list]) -> List[list]:
        pass

    def _key_expansion(self, value: List[list]) -> List[list]:
        pass

