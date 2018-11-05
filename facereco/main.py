from PIL import Image
import face_recognition

# Load the jpg file into a numpy array
image = face_recognition.load_image_file("test2.jpg")

xichtove_lokace = face_recognition.face_locations(image)

print("I found {} face(s) in this photograph.".format(len(xichtove_lokace)))

for xicht in xichtove_lokace:

    # Print the location of each face in this image
    # top, right, bottom, left = xicht
    top = xicht[0]
    right = xicht[1]
    bottom = xicht[2]
    left = xicht[3]

    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    # You can access the actual face itself like this:
    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.show()