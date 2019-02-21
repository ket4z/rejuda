from PIL import ImageDraw
import PIL.Image
import PIL.ImageTk
import face_recognition
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from os import path
from screeninfo import get_monitors
import re

for m in get_monitors():
    print(str(m))
    ints = re.findall(r'\d+', str(m))
    x = ints[0]
    print(x)

resizeTargetSize = (int(x) - 200) / 2
print(str(resizeTargetSize))

root = Tk()
root.title("Face recognition")
root.attributes('-zoomed', True)


home = path.expanduser('~')

class MainWindow:

    def __init__(self, master):

        # Setting image... to a default image
        self.imageBeforeG = PIL.Image.open("default-image.jpg")
        self.imageAfterG = PIL.Image.open("default-image.jpg")

        # Resizing image... to defined resolution
        self.imageBeforeG = self.resizeImage(self.imageBeforeG)
        self.imageAfterG = self.resizeImage(self.imageAfterG)

        # Saving image... to ImageTk.PhotoImage / for being able to show on label
        self.imageBeforeG = PIL.ImageTk.PhotoImage(self.imageBeforeG)
        self.imageAfterG = PIL.ImageTk.PhotoImage(self.imageAfterG)

        # Saving image... to ImageTk.PhotoImage / for being able to show on label
        self.imageBefore = self.imageBeforeG
        self.imageAfter = self.imageAfterG

        self.lblHeader = Label(master, text="Recognize face(s) from your own photo!")
        self.lblHeader.config(font=("", 30))
        self.lblHeader.pack()

        frame = Frame(master)
        frame.pack()

        self.btnFindFile = Button(frame, text="Find file", command=self.findFile)
        # self.btnFindFile.pack()
        self.btnFindFile.grid(row=0, column=0)

        self.btnSaveFile = Button(frame, text="Save file", command=self.saveFile)
        self.btnSaveFile.grid(row=0, column=2)

        self.imgBeforePI = Label(frame, image=self.imageBefore)
        self.imgBeforePI.grid(row=1, column=0)

        self.btnRecognize = Button(frame, text='Find faces', command=self.findFaces)
        self.btnRecognize.grid(row=1, column=1)

        self.imgAfterPI = Label(frame, image=self.imageAfter)
        self.imgAfterPI.grid(row=1, column=2)

        self.lblAkce = Label(master, text="Nahraj obrazek")
        self.lblAkce.pack()

    def findFile(self):
        try:
            root.filename = filedialog.askopenfilename(initialdir=home, title="Select file", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
            # root.filename = "koule.jpg"
            print("working on file > " + root.filename)

            imageToResize = PIL.Image.open(root.filename)
            image = self.resizeImage(imageToResize)

            self.imageBefore = PIL.ImageTk.PhotoImage(image)
            self.imgBeforePI.configure(image=self.imageBefore)
            self.imgBeforePI.image = self.imageBefore

            self.imgAfterPI.configure(image=self.imageAfterG)
            self.imgAfterPI.image = self.imageAfterG

            root.update()
        except:
           self.ffError()

    def resizeImage(self, image):
        try:
            imageSize = image.size
            if imageSize[1] > imageSize[0]:
                print(imageSize)
                w1 = imageSize[0]
                h1 = imageSize[1]
                w2 = w1 - 400  # desired image width after resizing
                h2 = w2 * h1 / w1
                print(str(w2))
                return image.resize((int(w2), int(h2)))
            else:
                imageSize = image.size
                print(imageSize)
                w1 = imageSize[0]
                h1 = imageSize[1]
                w2 = 900  # desired image width after resizing
                h2 = w2 * h1 / w1
                return image.resize((w2, int(h2)))
        except:
            messagebox.showerror("Chyba!", "Nepovedlo se zmenit velikost obrazku")

    def findFaces(self):
        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(root.filename)

        xichtove_lokace = face_recognition.face_locations(image)

        if len(xichtove_lokace) == 0:
            messagebox.showerror('Error!', "Didn't find any face(s) on selected photo!")
        else:
            print("I found {} face(s) in this photograph.".format(len(xichtove_lokace)))

            # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
            # See http://pillow.readthedocs.io/ for more about PIL/Pillow
            pil_image = PIL.Image.fromarray(image)
            # Create a Pillow ImageDraw Draw instance to draw with
            draw = ImageDraw.Draw(pil_image)

            counter = 0

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

                # cerveny boxik s tloustkou 3px
                draw.rectangle(((left, top), (right, bottom)), outline=(255, 0, 0), width=3)
                # jmenovka
                draw.rectangle(((left, bottom), (right, bottom + 20)), outline=(255, 0, 0), fill=255)

                counter = counter + 1
                draw.text(((left + 5, bottom + 5)), text=str(counter), fill=(255, 255, 255))

                # cerveny kruh
                # draw.ellipse(((left, top), (right, bottom)), None, outline=(255, 0, 0))

            # free the drawing library from memory
            del draw

            # display the resulting image

            # lets resize it first
            resizedImage = self.resizeImage(pil_image)

            self.imageAfter = PIL.ImageTk.PhotoImage(resizedImage)
            self.imageToSave = pil_image
            self.imgAfterPI.configure(image=self.imageAfter)
            self.imgAfterPI.image = self.imageAfter

            self.lblAkce.configure(text="Fotografie uspesne konvertovana, muzes vysledek ulozit")

            root.update()

    def saveFile(self):
        try:
            # save a copy of the new image to disk?
            self.filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=(("JPEG file", "*.jpg"),("All Files", "*.*") ))
            # print("saving on file > " + root.filename)

            self.imageToSave.save(self.filename)
            self.lblAkce.configure(text="Fotografie byla ulozena do " + str(self.filename.name) + "   > muzes otevrit kliknutim!")
            self.lblAkce.bind("<Button-1>", self.openFile)

            # system("open " + filename.name)
        except:
            messagebox.showwarning('Warning!', "Photo hasn't been saved!")

    def openFile(self, event):
        #print("you clicked", event.widget)
        savedImage = PIL.Image.open(self.filename.name)
        savedImage.show()

    def ffError(self):
        messagebox.showwarning('Warning!', 'You need to chose an image!')


mw = MainWindow(root)
root.mainloop()


# TODO: resize also output image using resizeImage() method
