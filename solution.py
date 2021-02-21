import os
import time
import datetime
from typing import List

# XOR imported for clarity. Usually represented by ^
# Note: ixor is the equivilent of ^= but behaves unpredicatbly due to the way classes are defined in Python
# so it is not used here
from operator import xor

# Used to calculate inverse diffusion array
from calc_inverse_diff import compute_inverse, u32_to_bits_reverse, bits_to_u32_reverse


# 1st part of confusion array:
conf1 = [0xac,0xd1,0x25,0x94,0x1f,0xb3,0x33,0x28,0x7c,0x2b,0x17,0xbc,0xf6,0xb0,0x55,0x5d,
0x8f,0xd2,0x48,0xd4,0xd3,0x78,0x62,0x1a,0x02,0xf2,0x01,0xc9,0xaa,0xf0,0x83,0x71,
0x72,0x4b,0x6a,0xe8,0xe9,0x42,0xc0,0x53,0x63,0x66,0x13,0x4a,0xc1,0x85,0xcf,0x0c,
0x24,0x76,0xa5,0x6e,0xd7,0xa1,0xec,0xc6,0x04,0xc2,0xa2,0x5c,0x81,0x92,0x6c,0xda,
0xc6,0x86,0xba,0x4d,0x39,0xa0,0x0e,0x8c,0x8a,0xd0,0xfe,0x59,0x96,0x49,0xe6,0xea,
0x69,0x30,0x52,0x1c,0xe0,0xb2,0x05,0x9b,0x10,0x03,0xa8,0x64,0x51,0x97,0x02,0x09,
0x8e,0xad,0xf7,0x36,0x47,0xab,0xce,0x7f,0x56,0xca,0x00,0xe3,0xed,0xf1,0x38,0xd8,
0x26,0x1c,0xdc,0x35,0x91,0x43,0x2c,0x74,0xb4,0x61,0x9d,0x5e,0xe9,0x4c,0xbf,0x77,
0x16,0x1e,0x21,0x1d,0x2d,0xa9,0x95,0xb8,0xc3,0x8d,0xf8,0xdb,0x34,0xe1,0x84,0xd6,
0x0b,0x23,0x4e,0xff,0x3c,0x54,0xa7,0x78,0xa4,0x89,0x33,0x6d,0xfb,0x79,0x27,0xc4,
0xf9,0x40,0x41,0xdf,0xc5,0x82,0x93,0xdd,0xa6,0xef,0xcd,0x8d,0xa3,0xae,0x7a,0xb6,
0x2f,0xfd,0xbd,0xe5,0x98,0x66,0xf3,0x4f,0x57,0x88,0x90,0x9c,0x0a,0x50,0xe7,0x15,
0x7b,0x58,0xbc,0x07,0x68,0x3a,0x5f,0xee,0x32,0x9f,0xeb,0xcc,0x18,0x8b,0xe2,0x57,
0xb7,0x49,0x37,0xde,0xf5,0x99,0x67,0x5b,0x3b,0xbb,0x3d,0xb5,0x2d,0x19,0x2e,0x0d,
0x93,0xfc,0x7e,0x06,0x08,0xbe,0x3f,0xd9,0x2a,0x70,0x9a,0xc8,0x7d,0xd8,0x46,0x65,
0x22,0xf4,0xb9,0xa2,0x6f,0x12,0x1b,0x14,0x45,0xc7,0x87,0x31,0x60,0x29,0xf7,0x73]

# 2nd part of confusion array:
conf2 = [0x2c,0x97,0x72,0xcd,0x89,0xa6,0x88,0x4c,0xe8,0x83,0xeb,0x59,0xca,0x50,0x3f,0x27,
0x4e,0xae,0x43,0xd5,0x6e,0xd0,0x99,0x7b,0x7c,0x40,0x0c,0x52,0x86,0xc1,0x46,0x12,
0x5a,0x28,0xa8,0xbb,0xcb,0xf0,0x11,0x95,0x26,0x0d,0x34,0x66,0x22,0x18,0x6f,0x51,
0x9b,0x3b,0xda,0xec,0x5e,0x00,0x2a,0xf5,0x8f,0x61,0xba,0x96,0xb3,0xd1,0x30,0xdc,
0x33,0x75,0xe9,0x6d,0xc8,0xa1,0x3a,0x3e,0x5f,0x9d,0xfd,0xa9,0x31,0x9f,0xaa,0x85,
0x2f,0x92,0xaf,0x67,0x78,0xa5,0xab,0x03,0x21,0x4f,0xb9,0xad,0xfe,0xf3,0x42,0xfc,
0x17,0xd7,0xee,0xa3,0xd8,0x80,0x14,0x2e,0xa0,0x47,0x55,0xc4,0xff,0xe5,0x13,0x3f,
0x81,0xb6,0x7a,0x94,0xd0,0xb5,0x54,0xbf,0x91,0xa7,0x37,0xf1,0x6b,0xc9,0x1b,0xb1,
0x3c,0xb6,0xd9,0x32,0x24,0x8d,0xf2,0x82,0xb4,0xf9,0xdb,0x7d,0x44,0xfb,0x1e,0xd4,
0xea,0x5d,0x35,0x69,0x23,0x71,0x57,0x01,0x06,0xe4,0x55,0x9a,0xa4,0x58,0x56,0xc7,
0x4a,0x8c,0x8a,0xd6,0x6a,0x49,0x70,0xc5,0x8e,0x0a,0x62,0xdc,0x29,0x4b,0x42,0x41,
0xcb,0x2b,0xb7,0xce,0x08,0xa1,0x76,0x1d,0x1a,0xb8,0xe3,0xcc,0x7e,0x48,0x20,0xe6,
0xf8,0x45,0x93,0xde,0xc3,0x63,0x0f,0xb0,0xac,0x5c,0xba,0xdf,0x07,0x77,0xe7,0x4e,
0x1f,0x28,0x10,0x6c,0x59,0xd3,0xdd,0x2d,0x65,0x39,0xb2,0x74,0x84,0x3d,0xf4,0xbd,
0xc7,0x79,0x60,0x0b,0x4d,0x33,0x36,0x25,0xbc,0xe0,0x09,0xcf,0x5b,0xe2,0x38,0x9e,
0xc0,0xef,0xd2,0x16,0x05,0xbe,0x53,0xf7,0xc2,0xc6,0xa2,0x24,0x98,0x1c,0xad,0x04]

# diffusion array:
diffusion = [0xf26cb481,0x16a5dc92,0x3c5ba924,0x79b65248,0x2fc64b18,0x615acd29,0xc3b59a42,0x976b2584,
0x6cf281b4,0xa51692dc,0x5b3c24a9,0xb6794852,0xc62f184b,0x5a6129cd,0xb5c3429a,0x6b978425,
0xb481f26c,0xdc9216a5,0xa9243c5b,0x524879b6,0x4b182fc6,0xcd29615a,0x9a42c3b5,0x2584976b,
0x81b46cf2,0x92dca516,0x24a95b3c,0x4852b679,0x184bc62f,0x29cd5a61,0x429ab5c3,0x84256b97]

# Created in main - should result in the following:
"""inverse_diff = [4067210369, 379968658, 1012640036, 2041991752, 801524504, 1633340713, 3283458626, 2540381572,
1827832244, 2769720028, 1530668201, 3061401682, 3324975179, 1516317133, 3049472666, 1805091877,
3028415084, 3700561573, 2837724251, 1380481462, 1259876294, 3442041178, 2588066741, 629446507,
2176085234, 2463933718, 615078716, 1213380217, 407619119, 701323873, 1117435331, 2217044887]"""




def confuse_test(solution_result: bytearray, output: bytearray):
    """Computes confusion for given output and candidate array. Used in Used in backward_rounds_helper()."""
    for j in range(32):
        output[j] = conf1[solution_result[j]]
        solution_result[j] = 0


def diffuse_test(solution_result: bytearray, output: bytearray):
    """
    Computes diffusion XOR for given output and candidate array. 
    Used in Used in backward_rounds_helper().
    """
    for j in range(32):
        for k in range(32):
            solution_result[j] ^= output[k] * ((diffusion[j] >> k) & 1) # XOR=


def compress(solution_result: bytearray, output: bytearray):
    """Final XOR for cipher testing of proposed solution."""
    for i in range(16):
        output[i] = xor(conf1[solution_result[i*2]], conf2[solution_result[i*2+1]])
        

def inverse_diffuse(output: bytearray, candidate_arr: bytearray):
    """Undo diffusion for given output and candidate array. Used in backward_rounds_helper()."""
    for j in range(32):
        for k in range(32):
            # XOR and assign value to left value
            # return inverse_diff[j] with bits shifted to the right by k places.
            # Taken from main method.
            output[j] ^= candidate_arr[k] * ((inverse_diff[j] >> k) & 1)


def compute_inverse_conf1():
    """Returns the inverse of conf1 confusion table."""
    result = [[] for i in range(256)]
    for i in range(256):
        result[conf1[i]].append(i)

    return result


def generate_permutation(arr: List):
    """
    Given a list of 32 sublists, each containing 256 items.

    Generate a permutation: https://en.wikipedia.org/wiki/Permutation_box
    """
    # list of indicies
    idx = [0 for _ in range(len(arr))]
    # 32 item list of 255 -> [255, 255....]
    limit = [len(x)-1 for x in arr]

    terminate = False
    while not terminate:
        yield [arr[i][idx[i]] for i in range(len(arr))]
        terminate = True

        for i in range(len(arr)):
            if idx[i] < limit[i]:
                # if we found a value that can be changed
                idx[i] += 1
                for j in range(i):
                    idx[j] = 0
                terminate = False
                break


def backward_rounds_helper(output, candidate_arr, inverse_conf1, n):
    """
    Recursively attempts to undo the diffusion and then confusion modification. 

    Takes in:

    - output        -> an empty bytearray of 32
    - candidate_arr -> a bytearray that is our current candidate for use.
    - inverse_conf1 -> inverted version of confusion
    """
    if n == 0:
        return candidate_arr

    # Reverse diffusion
    inverse_diffuse(output, candidate_arr)

    # try to undo the confusion
    tmp = []
    prod = 1
    for j in range(32):
        tmp.append(inverse_conf1[output[j]])
        prod *= len(inverse_conf1[output[j]])

    if prod == 0:
        # In case of no result then move on - some items can't be calculated.
        return None

    # Generate permutations
    gen = generate_permutation(tmp)

    # Unpack generator
    # Recursively change the candidate to one generated by permutation
    for perm in gen:
        candidate_arr = bytearray(perm)
        output = bytearray(32)
        result = backward_rounds_helper(output, candidate_arr, inverse_conf1, n-1)
        if result is not None:
            return result


def generate_byte_conf_mapping():
    """
    Returns an array consisting of mapped byte -> corresponding confusion array byte in confusion array.

    Returns in the format of a list of 256 sublists, 
    each sublist containing many pairs in the form (byte, confusion array mapped).

    Note: a byte can have more than one potential match. E.g. 7 in the first iteration might match 33 and 209.
    This would look like [[....(7, 33), (7, 209)...], [...]]
    """
    # Generate an empty list of lists
    results = [[] for _ in range(256)]

    for k in range(256):
        for i in range(256):
            # tmp = confusion1 array value at [i] XOR k
            tmp = xor(conf1[i], k)

            try:
                # Return list of indicies of all occurences in confusion2 array 
                # where a specific position's value is equal to tmp
                indices = [idx for idx, x in enumerate(conf2) if x == tmp]

                # for each index position append it to a specific place in the result array
                for x in indices:
                    results[k].append((i, x))

            except ValueError:
                # otherwise, it's not in confusion2 array
                continue
    
    return results


def generate_candidates(output: bytearray):
    """
    Creates a generator yielding a list of candidate bytearrays for testing.

    1. Generates a mapping of byte -> confusion matrix vals.
    2. For each item in the output variable, 
        get the corresponding value when it is passed as a index to the generated mapping.
    3. Generate a permutation and thereafter a bytearray to return

    Ref: https://graphics.stanford.edu/~seander/bithacks.html
    """
    # Generate a mapping of byte -> confusion value(s)
    mappings = generate_byte_conf_mapping()
    # For each position in the output array passed in, return the corresponding item from our mappings list
    sub_map = [mappings[x] for x in output]
    # sub_map is 32 lists of 256 each

    # g is a generator, every time yielding a list of 32 items, each iterm in that being in the form of (val1, val2)
    gen = generate_permutation(sub_map)
    
    # Unpacking permutations
    for permutation in gen:
        results = []

        for x1, x2 in permutation:
            results.append(x1)
            results.append(x2)

        yield bytearray(results)



def solve(target: str):
    """
    Given a target string, produce a bytearray that, 
    when passed through the hireme_problem in place of the given input array, 
    will yield the target string.

    Presume input string of 15 chars long. Otherwise modify bytearray conversion below.
    """

    # Add trailing zeros to make output 32 byte long.
    output = bytearray(target + "\x00" * 17, "ascii")

    # Generate candidates:
    gen = generate_candidates(output)

    # result of compute_inverse_conf1 should be:
    """inverse_conf1 = [[106], [26], [24, 94], [89], [56], [86], [227], [195], [228], [95], [188], [144], [47], [223], [70], [], [88], [], [245], [42], [247], [191], [128], [10], [204], [221], [23], [246], [83, 113], [131], [129], [4], [], [130], [240], [145], [48], [2], [112], [158], [7], [253], [232], [9], [118], [132, 220], [222], [176], [81], [251], [200], [6, 154], [140], [115], [99], [210], [110], [68], [197], [216], [148], [218], [], [230], [161], [162], [37], [117], [], [248], [238], [100], [18], [77, 209], [43], [33], [125], [67], [146], [183], [189], [92], [82], [39], [149], [14], [104], [184, 207], [193], [75], [], [215], [59], [15], [123], [198], [252], [121], [22], [40], [91], [239], [41, 181], [214], [196], [80], [34], [], [62], [155], [51], [244], [233], [31], [32], [255], [119], [], [49], [127], [21, 151], [157], [174], [192], [8], [236], [226], [103], [], [60], [165], [30], [142], [45], [65], [250], [185], [153], [72], [205], [71], [137, 171], [96], [16], [186], [116], [61], [166, 224], [3], [134], [76], [93], [180], [213], [234], [87], [187], [122], [], [201], [69], [53], [58, 243], [172], [152], [50], [168], [150], [90], [133], [28], [101], [0], [97], [173], [], [13], [], [85], [5], [120], [219], [175], [208], [135], [242], 
    [66], [217], [11, 194], [178], [229], [126], [38], [44], [57], [136], [159], [164], [55, 64], [249], [235], [27], [105], [], [203], [170], [102], [46], [73], [1], [17], [20], [19], [], [143], [52], [111, 237], [231], [63], [139], [114], [167], [211], [163], [84], [141], [206], [107], [], [179], [78], [190], [35], [36, 124], [79], [202], [54], [108], [199], [169], [29], [109], [25], [182], [241], [212], [12], [98, 254], [138], [160], [], [156], [225], [177], [74], [147]]
    """
    inverse_conf1 = compute_inverse_conf1()

    count = 0
    for candidate in gen:
        print("Testing with candidate: {}".format(candidate))
        output_test = bytearray(32)

        result = backward_rounds_helper(output_test, candidate, inverse_conf1, 256)
        if result is None:
            continue

        print("Solution: {}".format(result)) # suppose to be a working solution

        # Convert to hex and dump it into a .txt file for use in hireme_problem.py
        hex_arr = [hex(i) for i in result]

        f = open("input_arr_solution.txt", "a")
        f.write(repr(hex_arr)+"\n") # Don't forget to remove ''
        f.close()
        #import binascii
        #print("Result: ", binascii.hexlify(result))

        # Verify the result, it should produce the target
        test_output = bytearray(32)
        #forward_rounds(result, test_output)
        for i in range(256):
            confuse_test(result, output)
            diffuse_test(result, output)

        compress(result, test_output)
        print("Solution output: {}".format(test_output))

        count += 1
        if count > 1:
            break



if __name__ == "__main__":
    start_time = time.time()

    # inverse diffuse array calc
    diff_matrix = list(map(lambda x: u32_to_bits_reverse(x), diffusion))
    inverse_diff_matrix = compute_inverse(diff_matrix)
    inverse_diff = list(map(lambda x: bits_to_u32_reverse(x), inverse_diff_matrix))

    # Invoke solver method using inverse_diff array
    solve("Hire me!!!!!!!!")
    #solve("Live Overflow!!!")
    print("--- Time taken: %s ---" % str(datetime.timedelta(seconds=time.time() - start_time)))