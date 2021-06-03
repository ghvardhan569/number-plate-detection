import cv2

# Opens the Video file
cap= cv2.VideoCapture(0)
vid_cod=cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter("Desktop/WWCD/video.mp4", vid_cod, 20.0, (640,480))
i=0
while(True):
     # Capture each frame of webcam video
     ret,frame = cap.read()
     if ret == False:
        break
     cv2.imshow("My cam video", frame)
     output.write(frame)
     cv2.imwrite('pics/no_plate'+str(i)+'.jpg',frame)
     i+=1
     # Close and break the loop after pressing "x" key
     if cv2.waitKey(1000) &0XFF == ord('q'):
         break

     elif i>10:
         break
    # close the already opened camera
cap.release()
# close the already opened file
output.release()
# close the window and de-allocate any associated memory usage
cv2.destroyAllWindows()
