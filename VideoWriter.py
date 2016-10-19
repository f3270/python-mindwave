#coding: latin-1
import cv2


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

w = cap.get(cv2.CAP_PROP_FRAME_WIDTH);
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT);
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
out = cv2.VideoWriter('./data/output.avi',fourcc, 15.0, (int(w),int(h)))

while (True):
    ret, frame = cap.read()

    out.write(frame)
    cv2.imshow('Video Stream', frame)

    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
