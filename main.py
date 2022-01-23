from utils import EncryptDecryption as ed


def encrypt(plain, key):
    def fill_plain(p_txt):
        pl = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
        for jj in range(4):
            for kk in range(4):
                pl[jj][kk] = p_txt[0:2]
                p_txt = p_txt[2:]
        return pl

    # 1th round
    obj = ed(plain=plain, key=key)
    plain_txt = obj.add_round_key(obj.plain, obj.key[0])
    plain = fill_plain(plain_txt)

    # 2th to 9th round
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


print(encrypt(plain='3243F6A8885A308D313198A2E0370734', key='2B7E151628AED2A6ABF7158809CF4F3C'))



