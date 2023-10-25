from datetime import datetime


class LastTimeRunnerHolder:
    
    __lastTime = datetime.now()
    
    @classmethod
    def setLastTime(cls, t :type(datetime.now())) -> None:
        print('set')
        with open('tempFile.txt', 'w') as file:
            file.write(str(t))
        cls.__lastTime = t
        
    @classmethod
    def getTimeInterval(cls) -> float:
        return (datetime.now() - cls.__lastTime).total_seconds()