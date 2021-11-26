from Queue import Sender
import time

senderA = Sender("produtos");

count = 1

while(True):
    senderA.send("{1:"+str(count)+"}")
    count += 1
    time.sleep(1)
