#!/usr/bin/env python3

import cv2
import time
import threading
import time

class displayFrames(threading.Thread):
    def __init__(self, lock, q2=[]):
        threading.Thread.__init__(self)
        self.lock = lock
        self.q2 = q2
    def run(self):
        # globals
        outputDir    = 'frames'
        frameDelay   = 42       # the answer to everything

        # initialize frame count
        count = 0

        startTime = time.time()
     
        frame = ""
        while frame is not None:
            self.lock.acquire()
            if(len(self.q2) > 0):#checking if queue is empty
                count = self.q2.pop(0)
                if count == -1:#means end sequence has started
                    break
            else:
                self.lock.release()
                time.sleep(.1)#give the other threads some time to produce
                continue
            self.lock.release()
            # Generate the filename for the first frame 
            frameFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)

            # load the frame
            frame = cv2.imread(frameFileName)

            # compute the amount of time that has elapsed
            # while the frame was processed
            diff = 0.0417 + startTime
            if diff - time.time() > 0:  #ensuring that the time duration is 24 fps
                time.sleep(diff-time.time())
            elapsedTime = int((time.time() - startTime)*1000)
            print("Time to process frame {} ms".format(elapsedTime))

            print("Displaying frame {}".format(count))
            # Display the frame in a window called "Video"
            cv2.imshow("Video", frame)
            
            # determine the amount of time to wait, also
            # make sure we don't go into negative time
            timeToWait = max(1, frameDelay - elapsedTime)

            # Wait for 42 ms and check if the user wants to quit
            if cv2.waitKey(timeToWait) and 0xFF == ord("q"):
                break    

            # get the start time for processing the next frame
            startTime = time.time()


        # make sure we cleanup the windows, otherwise we might end up with a mess
        cv2.destroyAllWindows()
