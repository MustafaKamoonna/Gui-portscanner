#!/usr/bin/env python

from easygui import *
import socket
import threading
import Queue


choices = ["Host/IP", "Start Port", "End Port"]
Answers = multenterbox("Please Enter The Required Fields", "Port Scanner", choices)
ip,startport,endport = Answers

#ip = "127.0.0.1"
ports = range(int(startport), int(endport))
print_lock = threading.Lock()

class WorkerThread(threading.Thread):
    def __init__(self,queue,tid):
        threading.Thread.__init__(self)
        self.queue = queue
        self.tid = tid
        print "Worker %d reporting at your service" %self.tid

    def run(self):
        total_ports = 0
        while True:
            port = 0
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(3)
            try:
                port = self.queue.get(timeout=1)
                try:
                    response = sock.connect((ip,port))   
                    with print_lock:
                    
                        print("Port %d is OPEN" %port)       
                except:
                    pass
                sock.close()


            except Queue.Empty:
                print "Worker %d have exited, no more ports to scan" %self.tid
                return
            
                
            self.queue.task_done()
            total_ports +=1

queue = Queue.Queue()
threads = []
for i in range(1, 5):
    print "Creating worker thread id %d" %i
    worker = WorkerThread(queue, i)
    worker.setDaemon(True)
    worker.start()
    threads.append(worker)
    print "Worker thread id %d created" %i

for j in ports:
    queue.put(j)

queue.join()

#wait for all threads to exit

for item in threads:
    item.join()


print "Scan Completed"
    
