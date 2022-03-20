# *_* coding : UTF-8 *_*
# 开发人员   ：csu·pan-_-||
# 开发时间   ：2020/10/13 20:18
# 文件名称   ：roxml_to_dota.py
# 开发工具   ：PyCharm
# 功能描述   ：把rolabelimg标注的xml文件转换成dota能识别的xml文件
#             就是把旋转框 cx,cy,w,h,angle，转换成四点坐标x1,y1,x2,y2,x3,y3,x4,y4
# 修改：小鸡炖技术

import os
import xml.etree.ElementTree as ET
import math
import cv2
import numpy as np


def edit_xml(xml_file):

    if ".xml" not  in xml_file:
        return 
        
    tree = ET.parse(xml_file)
    objs = tree.findall('object')

    txt=xml_file.replace(".xml",".txt")

    png=xml_file.replace(".xml",".jpg")
    src=cv2.imread(png,1)

    with open(txt,'w') as wf:
        wf.write("imagesource:GoogleEarth\n")
        wf.write("gsd:0.115726939386\n")

        for ix, obj in enumerate(objs):

            x0text = ""
            y0text =""
            x1text = ""
            y1text =""
            x2text = ""
            y2text = ""
            x3text = ""
            y3text = ""
            difficulttext=""
            className=""

            obj_type = obj.find('type')
            type = obj_type.text

            obj_name = obj.find('name')
            className = obj_name.text

            obj_difficult= obj.find('difficult')
            difficulttext = obj_difficult.text

            if type == 'bndbox':
                obj_bnd = obj.find('bndbox')
                obj_xmin = obj_bnd.find('xmin')
                obj_ymin = obj_bnd.find('ymin')
                obj_xmax = obj_bnd.find('xmax')
                obj_ymax = obj_bnd.find('ymax')
                xmin = float(obj_xmin.text)
                ymin = float(obj_ymin.text)
                xmax = float(obj_xmax.text)
                ymax = float(obj_ymax.text)

                x0text = str(xmin)
                y0text = str(ymin)
                x1text = str(xmax)
                y1text = str(ymin)
                x2text = str(xmin)
                y2text = str(ymax)
                x3text = str(xmax)
                y3text = str(ymax)

                points=np.array([[int(x0text),int(y0text)],[int(x1text),int(y1text)],[int(x2text),int(y2text)],[int(x3text),int(y3text)]],np.int32)
                cv2.polylines(src,[points],True,(255,0,0)) #画任意多边

            elif type == 'robndbox':
                obj_bnd = obj.find('robndbox')
                obj_bnd.tag = 'bndbox'   # 修改节点名
                obj_cx = obj_bnd.find('cx')
                obj_cy = obj_bnd.find('cy')
                obj_w = obj_bnd.find('w')
                obj_h = obj_bnd.find('h')
                obj_angle = obj_bnd.find('angle')
                cx = float(obj_cx.text)
                cy = float(obj_cy.text)
                w = float(obj_w.text)
                h = float(obj_h.text)
                angle = float(obj_angle.text)

                x0text, y0text = rotatePoint(cx, cy, cx - w / 2, cy - h / 2, -angle)
                x1text, y1text = rotatePoint(cx, cy, cx + w / 2, cy - h / 2, -angle)
                x2text, y2text = rotatePoint(cx, cy, cx + w / 2, cy + h / 2, -angle)
                x3text, y3text = rotatePoint(cx, cy, cx - w / 2, cy + h / 2, -angle)

                points=np.array([[int(x0text),int(y0text)],[int(x1text),int(y1text)],[int(x2text),int(y2text)],[int(x3text),int(y3text)]],np.int32)
                cv2.polylines(src,[points],True,(255,0,0)) #画任意多边形

          

            # print(x0text,y0text,x1text,y1text,x2text,y2text,x3text,y3text,className,difficulttext)
            wf.write("{} {} {} {} {} {} {} {} {} {}\n".format(x0text,y0text,x1text,y1text,x2text,y2text,x3text,y3text,className,difficulttext))

        #cv2.imshow("ddd",src)
        #cv2.waitKey()


# 转换成四点坐标
def rotatePoint(xc, yc, xp, yp, theta):
    xoff = xp - xc;
    yoff = yp - yc;
    cosTheta = math.cos(theta)
    sinTheta = math.sin(theta)
    pResx = cosTheta * xoff + sinTheta * yoff
    pResy = - sinTheta * xoff + cosTheta * yoff
    return str(int(xc + pResx)), str(int(yc + pResy))

if __name__ == '__main__':
    dir="/home/casso/DataSet1/"
    filelist = os.listdir(dir)
    for file in filelist:
        edit_xml(os.path.join(dir,file))
