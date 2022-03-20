import cv2
import os

curDir = os.curdir  # 获取当前执行python文件的文件夹
sourceDir = os.path.join(curDir, 'picture')
resultDir = os.path.join(curDir, 'resolution_lower')


def resolution_lower_handler(sourceDir, resultDir):
    img_list = os.listdir(sourceDir)
    category = input("category:")
    for file in img_list:
        name = file.split(".")[0]
        os.rename(os.path.join(sourceDir, file), os.path.join(resultDir, '{}_{}.{}'.format(category, name, "jpg")))

    img_list2 = os.listdir(resultDir)
    for i in img_list2:
        pic = cv2.imread(os.path.join(resultDir, i), cv2.IMREAD_COLOR)
        pic_n = cv2.resize(pic, (1280, 720))
        pic_name = i
        cv2.imwrite(os.path.join(resultDir, i), pic_n)


if __name__ == '__main__':
    resolution_lower_handler(sourceDir, resultDir)