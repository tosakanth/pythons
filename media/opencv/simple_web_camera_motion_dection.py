import cv2

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  d3 = cv2.absdiff(d1,d2)
  return cv2.mean(d3)

cam = cv2.VideoCapture(0)


# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
threshold = 2.0

while True:
  img_diff = diffImg(t_minus, t, t_plus)[0]
  if img_diff > threshold :
	  print "Movement"
  else :
	  print "Stand still"	  
	  
  # Read next image
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

  key = cv2.waitKey(10)
  if key == 27:
    break

print "Goodbye"
