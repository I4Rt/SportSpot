import cv2
import time
class CameraSession:
    def __init__(self, route):
        self.route = route
        try:
            self.__stream = cv2.VideoCapture(self.route)
        except:
            raise Exception(f'Unable to get connetion with route "{route}"')
    
    # ?
    def getNextFrame(self):
        while True:
            success, image = self.__stream.read()
            if success:
                ret, jpeg = cv2.imencode('.jpg', image)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(2)
            else:
                try:
                    return (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except:
                    return (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')
                    
    def release(self):
        self.__stream.release()