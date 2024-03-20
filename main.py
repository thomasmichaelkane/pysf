import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

image_filename = sys.argv[1]

img = cv2.imread(image_filename)

cv2.imshow("PSF", img)

cv2.waitKey(0)

width = img.shape[0]
height = img.shape[1]

mid_line_x = int(round(width/2))
mid_line_y = int(round(height/2))

profile_x = img[:, mid_line_x]
profile_y = img[mid_line_y, :]

fig1 = plt.figure()
plt.plot(profile_x)

fig2 = plt.figure()
plt.plot(profile_y)

plt.show()



