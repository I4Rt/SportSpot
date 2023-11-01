from threading import Thread, Event


class StopableThread(Thread):
    
    def __init__(self, looped = False, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.__looped = looped
        self.__event = Event()
        
    def stop(self, ):
        self.__event.set()
        
    def run(self):
        if self.__looped:
            while not self.__event.is_set():
                self._target(*self._args, **self._kwargs)
        else:
            self._target(self._args, **self._kwargs)
    
    
    

    
    
if __name__ == '__main__':
    from time import sleep
    from datetime import datetime as dt

    def doPrints(text, adder = ''):
        print(str(dt.now()), text, adder)
        sleep(1)
        
    st = StopableThread(target=doPrints, args=('Привет! Я пишу текст!'), kwargs={'adder': 'УРА'}, looped=False)
    st.start()
    
    sleep(7)
    
    st.stop()
    st.join()
    
    print('finished')