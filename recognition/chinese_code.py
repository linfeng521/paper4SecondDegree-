import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def cv2ImgAddText(img, text, left, top, textColor=[255, 0, 0], textSize=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    colors = tuple([int(color) for color in textColor])
    fontText = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, colors, font=fontText)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


if __name__ == '__main__':

    img = cv2.imread('img/zixia.jpg')
    img = cv2ImgAddText(img, "大家好，我是星爷", 140, 60, (255, 255, 0), 20)
    cv2.imshow('img', img)

    while True:
        if cv2.waitKey(1) == 27:
            break
