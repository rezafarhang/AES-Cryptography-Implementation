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
            # print(index)
            # print(hex_txt[index] + hex_txt[index + 1])
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
    CONSTANT_MATRIX = [[0x02, 0x03, 0x01, 0x01], [0x01, 0x02, 0x03, 0x01],
                       [0x01, 0x01, 0x02, 0x03], [0x03, 0x01, 0x01, 0x02]]

    INVERSE_CONSTANT_MATRIX = [[0x0E, 0x0B, 0x0D, 0x09], [0x09, 0x0E, 0x0B, 0x0D],
                               [0x0D, 0x09, 0x0E, 0x0B], [0x0B, 0x0D, 0x09, 0x0E]]

    def __init__(self, plain: str, key: str):
        # EN for encryption and DE for Decryption
        self.mode = 'EN'
        self.plain = plain
        self.cypher = ''
        self.key: list = self._key_expansion(key.lower())

    SBox = [
        '63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76',
        'ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0',
        'b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15',
        '04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75',
        '09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84',
        '53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf',
        'd0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8',
        '51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2',
        'cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73',
        '60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db',
        'e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79',
        'e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08',
        'ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a',
        '70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e',
        'e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df',
        '8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16'
    ]
    SBoxInv = [
        '52', '09', '6a', 'd5', '30', '36', 'a5', '38', 'bf', '40', 'a3', '9e', '81', 'f3', 'd7', 'fb',
        '7c', 'e3', '39', '82', '9b', '2f', 'ff', '87', '34', '8e', '43', '44', 'c4', 'de', 'e9', 'cb',
        '54', '7b', '94', '32', 'a6', 'c2', '23', '3d', 'ee', '4c', '95', '0b', '42', 'fa', 'c3', '4e',
        '08', '2e', 'a1', '66', '28', 'd9', '24', 'b2', '76', '5b', 'a2', '49', '6d', '8b', 'd1', '25',
        '72', 'f8', 'f6', '64', '86', '68', '98', '16', 'd4', 'a4', '5c', 'cc', '5d', '65', 'b6', '92',
        '6c', '70', '48', '50', 'fd', 'ed', 'b9', 'da', '5e', '15', '46', '57', 'a7', '8d', '9d', '84',
        '90', 'd8', 'ab', '00', '8c', 'bc', 'd3', '0a', 'f7', 'e4', '58', '05', 'b8', 'b3', '45', '06',
        'd0', '2c', '1e', '8f', 'ca', '3f', '0f', '02', 'c1', 'af', 'bd', '03', '01', '13', '8a', '6b',
        '3a', '91', '11', '41', '4f', '67', 'dc', 'ea', '97', 'f2', 'cf', 'ce', 'f0', 'b4', 'e6', '73',
        '96', 'ac', '74', '22', 'e7', 'ad', '35', '85', 'e2', 'f9', '37', 'e8', '1c', '75', 'df', '6e',
        '47', 'f1', '1a', '71', '1d', '29', 'c5', '89', '6f', 'b7', '62', '0e', 'aa', '18', 'be', '1b',
        'fc', '56', '3e', '4b', 'c6', 'd2', '79', '20', '9a', 'db', 'c0', 'fe', '78', 'cd', '5a', 'f4',
        '1f', 'dd', 'a8', '33', '88', '07', 'c7', '31', 'b1', '12', '10', '59', '27', '80', 'ec', '5f',
        '60', '51', '7f', 'a9', '19', 'b5', '4a', '0d', '2d', 'e5', '7a', '9f', '93', 'c9', '9c', 'ef',
        'a0', 'e0', '3b', '4d', 'ae', '2a', 'f5', 'b0', 'c8', 'eb', 'bb', '3c', '83', '53', '99', '61',
        '17', '2b', '04', '7e', 'ba', '77', 'd6', '26', 'e1', '69', '14', '63', '55', '21', '0c', '7d'
    ]

    def sub_bytes_transform(self, value: List[list]) -> List[list]:
        s_box = self.SBox if self.mode == "EN" else self.SBoxInv

        for i in range(4):
            for j in range(4):
                value[i][j] = s_box[int(value[i][j], 16)]

        return value

    @staticmethod
    def shift_rows(value: List[list]) -> List[list]:
        shifted_list = []
        for i in range(4):
            l = np.array(value)[:, i]
            shifted_list.append(list(np.roll(l, -i)))

        # result = []
        # for j in range(4):
        #     temp = []
        #     for k in range(4):
        #         temp.append(shifted_list[k][j])
        #     result.append(temp)
        return shifted_list

    @staticmethod
    def galois_multiple(a, b):
        p = 0
        bit_set = 0
        for i in range(8):
            if b & 1 == 1:
                p ^= a
            bit_set = a & 0x80
            a <<= 1
            if bit_set == 0x80:
                a ^= 0x1b
            b >>= 1
        return p % 256

    def mix_column(self, value: List[list]) -> List[list]:
        def get_col(ls,i):
            column = [ls[0][i], ls[1][i], ls[2][i], ls[3][i]]
            return column

        cons_m = self.CONSTANT_MATRIX if self.mode == "EN" else self.INVERSE_CONSTANT_MATRIX
        mixed_columns = []
        """
        row1 = self.CONSTANT_MATRIX[0]
        col1 = np.array(self.CONSTANT_MATRIX)[:, 0]
        mixed_columns.append(
            self.galois_multiple(row1[0], col1[0]) ^ self.galois_multiple(row1[1], col1[1])
            ^ self.galois_multiple(row1[2], col1[2]) ^ self.galois_multiple(row1[3], col1[3])
        )
        """
        for i in range(4):
            mix = []
            for j in range(4):
                row = cons_m[j]
                col = get_col(value,i)
                hs = hex(
                    self.galois_multiple(row[0], int(col[0], 16)) ^ self.galois_multiple(row[1], int(col[1], 16))
                    ^ self.galois_multiple(row[2], int(col[2], 16)) ^ self.galois_multiple(row[3], int(col[3], 16))
                )[2:]
                hs = ''.join('0' for _ in range(2 - len(hs))) + hs
                mix.append(hs)
            mixed_columns.append(mix.copy())
            mix.clear()
        result = []
        temp = np.array(mixed_columns)
        for i in range(4):
            result.append(list(temp[:, i]))
        res = ''
        for j in range(4):
            for k in range(4):
                res += mixed_columns[j][k]
        return res

    def add_round_key(self, value: str, round_key: str) -> List[list]:
        key = round_key
        res = ''
        for i in range(len(value)):
            a = TextProcessor.hex_to_binary(key[i])
            b = TextProcessor.hex_to_binary(value[i])
            c = int(a, 2) ^ int(b, 2)
            c = TextProcessor.binary_to_hex(bin(c)[2:])
            res += c
        return res

    def _key_expansion(self, key: str) -> List[str]:
        def g(word, r):
            def r_con(r):
                rc = ['01', '02', '04', '08', '10', '20', '40', '80', '1b', '36']
                return rc[r]

            def sub_word(word):
                s_box = self.SBox if self.mode == "EN" else self.SBoxInv
                result = ''
                for i in range(0, 8, 2):
                    result += s_box[int(word[i: i + 2], 16)]
                return result

            def rot_word(word):
                return f'{word[2:]}{word[:2]}'

            word = sub_word(rot_word(word))

            return hex(int(word[0], 16) ^ int(r_con(r)[0], 16))[2:] + \
                   hex(int(word[1], 16) ^ int(r_con(r)[1], 16))[2:] + \
                   hex(int(word[2:], 16) ^ 0)[2:]

        def x_or(w1, w2):
            hex_x_or = ''
            for index in range(len(w1)):
                hex_x_or += hex(int(w1[index], 16) ^ int(w2[index], 16))[2:]
            return hex_x_or

        keys = [key, ]
        for i in range(10):
            k = keys[-1]
            g_result = g(k[24:], i)

            w0 = x_or(g_result, k[:8])
            w1 = x_or(w0, k[8:16])
            w2 = x_or(w1, k[16:24])
            w3 = x_or(w2, k[24:])

            keys.append(w0 + w1 + w2 + w3)

        return keys
