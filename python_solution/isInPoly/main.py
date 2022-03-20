from shapely import geometry
import math

def ConvertFormat(x,y,w,h,θ):
    x11 = x-w/2
    y11 = y+h/2

    x12 = x-w/2
    y12 = y-h/2

    x13 = x+w/2
    y13 = y+h/2

    x14 = x+w/2
    y14 = y-h/2

    X1 = (x12 - x) * math.cos(θ) - (y12 - y) * math.sin(θ) + x
    Y1 = (y12 - y) * math.cos(θ) + (x12 - x) * math.sin(θ) + y
    X2 = (x11 - x) * math.cos(θ) - (y11 - y) * math.sin(θ) + x
    Y2 = (y11 - y) * math.cos(θ) + (x11 - x) * math.sin(θ) + y
    X3 = (x13 - x) * math.cos(θ) - (y13 - y) * math.sin(θ) + x
    Y3 = (y13 - y) * math.cos(θ) + (x13 - x) * math.sin(θ) + y
    X4 = (x14 - x) * math.cos(θ) - (y14 - y) * math.sin(θ) + x
    Y4 = (y14 - y) * math.cos(θ) + (x14 - x) * math.sin(θ) + y
    return (X1, Y1), (X2, Y2), (X3, Y3), (X4, Y4)


def if_inPoly(polygon, Points):
    line = geometry.LineString(polygon)
    point = geometry.Point(Points)
    polygon = geometry.Polygon(line)
    return polygon.contains(point)


square = [(0, 0), (1, 0), (1, 1), (0, 1)]  # 多边形坐标
pt1 = (2, 2)  # 点坐标
pt2 = (0.5, 0.5)
print(if_inPoly(square, pt1))
print(if_inPoly(square, pt2))


 # //角度转换
 #    let X1, Y1, X2, Y2, X3, Y3, X4, Y4;
 #    let θ = (180-arrowθ) * math.PI / 180,
 #    back_left = {
 #      x: x - scaleW / 2,
 #      y: y + scaleH / 2,
 #    },
 #    back_right = {
 #      x: x - scaleW / 2,
 #      y: y - scaleH / 2,
 #    },
 #    front_left = {
 #      x: x + scaleW / 2,
 #      y: y + scaleH / 2,
 #    },
 #    front_right = {
 #      x: x + scaleW / 2,
 #      y: y - scaleH / 2,
 #    };
 #     //按逆时针或者顺时针旋转角度center.x后的四个点坐标
 #    X1 = (back_right.x - x) * math.cos(θ) - (back_right.y - y) * math.sin(θ) + x;
 #    Y1 = (back_right.y - y) * math.cos(θ) + (back_right.x - x) * math.sin(θ) + y;
 #    X2 = (back_left.x - x) * math.cos(θ) - (back_left.y - y) * math.sin(θ) + x;
 #    Y2 = (back_left.y - y) * math.cos(θ) + (back_left.x - x) * math.sin(θ) + y;
 #    X3 = (front_left.x - x) * math.cos(θ) - (front_left.y - y) * math.sin(θ) + x;
 #    Y3 = (front_left.y - y) * math.cos(θ) + (front_left.x - x) * math.sin(θ) + y;
 #    X4 = (front_right.x - x) * math.cos(θ) - (front_right.y - y) * math.sin(θ) + x;
 #    Y4 = (front_right.y - y) * math.cos(θ) + (front_right.x - x) * math.sin(θ) + y;
 #    back_right=[X2,Y2];
 #    back_left = [X1,Y1];
 #    front_left = [X3,Y3];
 #    front_right = [X4,Y4];
 #    return [back_left,back_right,front_left,front_right]```

