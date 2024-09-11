This is a Python application with a tkinter UI that uses PIL to process images. The purpose is to be able to add a watermark (image) on to a main image.

I referenced the pillow documentation and worked on getting code for the image processing working. 
I then migrated that code into it's own class and used a function that took parameters:
 image - the main image file path
 watermark - the watermark image (transparency supported and recommended)
 size of the watermark as a percentage value (float)
 opacity of the watermark as a percentage value (float)
 6 options for where to position the watermark 
  "tl" top left
  "tc" top center
  "br" bottom right, ect

I then worked with tkinter to develop the UI from a mock up I created. 

I used :
 file dialogs
 sliders
 radio buttons
 along with more basic buttons and labels

I checked that specified paths were inputted correctly
I included a preview option
I included an export functionality

What was hard, what was easy: 
 At first, just getting started an familiarized was hard, but once I got rolling in pillow then in tkinter, things started to come together. Understanding the image processing , masking and blending modes in pillow at first was hard, but eventually I got the hang of it.

How might you improve for the next project? What was your biggest learning from today? 
 How to process the images was the biggest thing I learned. This is a program I would have used a few years ago when I was doing a lot of photography.

What would you do differently if you were to tackle this project again?
 I don't think i would have done too much differently. 


