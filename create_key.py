from random import *

key = "".join([choice("0123456789ABCDEF") for i in range(64)])
key_file = open('./key.key', 'w')
key_file.writelines(key)
key_file.close()
