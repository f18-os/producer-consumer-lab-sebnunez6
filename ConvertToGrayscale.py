#!/usr/bin/env python3

import cv2
import threading
import time


class GrayScaleThread(threading.Thread):
    def __init__(self, lock, q1= [],q2=[]):
        threading.Thread.__init__(self)
        self.lock = lock
        self.q1 = q1
        self.q2 = q2
    def run(self):
        # globals
        outputDir    = 'frames'

        # initialize frame count
        count = 0
        inputFrame = ""

        while inputFrame is not None:
            self.lock.acquire()
            if(len(self.q1) > 0):
                count = self.q1.pop(0)
                while len(self.q2) > 10:
                    self.lock.release()
                    time.sleep(.100) #gives other threads time to catch up
                    self.lock.acquire()
                self.q2.append(count)
                if count == -1:
                    self.q2.append(-1)
                    self.lock.release()
                    break
            else:
                self.lock.release()
                continue
            self.lock.release()
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

            # # generate input file name for the next frame
            # inFileName = "{}/frame_{:04d}.jpg".format(outputDir, count)

            # # load the next frame
            # inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)

    
    
