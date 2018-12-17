from PIL import ImageDraw
import PIL.Image
import PIL.ImageTk
import face_recognition
from tkinter import filedialog
from tkinter import *
from os import path

root = Tk()
root.title("Face recognition")
root.geometry("1200x800")
home = path.expanduser('~')

imageBeforeG = PIL.ImageTk.PhotoImage(file="default-image.jpg")
imageAfterG = PIL.ImageTk.PhotoImage(file="default-image.jpg")

class MainWindow:

    def __init__(self, master):

        self.imageBefore = imageBeforeG
        self.imageAfter = imageAfterG

        self.lblHeader = Label(master, text="Recognize face(s) from your own photo!")
        self.lblHeader.pack()

        frame = Frame(master)
        frame.pack()

        self.btnFindFile = Button(frame, text="Find file", command=self.findFile)
        # self.btnFindFile.pack()
        self.btnFindFile.grid(row=0, column=0)

        self.btnFindFile = Button(frame, text="Save file", command=self.saveFile)
        self.btnFindFile.grid(row=0, column=1)

        self.imgBeforePI = Label(frame, image=self.imageBefore)
        self.imgBeforePI.grid(row=1, column=0)

        self.imgAfterPI = Label(frame, image=self.imageAfter)
        self.imgAfterPI.grid(row=1, column=1)

    def findFile(self):
        # root.filename = filedialog.askopenfilename(initialdir=home, title="Select file", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        root.filename = "koule.jpg"
        print("working on file > " + root.filename)
        self.imageBefore = PIL.ImageTk.PhotoImage(file=root.filename)
        self.imgBeforePI.configure(image=self.imageBefore)
        self.imgBeforePI.image = self.imageBefore
        root.update()

        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(root.filename)

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
        self.imageAfter = PIL.ImageTk.PhotoImage(pil_image)
        self.imageToSave = pil_image
        self.imgAfterPI.configure(image=self.imageAfter)
        self.imgAfterPI.image = self.imageAfter
        root.update()

    def saveFile(self):
        # save a copy of the new image to disk?
        root.filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=(("JPEG file", "*.jpg"),("All Files", "*.*") ))
        # print("saving on file > " + root.filename)

        self.imageToSave.save(root.filename)


mw = MainWindow(root)
root.mainloop()
