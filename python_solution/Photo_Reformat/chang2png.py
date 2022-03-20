import os
import cv2
import sys
import numpy as np

path1 = "./picture/"
path2 = "./resolution_lower/"
print(path1)

for filename in os.listdir(path1):
    if os.path.splitext(filename)[1] == '.jpg':
        # print(filename)
        img = cv2.imread(path1 + filename)
        print(filename.replace(".jpg", ".png"))
        newfilename = filename.replace(".jpg", ".png")
        # cv2.imshow("Image",img)
        # cv2.waitKey(0)
        cv2.imwrite(path2 + newfilename, img)