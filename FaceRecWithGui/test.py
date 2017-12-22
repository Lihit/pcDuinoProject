import cv2 

cap=cv2.VideoCapture(0)
r,f=cap.read()
while r:
    #f=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    cv2.imshow('myvideo',f)
    r,f=cap.read()
    if not r:
        break
    if cv2.waitKey(1) & 0xff=='q':
        break

cv2.destroyAllWindows()