import glob
import pandas as pd
import numpy as np
import cv2
import  imutils
import csv
import sys
import pytesseract
#pytesseract.pytesseract.tesseract_cmd=r'C:\Tesseract-OCR\tesseract.exe'
import time

key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
'''while True:
    try:
        check, frame = webcam.read()
        #print(check) #prints true as long as the webcam is running
        #print(frame) #prints matrix values of each framecd 
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'): 
            cv2.imwrite(filename='no_plate.jpg', img=frame)
            webcam.release()
            cv2.waitKey(1650)
            cv2.destroyAllWindows()
            print("Processing image...")
            img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
            print("Image saved!")
        
            break
        elif key == ord('q'):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
        
    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break'''

image = cv2.imread('no_plate.jpg')

image = imutils.resize(image, width=500)

#cv2.imshow("Original Image", image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("1 - Grayscale Conversion", gray)

gray = cv2.bilateralFilter(gray, 11, 17, 17)
#cv2.imshow("2 - Bilateral Filter", gray)

edged = cv2.Canny(gray, 170, 200)
#cv2.imshow("4 - Canny Edges", edged)

cnts, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30] 
NumberPlateCnt = None 

count = 0
for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:  
            NumberPlateCnt = approx 
            break

# Masking the part other than the number plate
mask = np.zeros(gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[NumberPlateCnt],0,255,-1)
new_image = cv2.bitwise_and(image,image,mask=mask)
#cv2.namedWindow("Final_image",cv2.WINDOW_NORMAL)
#cv2.imshow("Final_image",new_image)

# Configuration for tesseract
#config = ('-l eng --oem 1 --psm 3')

# Run tesseract OCR on image
pytesseract.pytesseract.tesseract_cmd=r'C:\Tesseract-OCR\tesseract.exe'
text = str(pytesseract.image_to_string(new_image))
print(text)
count=0

with open("miss_table.csv","r") as f:
    csvreader = csv.reader(f, delimiter=",")
    for row in csvreader:
        if text in row[2]:
            p=row[2].index(text)
            print("Your Car is Spotted")
            count=1
            raw_data = {'date': [time.asctime( time.localtime(time.time()) )], 'v_number': [text]}
            import os
            os.system('python clientalert.py')
            break

print(text)
#Data is stored in CSV file
if count == 0:
    raw_data = {'date': [time.asctime( time.localtime(time.time()) )], 'v_number': [text]}

df = pd.DataFrame(raw_data, columns = ['date', 'v_number'])
df.to_csv('data.csv')

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ],sort=False)
#export to csv
combined_csv.to_csv( "data1.csv", index=False)

# Print recognized text
print(text)

cv2.waitKey(0)
