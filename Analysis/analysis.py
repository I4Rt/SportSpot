from flask import Flask, request, json
import warnings
from ultralytics import YOLO
import json
from base64 import b64decode
import cv2
from shapely.geometry import Point, Polygon
import os


model = YOLO('yolov8n.pt')
warnings.filterwarnings("ignore")
app = Flask(__name__)


def checkIfInside(border, target):
    """Checking if point in polygon or not."""
    return Polygon(border).contains(Point(target[0], target[1]))


@app.route('/recognition', methods=['GET', 'POST'])
def recognition():
    """Recognition image and send the counter."""
    data = json.loads(request.stream.read())
    id = data.get('id', None)
    camid = data.get('camid', None)
    sectorid = data.get('sectorid', None)
    type = data.get('type', None)
    coords = data.get('params', None)

    camera_image = b64decode(data.get('img', None))
    with open(r'queue\\{}.jpg'.format(id), 'wb') as image:
        image.write(camera_image)
        image_cv2 = cv2.imread(r'queue\\{}.jpg'.format(id))

    results = model.predict(source=image_cv2, imgsz=1920, conf=0.25, classes=[0])
    decImg_h, decImg_w = image_cv2.shape[:2]
    border = []

    for coord in coords['coordinates']:
        border.append((round(coord[0] * decImg_w / 100), round(coord[1] * decImg_h / 100)))
    border.append(border[0])

    counter = 0
    # Check our person in polygon it or not
    boxes = results[0].boxes
    for box in boxes:
        if checkIfInside(border, (box.xyxy[0][0].item(), box.xyxy[0][3].item())) and \
                checkIfInside(border, (box.xyxy[0][2].item(), box.xyxy[0][3].item())):
            counter += 1

    response = app.response_class(
        response=json.dumps({'count': counter}),
        status=200,
        mimetype='application/json'
    )

    return response


if __name__ == "__main__":
    if not os.path.isdir('queue'):
        os.mkdir('queue')
    
    app.run(host='0.0.0.0', debug=False)
