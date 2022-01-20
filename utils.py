from typing import List


class TextProcessor:
    def string_to_hex(self, txt: str) -> str:
        # 2-1
        pass

    def hex_to_binary(self, value) -> str:
        # 2-2
        pass

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
