import random
from math import floor
from math import sqrt

RANDOM_START = 32768
RANDOM_END = 65535


def is_prime(num):

    # primes have to be bigger than 2
    if num < 2:
        return False

    # consider the only even prime number
    if num == 2:
        return True

    # even number can not be primes
    if num % 2 == 0:
        return False

    # check other odd number
    for i in range(3, floor(sqrt(num))):
        if num % i == 0:
            return False

    return True

# whether (e,phi) are coprime, with the gcd(e,phi)=1 condition


def gcd(a, b):

    # get remainder each loop until b is 0, then a is the final gcd
    while b != 0:
        a, b = b, a % b

    return a

# Extended Euclidean algorithm to find the modular inverse, a < b


def modular_inverse(a, b):

    # when a = 0, then gcd(0,b) = b and a*x+b*y=b, so x =0 y=1
    if a == 0:
        return b, 0, 1

    #div is gcd
    div, x1, y1 = modular_inverse(b % a, a)

    # update the parameters for x,y accordingly. x is current remainder and y is the previous remainder
    x = y1-(b//a)*x1
    y = x1

    # use recursion to get the final result, final x is the inverse of a
    return div, x, y


def generate_large_prime(start=RANDOM_START, end=RANDOM_END):
    # generate a random number [RANDOM_START,RANDOM_END]
    num = random.randint(start, end)

    # check the number whethter it is a prime or not. If it is not a prime then regenerate the new number
    while not is_prime(num):
        num = random.randint(start, end)

    # number is prime
    return num


def generate_rsa_keys():

    # generate the first random prime
    p = generate_large_prime()
    q = generate_large_prime()
    print('p is:', p, 'q is:', q)
    print('p is prime:', is_prime(p))
    print('q is prime:', is_prime(q))

    # get n
    n = p*q
    print('N is:', n)

    # get phi(n)
    phi = (p-1)*(q-1)
    print('phi(N) is:', phi)

    # get public key number e
    e = random.randrange(1, phi)

    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    print("e is:", e)

    # get private key number d
    d = modular_inverse(e, phi)[1]

    if d < 0:
        d = d+phi
    print('d is:', d)

    # public key and private key
    return (e, n), (d, n)

# square and multiply


def divide_exponent_number(exponent):
    binary_exponet = list(reversed(bin(exponent)[2:]))
    i = 0
    divided_exponent_number_list = []
    for binary_num in binary_exponet:
        divided_exponent_number_list.append(2**i*int(binary_num))
        i += 1
    return divided_exponent_number_list


def square_and_multiply(num, exponent, modulus):

    square_and_multiply_dict = {}
    square_and_multiply_result = 1
    divided_exponent_number_list = divide_exponent_number(exponent)

    # get square and multiply result with modulus
    for i in range(len(bin(max(divide_exponent_number(exponent))))-2):
        square_and_multiply_dict.update({2**i: num})
        if (2**i) in divided_exponent_number_list:
            square_and_multiply_result *= num
        num = pow(num, 2, modulus)
    return square_and_multiply_result % modulus


def divide_message_to_3_bytes_chunks(text_string):
    split_strings = []

    # divide every 3 characters
    n = 3
    for index in range(0, len(text_string), n):
        split_strings.append(text_string[index: index + n])

    # print(split_strings)
    return split_strings

# convert each 3-byte chunks to hex format


def hex_format(chunk):

    hex_chunk = ''
    i = 0
    for c in chunk:
        if i == 0:
            hex_chunk += hex(ord(c))
        else:
            hex_chunk += hex(ord(c))[2:]
        i += 1
    return hex_chunk


# convert the entile chunks list to hex format as "0x"
def chunks_to_hex_string(split_strings_list):
    hex_string = [hex_format(c) for c in split_strings_list]
    print('MY_MESSAGE_HEXADECIMAL_STRING =', hex_string)
    return hex_string

# convert hex list to int list


def hex_string_to_int(hex_string):
    int_list = [int(c, 16) for c in chunks_to_hex_string(hex_string)]
    print('MY_MESSAGE_INT =', int_list)
    return int_list


def encrypt_and_sign(public_key, plain_text):
    e, n = public_key
    cipher_text = []
    bytes_chunks = divide_message_to_3_bytes_chunks(plain_text)
    print('MY_MESSAGE_chunks =', bytes_chunks)
    int_text = hex_string_to_int(bytes_chunks)
    for num in int_text:
        cipher_text.append(square_and_multiply(num, e, n))
    return cipher_text


def int_to_hex_string(int_list):
    hex_string_list = []
    for int_number in int_list:
        hex_string_list.append(hex(int_number))
    print('PARTNER_MESSAGE_HEXADECIMAL_STRING =', hex_string_list)
    return hex_string_list


def bytes_chunks_format(hex_string):
    a = '0x'
    b = ''
    list1 = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    for char in list1[1:]:
        b += chr(int(a+char, 16))
    return b


def hex_string_to_3_bytes_chunks(hex_string_list):
    hex_list = int_to_hex_string(hex_string_list)
    chunks_list = []
    for hex_string in hex_list:
        chunks_list.append(bytes_chunks_format(hex_string))
    return chunks_list


def decrypt_and_verify(private_key, cipher_text):
    d, n = private_key
    plain_text_chunks = []
    plain_text = ''
    for num in cipher_text:
        plain_text_chunks.append(square_and_multiply(num, d, n))
    plain_text_chunks = hex_string_to_3_bytes_chunks(plain_text_chunks)
    print('PARTNER_MESSAGE_chunks_AFTER_DECRYPT =', plain_text_chunks)
    for each_plain_text_chunk in plain_text_chunks:
        plain_text += each_plain_text_chunk
    return plain_text


def is_valid_signature(orginal_message, verified_message):
    if orginal_message == verified_message:
        return True
    else:
        return False


# My own public and private kay
# 61051 58831
# (960622037, 3591691381)
# (4674473,3591691381)
if __name__ == '__main__':
    # public_key, private_key = generate_rsa_keys()

    # public key from my partner
    public_key = (2575666295, 3393650443)

    # My own private key
    private_key = (4674473, 3591691381)

    # encrypt
    message_for_encryption = 'Group T Feiyu Duan 40160978 RSA'
    print('MY_MESSAGE =', message_for_encryption)
    cipher = encrypt_and_sign(public_key, message_for_encryption)
    print('MY_CIPHERTEXT=', cipher)
    print()

    # decrypt
    # cipher from my partner
    cipher = [726112781, 2425347659, 1750696870,
              2382748590, 492553636, 2154438234]
    print('PARTNER_CIPHERTEXT =', cipher)
    plaintext = decrypt_and_verify(private_key, cipher)
    print('PARTNER_MESSAGE_AFTER_DECRYPT =', plaintext)
    print()

    # sign
    message_for_signature = 'Feiyu Duan'
    print('MY_MESSAGE_TO_BE_SIGNED =', message_for_signature)
    signed_message = encrypt_and_sign(private_key, message_for_signature)
    print('MY_SIGNATURE =', signed_message)
    print()

    # verify
    # signed_message from my partner
    signed_message = 'Jasmeen Kaur'
    print('PARTNER_SIGNED_MESSAGE =', signed_message)
    signed_signature = [1657739693, 2952198091, 1859795175, 1811084381]
    print('PARTNER_SIGNATURE =', signed_signature)
    verified_message = decrypt_and_verify(public_key, signed_signature)
    print('PARTNER_SIGNATURE_AFTER_VERIFY =', verified_message)
    print("valid signature:",
          is_valid_signature(signed_message, verified_message))
