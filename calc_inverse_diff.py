import os 
from typing import List


diffusion = [0xf26cb481,0x16a5dc92,0x3c5ba924,0x79b65248,0x2fc64b18,0x615acd29,0xc3b59a42,0x976b2584,
0x6cf281b4,0xa51692dc,0x5b3c24a9,0xb6794852,0xc62f184b,0x5a6129cd,0xb5c3429a,0x6b978425,
0xb481f26c,0xdc9216a5,0xa9243c5b,0x524879b6,0x4b182fc6,0xcd29615a,0x9a42c3b5,0x2584976b,
0x81b46cf2,0x92dca516,0x24a95b3c,0x4852b679,0x184bc62f,0x29cd5a61,0x429ab5c3,0x84256b97]



def compute_inverse(bit_matrix: List):
    """
    Computes inverse using Gaussian-Jordan elimination. 
    https://online.stat.psu.edu/statprogram/reviews/matrix-algebra/gauss-jordan-elimination

    Input:
    - bit_matrix: a matrix of individual bits from the diffusion array. 32x32
    """
    tmp_matrix = [[1 if i == j else 0 for i in range(32)] for j in range(32)]
    # create a deep copy as we will modify it
    bit_matrix = [[bit_matrix[i][j] for j in range(32)] for i in range(32)]

    # for every column
    for col in range(32):
        # for every row starting from col ( we know all columns before col are 0)
        flag = 0
        for i in range(col, 32):
            # if we found a row that can be pivot on (for column col)
            if bit_matrix[i][col] == 1:
                # swap it to col
                tmp = bit_matrix[i]
                bit_matrix[i] = bit_matrix[col]
                bit_matrix[col] = tmp

                # also swap tmp_matrix
                tmp = tmp_matrix[i]
                tmp_matrix[i] = tmp_matrix[col]
                tmp_matrix[col] = tmp

                # assuming the matrix is invertible
                flag = 1
                #print("bit matrix after swap at {}th column: {}".format(j, bit_matrix))
                #print("inverse matrix after swap at {}th column: {}".format(j, tmp_matrix))
                break
        if flag == 0:
            print("warning: matrix not invertible")

        # then start to pivot, make all other rows this column 0
        for i in range(32):
            if i != col and bit_matrix[i][col] == 1:
                for k in range(32):
                    bit_matrix[i][k] ^= bit_matrix[col][k]
                    tmp_matrix[i][k] ^= tmp_matrix[col][k]


    return tmp_matrix


def bits_to_u32_reverse(bits: List):
    """Converts list of bits into unsigned 32bit integers."""
    res = 0
    for i in range(32):
        res += bits[i] * 2 ** i
    return res


def u32_to_bits_reverse(num: List):
    """
    Converts a single 32 bit from the diffusion array into a list of individual bytes.

    Doc on conversion in C++: https://stackoverflow.com/questions/64060850/how-to-convert-an-unsigned-integer-into-32-bit-binary-representation
    """
    # define an array 32 items long of zeros
    bits = [0 for _ in range(32)]
    for i in range(32):
        bit = num % 2
        bits[i] = bit
        # Remember: // in Python 3 does floor division to result in a round number.
        num = num // 2

    return bits


# inverse diffuse array calc - for test purposes:

#diff_matrix = list(map(lambda x: u32_to_bits_reverse(x), diffusion))
#inverse_diff_matrix = compute_inverse(diff_matrix)
#inverse_diff = list(map(lambda x: bits_to_u32_reverse(x), inverse_diff_matrix))
#print(inverse_diff)