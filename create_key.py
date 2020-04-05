from random import *
import string

key = "".join([choice(string.ascii_letters + string.digits) for i in range(64)])
# print(key)
key_file = open('./key.key', 'w')
key_file.writelines(key)
key_file.close()
