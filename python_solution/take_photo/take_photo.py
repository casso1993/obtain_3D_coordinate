import cv2

cap = cv2.VideoCapture(6)
cap.set(3, 1280)
cap.set(4, 720)
i = 0
while (1):
    ret, frame = cap.read()
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('/home/casso/photo1/total/' + str(i) + '.jpg', frame)
        i += 1
    cv2.imshow("capture", frame)
cap.release()
cv2.destroyAllWindows()

