import cv2

def diffImg(t0, t1, t2):
  # I chose t0 to be a base frame then I am going to calculate difference of the rest 2 frames
  # from the base frame.
  # To calculate difference between t1 and t0, then between t2 and t0	
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  
  # I get 2 differences then calculate difference between them again
  d3 = cv2.absdiff(d1,d2)
  
  #if there is not a movement (or very little movement) the result value should be low,
  #on the other hand it should be high.
  return cv2.mean(d3)

#initiate camera, I use camera index : 0
cam = cv2.VideoCapture(0)

# Read first three frames:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
threshold = 2.0 # This is my personal experience, you may calibrate it yourself.

while True:
  img_diff = diffImg(t_minus, t, t_plus)[0]
  if img_diff > threshold :
	  print "Movement"
  else :
	  print "Stand still"	  
	  
  # Read next 3 frames and so on.
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

  key = cv2.waitKey(10)
  if key == 27:
    break

print "Goodbye"
