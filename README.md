# Producer Consumer Lab

For this lab you will implement a trivial producer-consumer system using
python threads where all coordination is managed by counting and binary
semaphores for a system of two producers and two consumers. The producers and
consumers will form a simple rendering pipeline using multiple threads. One
thread will read frames from a file, a second thread will take those frames
and convert them to grayscale, and the third thread will display those
frames. The threads will run concurrently.

## File List
### ExtractFrames.py
Extracts a series of frames from the video contained in 'clip.mp4' and saves 
them as jpeg images in sequentially numbered files with the pattern
'frame_xxxx.jpg'.

### ConvertToGrayscale.py
Loads a series for frams from sequentially numbered files with the pattern
'frame_xxxx.jpg', converts the grames to grayscale, and saves them as jpeg
images with the file names 'grayscale_xxxx.jpg'

### DisplayFrames.py
Loads a series of frames sequently from files with the names
'grayscale_xxxx.jpg' and displays them with a 42ms delay.

### ExtractAndDisplay.py
Loads a series of framss from a video contained in 'clip.mp4' and displays 
them with a 42ms delay

## Requirements
* Extract frames from a video file, convert them to grayscale, and display
them in sequence
* You must have three functions
  * One function to extract the frames
  * One function to convert the frames to grayscale
  * One function to display the frames at the original framerate (24fps)
* The functions must each execute within their own python thread
  * The threads will execute concurrently
  * The order threads execute in may not be the same from run to run
* Threads will need to signal that they have completed their task
* Threads must process all frames of the video exactly once
* Frames will be communicated between threads using producer/consumer idioms
  * Producer/consumer quesues will be bounded at ten frames

Note: You may have ancillary objects and method in order to make you're code easer to understand and implement.

##Extract frames
class was turned into a thread with freudenthal's code. Mutex 
is used to lock and release when adding to a queue that will tell the ConvertToGrayscale which frame to
convert. If the queue is full it will wait until resources have been used. Once
it is done extracting frames it will queue -1 to signify the end of the video.

##DisplayFrames
Class was turned into a thread with freudenthal's code. Mutex is used 
to lock and release when receiving frames from the queue provided by
ConvertToGrayscale. If the queue is empty the code will loop until input is received.
If the end sequence is received the thread will finish running.

##ConvertToGrayscale
Class was turned into a thread with freudenthal's code. Mutex 
is used to lock and release when adding to a queue that will tell the Display
which frame to display. If the queue is full it will wait until resources  in the queue have been used. 
It receives frames while utilizing mutex from the frames queue and will run until the end sequence is received. If 
nothing is in the queue it will loop around until input is received. 

##theAllMighty
Class calls all the threads