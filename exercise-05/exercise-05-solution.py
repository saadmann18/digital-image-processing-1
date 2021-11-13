#!/usr/bin/env python
# coding: utf-8


# In[1]:

import cv2
import numpy as np
from matplotlib import pyplot as plt

dpi = plt.rcParams['figure.dpi']

# plot grayscale image in original size
def plot_img_orig(img):
    rows, cols = img.shape # image size
    fig = plt.figure(figsize = (cols/dpi, rows/dpi))
    fig.add_axes([0, 0, 1, 1])
    plt.axis('off')
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.show()

# In[2]:


# read the image as a grayscale image (parameter 0)
img = cv2.imread('images/pollen-var1.png', 0)
plot_img_orig(img)



# In[3]:
# compute histogram of given image

rows, cols = img.shape # image size

# list to save frequency of each gray value
hist = np.zeros(256, dtype=np.float64)

for iy in range(rows):
    for jx in range(cols):
        val = img[iy, jx] # get current gray value
        hist[val] += 1
            
hist    

# In[4]:
    
# compute histogram
#hist = compute_histogram(img)

# plot the result
val = np.arange(256) # horizontal axis (gray values)
plt.bar(val, hist, 1)
plt.show()


# In[ ]:

# compare with matplotlib
# `pollen-var1.png`: dark image.
plt.hist(cv2.imread('images/pollen-var1.png', 0).flatten(), 255, [0, 256])
plt.title('pollen-var1.png')
plt.show()

# In[ ]:

# histograms of the remaining three images
# `pollen-var2.png`: light image.
plt.hist(cv2.imread('images/pollen-var2.png', 0).flatten(), 255, [0, 256])
plt.title('pollen-var2.png')
plt.show()

# `pollen-var3.png`: low-contrast image.
plt.hist(cv2.imread('images/pollen-var3.png', 0).flatten(), 255, [0, 256])
plt.title('pollen-var3.png')
plt.show()

# `pollen-var4.png`: high-contrast image.
plt.hist(cv2.imread('images/pollen-var4.png', 0).flatten(), 255, [0, 256])
plt.title('pollen-var4.png')
plt.show()


# In[3]:
# compute histogram of given image
def compute_histogram(img):
    rows, cols = img.shape # image size
    
    # list to save frequency of each gray value
    hist = np.zeros(256, dtype=np.float64)
    
    for iy in range(rows):
        for jx in range(cols):
            val = img[iy, jx] # get current gray value
            hist[val] += 1
            
    return hist  
    
# In[3]:

# write your code here

# apply histogram equalization to given image
img = cv2.imread('images/checkerboard-small.png', 0)
rows, cols = img.shape # image size

# compute histogram (or use np.histogram)
hist = compute_histogram(img)

# normalize histogram ##kind of probability of occurances of certain pixels
hist_norm = hist / (rows * cols) #from slide 3-20
#print(sum(hist_norm)) # just for control

# compute transfer function ##kind of CDF calculation
tf = np.zeros(256, dtype=np.float64) # numpy array with zeros

for i in range (hist_norm.size):
    tf[i] = 255 * sum(hist_norm[0:i+1])

# equalization
res = np.zeros(shape=[rows, cols], dtype=np.uint8) # empty image to show the result

for iy in range(rows):
    for jx in range(cols):
        res[iy, jx] = tf[img[iy, jx]]   ##res[0,0] = tf[img[0,0]] 
                                     #--> res[0,0] = tf[42] pixel value at img[0,0]
                                     #--> tf[42] = 183.362, but dtype makes it integer
# equalize the four images and plot the results
plot_img_orig(img)
plot_img_orig(res)
plt.hist(res.flatten(), 255, [0, 256]); 
plt.title('pollen-var1.png'); 
plt.show()

# img = cv2.imread('images/pollen-var2.png', 0)
# res2, tf2 = histogram_equalization(img)
# plot_img_orig(res2)
# plt.hist(res2.flatten(), 255, [0, 256]); plt.title('pollen-var2.png'); plt.show()

# img = cv2.imread('images/pollen-var3.png', 0)
# res3, tf3 = histogram_equalization(img)
# plot_img_orig(res3)
# plt.hist(res3.flatten(), 255, [0, 256]); plt.title('pollen-var3.png'); plt.show()

# img = cv2.imread('images/pollen-var4.png', 0)
# res4, tf4 = histogram_equalization(img)
# plot_img_orig(res4)
# plt.hist(res4.flatten(), 255, [0, 256]); plt.title('pollen-var4.png'); plt.show()

# plot the transfer functions
val = np.arange(256) # horizontal axis (gray values)
plt.step(val, tf, label='pollen-var1.png')
# plt.step(val, tf2, label='pollen-var2.png')
# plt.step(val, tf3, label='pollen-var3.png')
# plt.step(val, tf4, label='pollen-var4.png')

plt.title("Transfer functions")
plt.xlabel("r")
plt.ylabel("s")

plt.legend()
plt.show()

# checkerboard
# img = cv2.imread('images/checkerboard-small.png', 0)
# res, tf = histogram_equalization(img)
# plot_img_orig(res)

# In[4]:
# apply histogram equalization to given image
def histogram_equalization(img):
    rows, cols = img.shape # image size
    
    # compute histogram (or use np.histogram)
    hist = compute_histogram(img)
    
    # normalize histogram
    hist_norm = hist / (rows * cols)
    print(sum(hist_norm)) # just for control
    
    # compute transfer function
    tf = np.zeros(256, dtype=np.float64) # numpy array with zeros
    
    for i in range (hist_norm.size):
        tf[i] = 255 * sum(hist_norm[0:i+1])

    # equalization
    res = np.zeros(shape=[rows, cols], dtype=np.uint8) # empty image

    for i in range(rows):
        for j in range(cols):
            res[i, j] = tf[img[i, j]]
    
    # return final result and transfer function
    return res, tf
# In[5]:
# apply local histogram equalization to given image using NxN windows (odd N required)

img = cv2.imread('images/squares.png', 0)
n = 3
rows, cols = img.shape # image size

# create empty image
res = np.zeros(shape=[rows, cols], dtype=np.uint8)

# compute offset
h = int(n / 2)

# move from pixel to pixel (border is just left out)
for iy in range(h, rows-h):
    for jx in range(h, cols-h):
        # get local neighborhood
        nbh = img[iy-h:iy+h+1, jx-h:jx+h+1]
        
        # compute transfer function and equalized neighborhood
        res_he, tf = histogram_equalization(nbh)
        
        # use the transfer function to assign the new gray value
        res[iy, jx] = tf[img[iy, jx]]
        
        # print some status information
        print("row = " + str(iy), end='\r') # current row
        
# return final result
res

# plot original image
#img = cv2.imread('images/squares.png', 0)
plot_img_orig(img)

# equalize the four images and plot the results
res_global, tf = histogram_equalization(img)
plot_img_orig(res_global)

# local histogram equalization
res_local = res
plot_img_orig(res_local)
cv2.imwrite('output/local.png', res_local)

# checkerboard
# img = cv2.imread('images/checkerboard-small.png', 0)
# res_local = local_histogram_equalization(img, 3)
# plot_img_orig(res_local)


# The global histogram equalization is not suitable to clearly identify the hidden symbols inside the boxes. The local method works much better, but mainly highlights the edges and considerably amplifies the noise. Furthermore, the method is quite slow (but it can be accelerated by reusing data, because only one row or column changes when moving from pixel to pixel). A better method for such problems is a local enhancement using histogram statistics.
# 
# The checkerboard consists of homogeneous areas (only one gray value) so that the equalization does only have an effect on the edges. 
