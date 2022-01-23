from utils import EncryptDecryption as ed, TextProcessor


def encrypt(plain, key):
    def fill_plain(p_txt):
        pl = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
        for jj in range(4):
            for kk in range(4):
                pl[jj][kk] = p_txt[0:2]
                p_txt = p_txt[2:]
        return pl

    # 0th round
    obj = ed(plain=plain, key=key)
    plain_txt = obj.add_round_key(obj.plain, obj.key[0])
    plain = fill_plain(plain_txt)

    # 1th to 9th round
    for i in range(1, 10):
        transform_p = obj.sub_bytes_transform(plain)
        shifted_p = obj.shift_rows(transform_p)
        mixed_p = obj.mix_column(shifted_p)
        plain_txt = obj.add_round_key(mixed_p, round_key=obj.key[i])
        plain = fill_plain(plain_txt)

    # 10th round
    transform_p = obj.sub_bytes_transform(plain)
    shifted_p = obj.shift_rows(transform_p)
    sh_p = ''
    for j in range(4):
        for k in range(4):
            sh_p += shifted_p[k][j]
    p = obj.add_round_key(sh_p, obj.key[10])
    return p


text = 'hi im reza'
hex_txt = TextProcessor.string_to_hex(text)
plain = hex_txt + '000000000000'
# print(TextProcessor.hex_to_binary(plain))
binary_plain = TextProcessor.hex_to_binary(plain)

# binary to hex bug! let's hardcode
# if binary_plain[-1] == 0:
#     new_binary_plain = binary_plain[:-1]+'1'
# else:
#     new_binary_plain = binary_plain[:-1] + '0'
# new_plain = TextProcessor.binary_to_hex(new_binary_plain)

cipher = encrypt(plain=plain, key='2B7E151628AED2A6ABF7158809CF4F3C')
print(cipher)
print(TextProcessor.hamming(TextProcessor.hex_to_binary(cipher), TextProcessor.hex_to_binary(plain)))

new_binary_plain = "01101000011010010010000001101001011011010010000001110010011001010111101001100001000000000000000000000000000000000000000000000001"
new_plain = TextProcessor.binary_to_hex(new_binary_plain) + '000000'

new_cipher = encrypt(plain=new_plain, key='2B7E151628AED2A6ABF7158809CF4F3C')
print(new_cipher)
print(TextProcessor.hamming(TextProcessor.hex_to_binary(new_cipher), TextProcessor.hex_to_binary(new_plain)))

print(TextProcessor.hamming(TextProcessor.hex_to_binary(new_cipher), TextProcessor.hex_to_binary(cipher)))

