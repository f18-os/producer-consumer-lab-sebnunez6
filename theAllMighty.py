from ExtractFrames import *
from ConvertToGrayscale import *
from DisplayFrames import *
import threading

lock = threading.Lock()
list1 = [] #list to convert to grayscales
list2 = [] #list to display
extractThread = ExtractFrames(lock,list1)
ConvertToGrayscale = GrayScaleThread(lock,list1,list2)
extractThread.start()
ConvertToGrayscale.start()
