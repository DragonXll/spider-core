import json
import re
import cv2
import numpy as np
import base64

def alpha2white(img):
    '''
    将透明的缺口图转换为黑色背景的缺口图
    :param img:
    :return:
    '''
    sp = img.shape
    width = sp[0]
    height = sp[1]
    for yh in range(height):
        for xw in range(width):
            color_d = img[xw, yh]
            if (color_d[3] != 255):  # 找到alpha通道不為255的像素
                img[xw, yh] = [0, 0, 0, 0]  # 改變這個像素
    return img


def find_part_about_hk(img, safe_space=5):
    '''
    找到缺口在原图上对应的 y坐标 的取值范围
    :param img: 处理过透明度后的缺口图
    :return:
    '''
    # h158 * w60
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    part_of_index = np.where(gray_img.sum(axis=1) > 0)
    # print(part_of_index)
    # 得到滑块对应的区域大小
    min_part = list(part_of_index)[0][0]
    max_part = list(part_of_index)[0][-1]
    # print(min_part, max_part)

    hk_img = img[min_part - safe_space:max_part + safe_space, :]
    # show_img(hk_img)

    return min_part, max_part, hk_img


def get_roi(img, init_min_y, init_max_y, safe_space=5):
    '''
    从原始的大图中截取出 可能存在小图的区域
    :param img: 原始大图
    :param init_y: 请求缺口图时返回的缺口图初始y坐标
    :param ksize: 缺口图的大小
    '''
    roi_img_rbg = img[init_min_y - safe_space + 2:init_max_y + safe_space + 2, :]
    # show_img(roi_img_rbg)
    roi_img_gray = cv2.cvtColor(roi_img_rbg, cv2.COLOR_BGR2GRAY)
    return roi_img_gray, roi_img_rbg


def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.frombuffer(imgString, np.uint8)
    # image = cv2.imdecode(nparr,1)
    return nparr


def get_base64(base64_url):
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", base64_url, re.DOTALL)
    return result.groupdict().get("data")


def run(background, slider):
    small_img = cv2.imdecode(base64_cv2(get_base64(slider)), -1)
    small_img = alpha2white(small_img)
    min_part, max_part, hk_img = find_part_about_hk(small_img)
    h, w, c = hk_img.shape

    big_img = cv2.imdecode(base64_cv2(get_base64(background)), 1)
    roi_img_gray, roi_img_rbg = get_roi(big_img, min_part, max_part)
    # cv2.imshow('img', small_img)
    # cv2.imshow('img', big_img)
    # 进行边缘检测
    roi_img_canny = cv2.Canny(roi_img_gray, 50, 100)
    hk_img_canny = cv2.Canny(cv2.cvtColor(hk_img, cv2.COLOR_BGR2GRAY), 300, 300)


    res = cv2.matchTemplate(image=roi_img_canny, templ=hk_img_canny, method=cv2.TM_CCOEFF_NORMED)
    # print(res)
    print(np.max(res))  # 匹配的最大概率
    loc = np.where(res == np.max(res))

    # 可能匹配多个目标的固定写法，如果是确定只有一个目标可以用 minMaxLoc 函数处理，从loc中遍历得到的左上坐标 pt -> (10, 10)
    for pt in zip(*loc[::-1]):
        # 指定左上和右下坐标 画矩形
        # cv2.rectangle(roi_img_rbg, pt, (pt[0] + w, pt[1] + h), color=(0, 0, 255), thickness=2)
        pts = pt[0]

    return pts
