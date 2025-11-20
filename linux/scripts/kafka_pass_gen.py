#!/bin/python3

import base64
import random
import string


def get_alphabet_digits_list():
 
    # alphabet_digits_list = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation)
    # alphabet_digits_list.remove('"')
    # alphabet_digits_list.remove('\\')
    # alphabet_digits_list.remove('}')
    # alphabet_digits_list.remove('{')
    # alphabet_digits_list.remove('\'')
    # alphabet_digits_list.remove('`')


# print(alphabet_digits_list)


    airflow_digits = "#!-_.:/()"

    return list(string.ascii_lowercase + string.ascii_uppercase + string.digits + airflow_digits)

alphabet_digits_list = get_alphabet_digits_list()

def generate_pass():
    chars = []
    for i in range(32):
        chars.append(random.choice(alphabet_digits_list))
    password = "".join(chars)
    if check_pass(password):
        return password
    else:
        return 0

def check_pass(password):
    lowercase_flag = False
    uppercase_flag = False
    digits_flag = False
    punct_flag = False
    for i in password:
        if not lowercase_flag and i in string.ascii_lowercase:
            lowercase_flag = True
            print("lowercase:", i)
        elif not uppercase_flag and i in string.ascii_uppercase:
            uppercase_flag = True
            print("uppercase:", i)
        elif not digits_flag and i in string.digits:
            digits_flag = True
            print("digit:", i)
        elif not punct_flag and i in string.punctuation:
            punct_flag = True
            print("punct:", i)

    return lowercase_flag and uppercase_flag and digits_flag and punct_flag

password = generate_pass()
print(password)
salt = base64.b64encode(bytes(password.encode('utf-8')))
print(salt.decode())