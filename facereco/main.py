from PIL import ImageDraw
import PIL.Image
import face_recognition
from tkinter import filedialog
from tkinter import *
from os import path

root = Tk()
root.title("Face recognition")
root.geometry("300x150")
home = path.expanduser('~')
imageBefore = PhotoImage(file="default-image.jpg")
imageAfter = PhotoImage(file="default-image.jpg")


class MainWindow:

    def __init__(self, master):

        self.imageBefore = imageBefore
        self.imageAfter = imageAfter

        frame = Frame(master)
        frame.pack()

        self.lblHeader = Label(frame, text="Recognize face(s) from your own photo!")
        self.lblHeader.pack()

        self.btnFindFile = Button(frame, text="Find file", command=self.findFile)
        self.btnFindFile.pack()

        self.btnFindFile = Button(frame, text="Save file", command=self.saveFile)
        self.btnFindFile.pack()

        self.imgBefore = Label(frame, image=self.imageBefore)
        self.imgBefore.pack()

        self.imgAfter = Label(frame, image=self.imageAfter)
        self.imgAfter.pack()

    def findFile(self):
        root.filename = filedialog.askopenfilename(
            initialdir=home,
            title="Select file",
            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        print("working on file > " + root.filename)

        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(root.filename)
        # image = face_recognition.load_image_file("test2.jpg")
        # image = face_recognition.load_image_file("koule.jpg")

        xichtove_lokace = face_recognition.face_locations(image)

        print("I found {} face(s) in this photograph.".format(len(xichtove_lokace)))

        # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
        # See http://pillow.readthedocs.io/ for more about PIL/Pillow
        pil_image = PIL.Image.fromarray(image)
        # Create a Pillow ImageDraw Draw instance to draw with
        draw = ImageDraw.Draw(pil_image)

        for xicht in xichtove_lokace:
            # Print the location of each face in this image
            # top, right, bottom, left = xicht
            top = xicht[0]
            right = xicht[1]
            bottom = xicht[2]
            left = xicht[3]

            print(
                "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                      right))

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
        self.imageAfter = pil_image
        self.imageBefore = image
        root.update()

    def saveFile(self):
        # save a copy of the new image to disk?
        root.filename = filedialog.asksaveasfilename(
            initialdir=home,
            title="Select file",
            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        print("saving on file > " + root.filename)

        self.imageAfter.save(root.filename)


mw = MainWindow(root)
root.mainloop()
