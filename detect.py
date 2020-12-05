# -*- coding: utf-8 -*-
import cv2
import time
import glob
import numpy as np
import argparse
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--confidence", type=float, default=0.25, help="minimum probability to filter weak detections")
ap.add_argument("-s", "--threshold_score", type=float, default=0.2, help="nms score's thresh")
ap.add_argument("-t", "--threshold", type=float, default=0.5, help="nms's thresh")
arg = vars(ap.parse_args())

class Detect_ship(object):
    CONFIG_PATH = 'yolov3-tiny-hz.cfg'
    WEIGHTS_PATH = 'model/yolov3-tiny-nofocalloss_best.weights'
    LABELS_PATH = 'hz_voc.names'
    CONF_THRESH = arg["confidence"]
    NMS_SCORE_THRESH = arg["threshold_score"]
    NMS_THRESH = arg["threshold"]
    
    @staticmethod
    def detect_v1(img_path:str, NET, LABELS, COLORS)->None:
        boxes = []
        confidences = []
        classIDs = []
        if isinstance(img_path, str):
            image = cv2.imread(img_path)
        else:
            image = img_path
        (H, W) = image.shape[:2]
        # 得到 YOLO需要的输出层
        end2_time = time.time()
        ln = NET.getLayerNames()
        end3_time = time.time()
        print("getLayerNames:", end3_time - end2_time)
        ln = [ln[i[0] - 1] for i in NET.getUnconnectedOutLayers()]
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (608, 608), swapRB=True, crop=False)
        NET.setInput(blob)
        layerOutputs = NET.forward(ln)
        end4_time = time.time()
        print("forward net:", end4_time - end3_time)
        # 在每层输出上循环
        for output in layerOutputs:
            # 对每个检测进行循环
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # 过滤掉那些置信度较小的检测结果
                if confidence > Detect_ship.CONF_THRESH:
                    # 框后接框的宽度和高度
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    # 边框的左上角
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # 更新检测出来的框
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        # 极大值抑制
        end5_time = time.time()
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, Detect_ship.NMS_SCORE_THRESH, Detect_ship.NMS_THRESH)  # 0.2,0.3
        print("NMSBoxes:", time.time() - end5_time)
        nms_box = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                nms_box.append([LABELS[classIDs[i]], boxes[i][0], boxes[i][1], boxes[i][0] + boxes[i][2],
                                boxes[i][1] + boxes[i][3], confidences[i]])

        sorted_boxes = sorted(nms_box, key=lambda x: x[1])  # 按左上角坐标x1从小到大排序

        print("sorted_boxes:", sorted_boxes)
        for i, box in enumerate(sorted_boxes):
            label, x1, y1, x2, y2, confidence = box
            # 在原图上绘制边框和类别
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            text = "{}:{:.3f}".format(label,confidence)
            cv2.putText(image, text, (x1, y2 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        #cv2.imshow("frame", image)
    
if __name__ == "__main__":
    #加载模型
    CONFIG_PATH = 'yolov3-tiny-hz.cfg'
    WEIGHTS_PATH = 'model/yolov3-tiny-nofocalloss_best.weights'
    LABELS_PATH = 'hz_voc.names'
    LABELS = open(LABELS_PATH).read().strip().split('\n')
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
    NET = cv2.dnn.readNetFromDarknet(CONFIG_PATH, WEIGHTS_PATH)
    s1 = time.time()
    print('successfully load net:', time.time()-s1)
    #循环输入图片
    stop_command='stop'
    while True:
        image_input=sys.stdin.readline().strip().split('\n')
        if(image_input is stop_command):
            break
        Detect_ship.detect_v1(image_input, NET, LABELS, COLORS)
 
