# -*- coding: utf-8 -*-
# @Time : 2020-12-05 17:59
# @Author : sloan
# @Email : 630298149@qq.com
# @File : flask_server.py
# @Software: PyCharm

from flask import Flask, jsonify, request
import cv2
import json
import base64
import numpy as np
import time
import logging
app = Flask(__name__)

CONFIG_PATH = '../yolov3-tiny-hz.cfg'
WEIGHTS_PATH = '../model/yolov3-tiny-nofocalloss_best.weights'
LABELS_PATH = '../hz_voc.names'
CONF_THRESH = 0.25
NMS_SCORE_THRESH = 0.2
NMS_THRESH = 0.3
LABELS = open(LABELS_PATH).read().strip().split('\n')
NET = cv2.dnn.readNetFromDarknet(CONFIG_PATH, WEIGHTS_PATH)
print("load net!")

@app.route("/api/detect", methods=['GET', 'POST'])
def detect():
    try:
        z = request.form.to_dict()
        img = z['image']
        roi = z['roi']
        imgString = base64.b64decode(img.encode('utf-8'))
        logging.info('roi:{},{}'.format(roi,type(roi)))
        nparr = np.frombuffer(imgString, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if roi:
            logging.info("crop image")
            x1,y1,x2,y2 = np.int0(roi.split(','))
            image = image[y1:y2,x1:x2]
        s1 = time.time()
        re = detect_v1(image)
        s2 = time.time()
        # res_json2str = json.dumps(res)
        logging.info("detect time:{} s".format(str(s2 - s1)))

    except Exception as e:
        logging.info("error:" + str(e))
        re = ''
    return jsonify({'result': re})

def detect_v1(img_path: str) -> None:
    boxes = []
    confidences = []
    classIDs = []
    if isinstance(img_path, str):
        image = cv2.imread(img_path)
    else:
        image = img_path
    (H, W) = image.shape[:2]
    # 得到 YOLO需要的输出层
    ln = NET.getLayerNames()
    # print("getLayerNames:", end3_time - end2_time)
    ln = [ln[i[0] - 1] for i in NET.getUnconnectedOutLayers()]
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (608, 608), swapRB=True, crop=False)
    # blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (W, H), swapRB=True, crop=False)
    NET.setInput(blob)
    layerOutputs = NET.forward(ln)
    # print("forward net:", end4_time - end3_time)
    # 在每层输出上循环
    for output in layerOutputs:
        # 对每个检测进行循环
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            # 过滤掉那些置信度较小的检测结果
            if confidence > CONF_THRESH:
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
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, NMS_SCORE_THRESH, NMS_THRESH)  # 0.2,0.3
    # print("NMSBoxes:", time.time() - end5_time)
    nms_box = []    # [{"class":'ship',"pos":[x1,y1,x2,y2],"score":0.999}]
    if len(idxs) > 0:
        for i in idxs.flatten():
            obj_ins = {}
            obj_ins['class'] = LABELS[classIDs[i]]
            obj_ins['pos'] = [boxes[i][0], boxes[i][1], boxes[i][0] + boxes[i][2], boxes[i][1] + boxes[i][3]]
            obj_ins['score'] = confidences[i]
            nms_box.append(obj_ins)
            # nms_box.append([LABELS[classIDs[i]], boxes[i][0], boxes[i][1], boxes[i][0] + boxes[i][2],
            #                 boxes[i][1] + boxes[i][3], confidences[i]])
    return nms_box

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(port=4392)

