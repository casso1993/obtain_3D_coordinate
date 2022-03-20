# -*- coding: utf-8 -*-


import cv2
import numpy as np

kernel_size = (11, 11);
sigma = 3;
image = cv2.imread('./0.jpg')

# 图像转灰度图
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

img = cv2.GaussianBlur(img, kernel_size, sigma)
cv2.imshow("gauss", img)



# 图像转二值图
ret, thresh = cv2.threshold(img, 110
                            , 254, cv2.THRESH_TOZERO)
cv2.imshow("binary", thresh)
# 功能：cv2.findContours()函数来查找检测物体的轮廓。
#参数:
# 参数1：寻找轮廓的图像，接收的参数为二值图，即黑白的（不是灰度图），所以读取的图像要先转成灰度的，再转成二值图
# 参数2: 轮廓的检索模式，有四种。
#       cv2.RETR_EXTERNAL 表示只检测外轮廓;
#       cv2.RETR_LIST 检测的轮廓不建立等级关系;
#       cv2.RETR_CCOMP 建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
#       cv2.RETR_TREE 建立一个等级树结构的轮廓。
#
# 参数3: 轮廓的近似办法.
#       cv2.CHAIN_APPROX_NONE 存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1-x2），abs（y2-y1））==1
#       cv2.CHAIN_APPROX_SIMPLE 压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
#       cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS 使用teh-Chinl chain 近似算法
# 注：opencv2返回两个值：contours：hierarchy。opencv3会返回三个值,分别是img, countours, hierarchy
#
#返回值
#cv2.findContours()函数返回两个值，一个是轮廓本身，还有一个是每条轮廓对应的属性。
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    # 找到边界坐标
    x, y, w, h = cv2.boundingRect(c)  # 计算点集最外面的矩形边界
    #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 找面积最小的矩形
    rect = cv2.minAreaRect(c)
    # 得到最小矩形的坐标
    box = cv2.boxPoints(rect)
    # 标准化坐标到整数
    box = np.int0(box)
    # 画出边界
    cv2.drawContours(image, [box], 0, (0, 0, 255), 3)
    # # 计算最小封闭圆的中心和半径
    # (x, y), radius = cv2.minEnclosingCircle(c)
    # # 换成整数integer
    # center = (int(x), int(y))
    # radius = int(radius)
    # # 画圆
    # cv2.circle(image, center, radius, (0, 255, 0), 2)

cv2.drawContours(image, contours, -1, (255, 0, 0), 1)
cv2.imshow("img", image)
cv2.imwrite("img_1.jpg", image)
cv2.waitKey(0)
