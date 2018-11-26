from PIL import Image, ImageDraw
import face_recognition

# Load the jpg file into a numpy array
image = face_recognition.load_image_file("test2.jpg")
# image = face_recognition.load_image_file("koule.jpg")

xichtove_lokace = face_recognition.face_locations(image)

print("I found {} face(s) in this photograph.".format(len(xichtove_lokace)))

# Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
# See http://pillow.readthedocs.io/ for more about PIL/Pillow
pil_image = Image.fromarray(image)
# Create a Pillow ImageDraw Draw instance to draw with
draw = ImageDraw.Draw(pil_image)

for xicht in xichtove_lokace:

    # Print the location of each face in this image
    # top, right, bottom, left = xicht
    top = xicht[0]
    right = xicht[1]
    bottom = xicht[2]
    left = xicht[3]

    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    # You can access the actual face itself like this:
    # face_image = image[top:bottom, left:right]
    # pil_image = Image.fromarray(face_image)
    # pil_image.show()

    # modry boxik
    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
    # cerveny kruh
    draw.ellipse(((left, top), (right, bottom)), None, outline=(255, 0, 0))

# free the drawing library from memory
del draw

# display the resulting image
pil_image.show()

# save a copy of the new image to disk?
# pil_image.save("image_with_boxes_and_circles.jpg")
