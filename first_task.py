n = int(input('Enter your length here: '))


def count_n_seq(length):
    st = ''
    for i in range(1, length + 1):
        str_i = str(i) * i
        remaining_length = length - len(st)
        if len(str_i) > remaining_length:
            st += str_i[:remaining_length]
            break
        st += str_i
    return st

