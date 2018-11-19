from PIL import Image, ImageDraw
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


# for x in range(100):
# 	S = id_generator(5)
# 	print(str(x) + '. ' + S)

S = id_generator(5)
print(S)

img = Image.new('RGB', (100, 30), color=(73, 109, 137))

d = ImageDraw.Draw(img)
d.text((10, 10), S, fill=(255, 255, 0))

img.save('pil_text.png')