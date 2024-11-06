#!/bin/python3

import base64
import random
import string
alphabet_digits_list = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation)
# print(alphabet_digits_list)
chars = []
for i in range(32):
    chars.append(random.choice(alphabet_digits_list))
password = "".join(chars)
print(password)
salt = base64.b64encode(bytes(password.encode('utf-8')))
print(salt.decode())