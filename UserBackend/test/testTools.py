
import os
import sys
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path)
from tools.FileUtil import *
import cv2
if __name__ == "__main__":
    img = cv2.imread('images/img1.jpg')
    encImg = FileUtil.convertImageToBytes(img)
    #cv2.imshow('test', img)
    #cv2.waitKey(0)
    
    data = {'id': '0',
            'camid': 0,
            'sectorid': 0,
            'img': encImg,
            'type': 'floor',
            'params': {'coordinates': [[3.6, 50.4], 
                                       [6.1, 95.1], 
                                       [85.2, 96.1], 
                                       [85.0, 96.1],
                                       [90.2, 86.3],
                                       [89.3, 37.2],
                                       ]}}
    with open('data.json', 'w') as file:
        file.write(json.dumps(data))
        
    decImg = FileUtil.convertBytesToImg(encImg)
    #print(decImg)
    
    cv2.imshow('вывод', decImg)
    cv2.waitKey(0)
    
    