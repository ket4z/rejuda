import string
import random

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


for x in range(100):
	S = id_generator(5)
	print(str(x) + '. ' + S)

S = id_generator(5)
print(S)