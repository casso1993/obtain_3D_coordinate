import cv2
import os
if __name__ == '__main__':
    dir="/home/trust/PIC"
    filelist = os.listdir(dir)
    for file in filelist:
        fileName=os.path.join(dir,file)
        if ".BMP"  not in fileName:
            continue

        src=cv2.imread(fileName,0)
        pngName=fileName.replace(".BMP",".png")
        cv2.imwrite(pngName,src)
        