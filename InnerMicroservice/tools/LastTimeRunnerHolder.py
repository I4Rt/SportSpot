from datetime import datetime
import os.path


class LastTimeRunnerHolder:
    __lastTime = datetime.now()

    @classmethod
    def setLastTime(cls, t: type(datetime.now())) -> None:
        print('set last time')
        with open('tempFile.txt', 'w') as file:
            file.write(str(t))
        cls.__lastTime = t
        # print('inside: ', cls.getTimeInterval())

    @classmethod
    def getTimeInterval(cls) -> float:
        return (datetime.now() - cls.__lastTime).total_seconds()