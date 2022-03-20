import cv2
import math


def draw_grasping(img, center_x, center_y, angel):
    x1 = int(90 * math.cos(angel) - 10 * math.sin(angel) + center_x)
    y1 = int(90 * math.sin(angel) + 10 * math.cos(angel) + center_y)

    x2 = int(70 * math.cos(angel) - 10 * math.sin(angel) + center_x)
    y2 = int(70 * math.sin(angel) + 10 * math.cos(angel) + center_y)

    x3 = int(70 * math.cos(angel) + 10 * math.sin(angel) + center_x)
    y3 = int(70 * math.sin(angel) - 10 * math.cos(angel) + center_y)

    x4 = int(90 * math.cos(angel) + 10 * math.sin(angel) + center_x)
    y4 = int(90 * math.sin(angel) - 10 * math.cos(angel) + center_y)

    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
    cv2.line(img, (x2, y2), (x3, y3), (255, 0, 0), 3)
    cv2.line(img, (x3, y3), (x4, y4), (255, 0, 0), 3)
    cv2.line(img, (x4, y4), (x1, y1), (255, 0, 0), 3)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    center_x1, center_y1 = 912.1343, 181.50093
    center_x2, center_y2 = 405.3361, 158.3884
    center_x3, center_y3 = 653.05676, 378.2073
    center_x4, center_y4 = 673.5327, 130.30548
    center_x5, center_y5 = 965.5416, 486.4309
    center_x6, center_y6 = 409.07892, 529.0702


    img = cv2.imread('./0.jpg')
    for i in range(6):
        draw_grasping(img, center_x1, center_y1, -0.67571485 + 3.14159265 / 3 * i)
        draw_grasping(img, center_x2, center_y2, -1.1097399 + 3.14159265 / 3 * i)
        draw_grasping(img, center_x3, center_y3, -0.9652691 + 3.14159265 / 3 * i)
        draw_grasping(img, center_x4, center_y4, -1.5653238 + 3.14159265 / 3 * i)
        draw_grasping(img, center_x5, center_y5, -1.246181 + 3.14159265 / 3 * i)
        draw_grasping(img, center_x6, center_y6, -0.74276346 + 3.14159265 / 3 * i)

    cv2.circle(img, (math.ceil(center_x1), math.ceil(center_y1)), 5, (0, 0, 255), 3)
    cv2.circle(img, (math.ceil(center_x2), math.ceil(center_y2)), 5, (0, 0, 255), 3)
    cv2.circle(img, (math.ceil(center_x3), math.ceil(center_y3)), 5, (0, 0, 255), 3)
    cv2.circle(img, (math.ceil(center_x4), math.ceil(center_y4)), 5, (0, 0, 255), 3)
    cv2.circle(img, (math.ceil(center_x5), math.ceil(center_y5)), 5, (0, 0, 255), 3)
    cv2.circle(img, (math.ceil(center_x6), math.ceil(center_y6)), 5, (0, 0, 255), 3)


    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 0
# 912.1343 181.50093 -0.67571485 -38.7156091279465
# 1
# 405.3361 158.3884 -1.1097399 -63.58341267902975
# 2
# 653.05676 378.2073 -0.9652691 -55.30584494273027
# 3
# 673.5327 130.30548 -1.5653238 -89.6864491127321
# 5
# 965.5416 486.4309 -1.246181 -71.40091253268982
# 9
# 409.07892 529.0702 -0.74276346 -42.557211464969406