from kafka import KafkaConsumer, KafkaProducer
import json
import cv2
import base64
import datetime
from numpy import frombuffer

from flask import Flask, request, json
import warnings
from ultralytics import YOLO
from base64 import b64decode
from shapely.geometry import Point, Polygon
import os

from threading import Thread

from producer import KafkaProducerPlus, json_serializer

try:
    model = YOLO('model_n.pt')
except:
    print("error in model_n.pt or file not found.")

warnings.filterwarnings("ignore")
app = Flask(__name__)

producer = KafkaProducerPlus(["localhost:9092"], topic="SO1_receive",
                             value_serializer=json_serializer)


def checkIfInside(border, target):
    """Checking if point in polygon or not."""
    return Polygon(border).contains(Point(target[0], target[1]))


def recognition(sectors, image):
    """Recognition image and send the counter."""

    results = model.predict(source=image, imgsz=1920, conf=0.5, classes=[0])
    decImg_h, decImg_w = image.shape[:2]

    counter = 0
    for sector in sectors:
        border = []
        boxes = results[0].boxes

        if sector["mode"] == 1:
            for coord in sector["points"]:
                border.append((round(coord[0] * decImg_w / 100), round(coord[1] * decImg_h / 100)))
            border.append(border[0])
        else:
            border.append([0, 0])
            border.append([decImg_w, 0])
            border.append([decImg_w, decImg_h])
            border.append([0, decImg_h])

        for box in boxes:
            if checkIfInside(border, (box.xyxy[0][0].item(), box.xyxy[0][3].item())) and \
                    checkIfInside(border, (box.xyxy[0][2].item(), box.xyxy[0][3].item())):

                # Only for debugging
                cv2.rectangle(image, (round(box.xyxy[0][0].item()), round(box.xyxy[0][1].item())),
                              (round(box.xyxy[0][2].item()), round(box.xyxy[0][3].item())), (0, 255, 0), 2)
                cv2.putText(image, str(round(box.conf[0].item(), 2)),
                            (round(box.xyxy[0][0].item()), round(box.xyxy[0][1].item()) - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

                counter += 1

    return counter, image  # image we should remove after debugging


class KafkaConsumerPlus:
    consumer = None
    topic = None
    server = None
    group_id = None
    auto_offset_reset = None

    def __init__(self, topic, bootstrap_servers, auto_offset_reset, group_id):
        self.topic = topic
        self.server = bootstrap_servers
        self.auto_offset_reset = auto_offset_reset
        self.group_id = group_id
        self.consumer = KafkaConsumer(self.topic,
                                      bootstrap_servers=self.server,
                                      auto_offset_reset=self.auto_offset_reset,
                                      group_id=self.group_id)

    def getTopic(self):
        return self.topic

    def getGroup(self):
        return self.group


class Analysis(Thread):

    def __init__(self, path, inner, outer):
        Thread.__init__(self)
        self.inner = inner
        self.outer = outer
        self.path = path
        # host
        # TODO: check/make qeries

    def run(self):

        if not os.path.isdir(self.path):
            os.mkdir(self.path)

        # Only for debugging
        if not os.path.isdir(self.path + "/received"):
            os.mkdir(self.path + "/received")
        if not os.path.isdir(self.path + "/detected"):
            os.mkdir(self.path + "/detected")
        if not os.path.isfile(self.path + '/counter.txt'):
            with open(self.path + '/counter.txt', 'x') as f:
                f.write("0")
                f.close()

        consumer = KafkaConsumerPlus(self.inner,
                                     "localhost:9092",
                                     "earliest",
                                     "consumer-group-a")

        producer = KafkaProducerPlus(["localhost:9092"], topic=self.outer,
                                     value_serializer=json_serializer)

        print("starting the consumer ImageReceiver from", self.inner)

        for msg in consumer.consumer:
            try:
                aggregationMode = 1
                taskId = 0
                res_counter = 0

                # Only for debugging
                with open(self.path + '/counter.txt', 'r') as f:
                    count_images = str(int(f.read()) + 1)
                    f.close()
                count_images = "0"*(5 - len(count_images)) + count_images

                threshold = 500
                count_for_delete = 100
                if len([filename for filename in os.listdir(self.path + "/received")]) > threshold:
                    count_deleted = 0
                    for filename in os.listdir(self.path + "/received"):
                        if count_deleted < count_for_delete:
                            os.remove(self.path + "/received/" + filename)
                            count_deleted += 1
                        else:
                            break
                    count_deleted = 0
                    for filename in os.listdir(self.path + "/detected"):
                        if count_deleted < count_for_delete:
                            os.remove(self.path + "/detected/" + filename)
                            count_deleted += 1
                        else:
                            break

                for key_main in json.loads(msg.value):
                    if key_main == "taskId":
                        taskId = json.loads(msg.value)["taskId"]
                    if key_main == "aggregationMode":
                        aggregationMode = json.loads(msg.value)["aggregationMode"]
                    if key_main == "data":
                        list_counter = []
                        for key_data in json.loads(msg.value)["data"]:
                            readImgBytes = base64.b64decode(key_data["img"])
                            npImg = frombuffer(readImgBytes, 'u1')
                            decImg = cv2.imdecode(npImg, 1)
                            cv2.imwrite(f'{self.path}/received/image_received_' + count_images + '.jpg', decImg)

                            cnt, image = recognition(key_data["sectors"], decImg)
                            cv2.imwrite(f'{self.path}/detected/image_detected_' + count_images + '.jpg', image)

                            list_counter.append(cnt)
                        # Sum the people, aggregationMode=1
                        if aggregationMode == 1:
                            res_counter = sum(list_counter)
                        # Find maximum, aggregationMode=2
                        else:
                            res_counter = max(list_counter)
                print('taskId', taskId)

                # Only for debugging
                image = cv2.imread(f'{self.path}/detected/image_detected_' + count_images + '.jpg', 1)
                cv2.putText(image, str(res_counter), (20, 60), cv2.FONT_HERSHEY_SIMPLEX , 1,
                            (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imwrite(f'{self.path}/detected/image_detected_' + count_images + '.jpg', image)
                # Only for debugging
                with open(self.path + '/counter.txt', 'w') as f:
                    f.write(count_images)
                    f.close()

                producer.sendMessage({"taskId": taskId, "counter": res_counter, "aggregationMode": aggregationMode,
                                      "datetime": str(datetime.datetime.now())})

            except Exception as e:
                print('got error', e)


if __name__ == "__main__":
    analizer1 = Analysis('fileData', 'SO1_data', 'SO1_receive')
    analizer2 = Analysis('streamData', 'SO1_local', 'SO1_receive')
    analizer3 = Analysis('streamSideData', 'SO1_side', 'SO1_receive')

    analizer1.start()
    analizer2.start()
    analizer3.start()
    # print('just print')
    '''
    # if not os.path.isdir('queue'):
    #     os.mkdir('queue')

    # consumer  = KafkaConsumerPlus("SO1_local",
    #                               "localhost:9092",
    #                               "earliest",
    #                               "consumer-group-a")

    # print("starting the consumer ImageReceiver")

    # for msg in consumer.consumer:
    #     aggregationMode = 1
    #     taskId = 0
    #     res_counter = 0
    #     for key_main in json.loads(msg.value):
    #         if key_main == "taskId":
    #             taskId = json.loads(msg.value)["taskId"]
    #         if key_main == "aggregationMode":
    #             aggregationMode = json.loads(msg.value)["aggregationMode"]
    #         if key_main == "data":
    #             list_counter = []
    #             for key_data in json.loads(msg.value)["data"]:
    #                 readImgBytes = base64.b64decode(key_data["img"])
    #                 npImg = frombuffer(readImgBytes, 'u1')
    #                 decImg = cv2.imdecode(npImg, 1)
    #                 cv2.imwrite("queue/image_receive.jpg", decImg)

    #                 list_counter.append(recognition(key_data["sectors"]))
    #             # Sum the people, aggregationMode=1
    #             if aggregationMode == 1:
    #                 res_counter = sum(list_counter)
    #             # Find maximum, aggregationMode=2
    #             else:
    #                 res_counter = max(list_counter)

    #     producer.sendMessage({"taskId":  taskId, "counter": res_counter, "aggregationMode": aggregationMode,
    #                           "datetime": str(datetime.datetime.now())})
    '''
