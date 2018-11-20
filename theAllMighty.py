#!/usr/bin/python
#importing all threads
from ExtractFrames import *
from ConvertToGrayscale import *
from DisplayFrames import *
import threading

lock = threading.Lock()
list1 = [] #list to convert to grayscales
list2 = [] #list to display
#intializing and starting threads
semaphore = threading.Semaphore(0)
semaphore2 = threading.Semaphore(10)
semaphore3 = threading.Semaphore(0)
semaphore4 = threading.Semaphore(10)
extractThread = ExtractFrames(lock,semaphore, semaphore2, list1)
ConvertToGrayscale = GrayScaleThread(lock,semaphore, semaphore2, semaphore3, semaphore4, list1,list2)
DisplayThread = displayFrames(lock,semaphore3, semaphore4, list2)
extractThread.start()
ConvertToGrayscale.start()
DisplayThread.start()