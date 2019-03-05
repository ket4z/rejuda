import face_recognition
import cv2
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def select_faces_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT ID, name, image FROM faces WHERE image <> ''")
    rows = cursor.fetchall()
    for row in rows:
        print("%d - %s" % (row[0], row[1]))
    return rows

def add_face_to_db(connection, user_id, user_name, user_image):
    cursor = connection.cursor()
    SQL = "INSERT INTO faces (ID, name, image) VALUES (%d, '%s', null)" % (user_id, user_name)
    # print(SQL)
    cursor.execute(SQL)
    connection.commit()


# mina flow BEGIN #####################################

db_connection = create_connection("facereco.db")
print(db_connection)
# add_face_to_db(db_connection, 6, "Kuba", "")
db_faces = select_faces_from_db(db_connection)

# reference to webcam #0 (default)
# docasne vypinam, pro az
# video_capture = cv2.VideoCapture(0)

for db_face in db_faces:
    # TODO: preulozit data z db pole "image" do docasneho fyzickeho souboru
    # TODO: natahnout fotku z tohoto docasneho souboru, nikoli z tomas.jpg
    image_from_db = face_recognition.load_image_file("tomas.jpg")
    face_encoding = face_recognition.face_encodings(image_from_db)[0]
    # TODO: smazat docasny soubor
    # TODO: pridat nakodovany oblicej (face_encoding) do face encodings
    # TODO: pridat jmeno z db do known names

# # Load a sample picture and learn how to recognize it.
# julo_image = face_recognition.load_image_file("julo.jpg")
# julo_face_encoding = face_recognition.face_encodings(julo_image)[0]
#
# # Load a second sample picture and learn how to recognize it.
# tomas_image = face_recognition.load_image_file("tomas.jpg")
# tomas_face_encoding = face_recognition.face_encodings(tomas_image)[0]
#
# marek_image = face_recognition.load_image_file("marek.jpg")
# marek_face_encoding = face_recognition.face_encodings(marek_image)[0]
#
# marian_image = face_recognition.load_image_file("marian.jpg")
# marian_face_encoding = face_recognition.face_encodings(marian_image)[0]
#
# # Create arrays of known face encodings and their names
# known_face_encodings = [
#     tomas_face_encoding,
#     marian_face_encoding,
#     marek_face_encoding,
#     julo_face_encoding
# ]
#
# known_face_names = [
#     "Tomas",
#     "Marian",
#     "Marek",
#     "Julo"
# ]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# docasny exit jeste pred analyzou webcam streamu, pro ucely ladeni kodovani obliceju z DB, pro produkci oedstranit
exit(101)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
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

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
