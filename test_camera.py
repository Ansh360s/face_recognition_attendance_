import cv2
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    if not ret:
        print("camera not working")
        break
    cv2.imshow("camera test",frame)
    if cv2.waitKey(1)==27:
        break
cap.release()
cv2.destroyAllWindows()