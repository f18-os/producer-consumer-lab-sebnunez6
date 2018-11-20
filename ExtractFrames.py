#!/usr/bin/env python3

import cv2
import threading
import os
import time
class ExtractFrames(threading.Thread):#creating thread class
	def __init__(self, lock, semaphore, semaphore2, q1= []):
		threading.Thread.__init__(self)
		self.lock = lock
		self.semaphore = semaphore
		self.semaphore2 = semaphore2
		self.q1 = q1
	def run(self):
		# globals
		outputDir    = 'frames'
		clipFileName = 'clip.mp4'
		# initialize frame count
		count = 0

		# open the video clip
		vidcap = cv2.VideoCapture(clipFileName)

		# create the output directory if it doesn't exist
		if not os.path.exists(outputDir):
			print("Output directory {} didn't exist, creating".format(outputDir))
			os.makedirs(outputDir)

		# read one frame
		success,image = vidcap.read()
		print("Reading frame {} {} ".format(count, success))
		while success:
		  # write the current frame out as a jpeg image
		  cv2.imwrite("{}/frame_{:04d}.jpg".format(outputDir, count), image)   
		  success,image = vidcap.read()
		  print('Reading frame {}'.format(count))
		  self.semaphore2.acquire() #Ensuring queue won't be full
		  self.lock.acquire()
		  self.q1.append(count)#adds frame to queue
		  self.lock.release() 
		  self.semaphore.release()#Signaling populating queue
		  count += 1
		self.q1.append(-1)#starts end sequence
		self.semaphore.release()
		self.semaphore2.acquire()
