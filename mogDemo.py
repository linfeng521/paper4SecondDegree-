import cv2
'''
动态目标识别使用MOG2背景拆分
'''

cap = cv2.VideoCapture('src/vtest.avi')
size =(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter('src/outputVideo.avi', fourcc, 25, size)

# fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)
#KNN背景分割器
knn = cv2.createBackgroundSubtractorKNN(detectShadows = True)
while cap.isOpened():

    ret,frame = cap.read()
    if ret == False:
        continue
    # fgmask = fgbg.apply(frame)
    fgmask = knn.apply(frame)

    ret, thread_fg = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)

    # 形态学闭运算(消除黑洞)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    binary_closing = cv2.morphologyEx(thread_fg, cv2.MORPH_CLOSE, kernel,iterations=2)

    contours, hierarchy = cv2.findContours(binary_closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) > 100:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            '''
            # 最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (255, 0, 0), 1)
            '''

    # cv2.imshow("diff", frame & cv2.cvtColor(thread_fg, cv2.COLOR_GRAY2BGR))
    # cv2.imshow('close', binary_closing)
    # cv2.imshow("frame", fgmask)
    # cv2.imshow('thread',thread_fg)
    if ret and cv2.waitKey(35) & 0xFF != ord('q'):
        cv2.imshow('frame', frame)
        video_writer.write(frame)
    else:
        break

video_writer.release()
cap.release()
cv2.destroyAllWindows()