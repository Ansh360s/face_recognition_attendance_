import face_recognition
img=face_recognition.load_image_file("images adress")

encodings=face_recognition.face_encodings(img)
print(encodings)