import cv2
import numpy as np
import chinese_code

# Load Yolo
net = cv2.dnn.readNet("model/yolov3.weights", "model/yolov3.cfg")
# get classes y
classes = []
with open("model/coco.names", "r", encoding='utf-8') as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
# 标记框颜色
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
# img = cv2.imread("traffic.jpg")
img = cv2.imread('../src/ali.jpeg')
# img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channels = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

net.setInput(blob)
outs = net.forward(output_layers)

# Showing informations on the screen
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Rectangle coordinates
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
print(indexes)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)  # bgr
        img = chinese_code.cv2ImgAddText(img, label, x, y - 30, color[::-1])
        # 添加中文支持
        # cv2.putText(img, label, (x, y + 30), font, 1, color, 3)

cv2.imshow("Image", img)
cv2.imwrite("../src/yolov3_out_ali.jpg",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(len(outs))
print(type(outs))
print(outs[0])
print(outs[0][0])
a = np.array(outs)
print(a.shape)
