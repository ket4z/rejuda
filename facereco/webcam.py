import os
import face_recognition
import cv2
import sqlite3
from sqlite3 import Error
from PIL import Image
import easygui

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def select_faces_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT ID, name, image FROM faces2 WHERE image <> ''")
    rows = cursor.fetchall()
    for row in rows:
        print("%d - %s" % (row[0], row[1]))
    return rows

def add_face_to_db(connection, user_name, user_image):
    # print(user_image)
    print("adding user %s to db" % user_name)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO faces2 (name, image) VALUES (?, ?)", (user_name, user_image))
    connection.commit()


# main flow BEGIN #####################################

db_connection = create_connection("facereco.db")
print(db_connection)
# add_face_to_db(db_connection, 6, "Kuba", "")
db_faces = select_faces_from_db(db_connection)

# reference to webcam #0 (default)
# docasne vypinam, pro az
video_capture = cv2.VideoCapture(0)

known_face_encodings = []
known_face_names = []

for db_face in db_faces:
    # debug
    if db_face[0] > 1:
        continue

    print("working on %s, storing image from db to temp disk file" % db_face[1])

    # temporary storage of db image to disk file tempfile.jpg
    with open("tempfile.jpg", "wb") as f_temp:
        f_temp.write(db_face[2])

    # load this temp image to face reco
    print("loading image from disk to face reco engine")
    image_from_db = face_recognition.load_image_file("tempfile.jpg")
    print("encoding face")
    try:
        face_encoding = face_recognition.face_encodings(image_from_db)[0]

        # add encoded face to array of faces (face_encoding)
        known_face_encodings.append(face_encoding)

        # add name to known names
        known_face_names.append(db_face[1])
    except:
        print("could not find any face on provided image")

    # delete temp file
    print("deleting temp file")
    os.remove("tempfile.jpg")

    print("----------")

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # copy untampered frame
    frame_copy = frame.copy()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    # TODO: process every N-th frame instead of every other, set 3, 4, etc for N ...
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Neznam"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # TODO: prepare saving unrecognized faces to DB on click or keypress, ask for name under which this face should be stored

    # hit 'q' on the keyboard to quit
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    # hit 's' on the keyboard to save new face
    elif key == ord('s'):
        if name == 'Neznam':
            print("I don't know thsis face, going to save it")
            print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
            face_image = frame_copy[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.show()
            newName = easygui.enterbox("Enter new person's name")
            if newName is not None:
                pil_image.save("tempNewFace.jpg")
                with open("tempNewFace.jpg", "rb") as f_tempNewFace:
                    newFaceData = f_tempNewFace.read()
                add_face_to_db(db_connection, newName, newFaceData)
            # TODO: rovnou se ten oblicej nauc
            image_from_db = face_recognition.load_image_file("tempNewFace.jpg")
            face_encoding = face_recognition.face_encodings(image_from_db)[0]
            # add encoded face to array of faces (face_encoding)
            known_face_encodings.append(face_encoding)
            # add name to known names
            known_face_names.append(newName)

        else:
            print("I already know this face, it is %s" % name)

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
