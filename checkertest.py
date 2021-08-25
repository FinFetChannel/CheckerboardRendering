import numpy as np
import cv2

frame0 = cv2.imread('2.png').astype('int') # current frame
frame00 = cv2.imread('1.png').astype('int') # previous frame 

height, width = frame0.shape[0], frame0.shape[1]

checkered = frame0.copy()
average = frame0.copy()
interlaced = frame0.copy()
diff = frame0.copy()
for j in range(width):
    for i in range(height):
        if i%2 == j%2:
            checkered[i][j] = [0,0,0]
            interlaced[i][j] = frame00[i][j]
            if i > 0 and i < height-1 and j > 0 and j < width-1:
                average[i][j] = np.mean([frame0[i][j-1],frame0[i-1][j],frame0[i][j+1], frame0[i+1][j]], axis=0)
                if max(np.abs(diff[i][j-1] - diff[i][j+1])) < 30:
                    diff[i][j] = np.mean([diff[i][j+1], diff[i][j-1]], axis = 0)
                elif max(np.abs(diff[i-1][j] - diff[i+1][j])) < 30:
                    diff[i][j] = np.mean([diff[i-1][j], diff[i+1][j]], axis = 0)
                else:
                    diff[i][j] = average[i][j]              
            elif i > 0 and i < height -1:
                average[i][j] = np.mean([diff[i-1][j], diff[i+1][j]], axis = 0)
                diff[i][j] = average[i][j]
            elif j > 0 and j < width-1:
                average[i][j] = np.mean([diff[i][j+1], diff[i][j-1]], axis = 0)
                diff[i][j] = average[i][j]

resized = cv2.resize(frame0.astype('uint8'), (905,509), interpolation = cv2.INTER_AREA)
resized = cv2.resize(resized, (1280,720), interpolation = cv2.INTER_CUBIC)
mixed = (interlaced + diff)/2
cv2.imwrite("checkered.png", checkered.astype('uint8'))
cv2.imwrite("average.png", average.astype('uint8'))
cv2.imwrite("interlaced.png", interlaced.astype('uint8'))
cv2.imwrite("differential.png", diff.astype('uint8'))
cv2.imwrite("resized.png", resized)
cv2.imwrite("mixed.png", mixed.astype('uint8'))
