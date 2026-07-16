import face_recognition
img=face_recognition.load_image_file("images/anshul_25/0.jpg")

encodings=face_recognition.face_encodings(img)
print(encodings)