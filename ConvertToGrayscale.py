#!/usr/bin/env python3

import cv2
import threading
import time


class GrayScaleThread(threading.Thread): #creating thread class
    def __init__(self, lock,semaphore1, semaphore2, semaphore3, semaphore4, q1= [],q2=[]):
        threading.Thread.__init__(self)
        self.lock = lock
        self.semaphore1 = semaphore1
        self.semaphore2 = semaphore2
        self.semaphore3 =  semaphore3
        self.semaphore4 = semaphore4
        self.q1 = q1
        self.q2 = q2
    def run(self):
        # globals
        outputDir    = 'frames'

        # initialize frame count
        count = 0
        inputFrame = ""

        while inputFrame is not None:
            self.semaphore1.acquire()#Checks if queue is empty
            self.lock.acquire()
            count = self.q1.pop(0)#Retrieves from queue
            self.lock.release()
            self.semaphore2.release()#ensuring queue won't be full
           
            if count == -1:#checks if end sequence has started
                self.q2.append(-1)
                self.semaphore3.release()
                break
            # get the next frame file name
            inFileName = "{}/frame_{:04d}.jpg".format(outputDir, count)

            # load the next file
            inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)
            

            print("Converting frame {}".format(count))

            # convert the image to grayscale
            grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
            
            # generate output file name
            outFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)
            # write output file
            cv2.imwrite(outFileName, grayscaleFrame)
            self.semaphore4.acquire()#Checks if queue2 is full
            self.lock.acquire()
            self.q2.append(count)#receives from queue2
            self.lock.release()
            self.semaphore3.release()#Signaling queue2 won't be empty
