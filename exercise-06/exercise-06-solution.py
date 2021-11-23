#!/usr/bin/env python
# coding: utf-8

# In[1]:
    
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

dpi = plt.rcParams['figure.dpi']

# plot grayscale image in original size
def plot_img_orig(img):
    rows, cols = img.shape # image size
    fig = plt.figure(figsize = (cols/dpi, rows/dpi))
    fig.add_axes([0, 0, 1, 1])
    plt.axis('off')
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.show()

# In[6]:

# write your code here

# apply local enhancement image using nxn windows (odd n required)
def enhance_local(img, n, k0, k1, k2, k3, c):
    rows, cols = img.shape # image size
    
    # compute global mean and variance
    m_g = np.mean(img); print("global mean = " + str(m_g))
    std_g = np.std(img); print("global std = " + str(std_g))
    
    # create copy of image
    res = img.copy()
    
    # compute offset
    h = int(n / 2)
    
    # move from pixel to pixel (border is just left out)
    for iy in range(h, rows-h):
        for jx in range(h, cols-h):
            # get local neighborhood
            nbh = img[iy-h:iy+h+1, jx-h:jx+h+1]
            
            # compute local mean and variance
            m_l = np.mean(nbh)
            std_l = np.std(nbh)
            
            # process pixels
            if (k0*m_g <= m_l and m_l <= k1*m_g and k2*std_g <= std_l and std_l <= k3*std_g):
                res[iy, jx] = c * img[iy, jx]
            
            # print some status information
            print("row = " + str(iy), end='\r') # current row
            
    # return final result
    return res


# In[8]:
# read the image as a grayscale image (parameter 0)
img = cv2.imread('images/squares2.png', 0)
plot_img_orig(img)

# In[9]:

# check histogram
plt.hist(img.flatten(), 255, [0, 256])
plt.show()

# In[10]:

hist, bins = np.histogram(img, bins=np.arange(257)) # bins are the bin edges (e.g. 2 values require 3 edges)
print(hist) # check numerical values

# In[11]:

# enhance image and plot the result
res = enhance_local(img, 3, 0, 0.2, 0, 0.2, 10.0)
plot_img_orig(res)

# In[12]:

# test for checkerboard
img_cb = cv2.imread('images/checkerboard-small.png', 0)
res = enhance_local(img_cb, 3, 0, 0.2, 0, 0.2, 10.0)
plot_img_orig(res)


# In[13]:

# read the image as a grayscale image (parameter 0)
img = cv2.imread('images/fruits-small.png', 0)
plot_img_orig(img)

# In[14]:
    
# padding size
b = 20

# In[15]:

# zero padding
img_zp = cv2.copyMakeBorder(img, b, b, b, b, cv2.BORDER_CONSTANT)
plot_img_orig(img_zp)

# In[16]:

# replication
img_rp = cv2.copyMakeBorder(img, b, b, b, b, cv2.BORDER_REPLICATE)
plot_img_orig(img_rp)

# In[17]:

# reflection
img_rf = cv2.copyMakeBorder(img, b, b, b, b, cv2.BORDER_REFLECT_101)
plot_img_orig(img_rf)

# In[18]:

# remove extra boundary from the zero padded image
rows, cols = img_zp.shape # image size
img_crop = img_zp[b:rows-b, b:cols-b] # last index is not included
plot_img_orig(img_crop)

# In[19]:

# mean filter given image corresponding to n x n mask (n must be odd)
def mean_filter(img, n):
    # compute offset / padding size
    b = int(n / 2)
    
    # zero padded image
    img_pad = cv2.copyMakeBorder(img, b, b, b, b, cv2.BORDER_CONSTANT)
    
    # size of padded image
    rows, cols = img_pad.shape
    
    # result image
    res = np.zeros(shape=[rows, cols], dtype=np.uint32) # note the data type (0 to 4294967295)
    
    # mean filtering
    for iy in range(b, rows-b):
        for jx in range(b, cols-b):
            # get local neighborhood
            nbh = img_pad[iy-b:iy+b+1, jx-b:jx+b+1]
            
            # compute sum and assign it to the current pixel
            res[iy, jx] = np.sum(nbh)
            
    # normalization (at the end because it is computationally expensive)
    res = res / (n*n)
    
    # remove extra border
    res = res[b:rows-b, b:cols-b]
    
    # return final result
    return res

# In[20]:

# read image as a grayscale image (parameter 0)
img = cv2.imread('images/p-building-small.png', 0)
plot_img_orig(img)

# In[21]:

# mean filter image
res_3_3 = mean_filter(img, 3); 
print("3x3"); 
plot_img_orig(res_3_3)

res_9_9 = mean_filter(img, 9); 
print("9x9"); 
plot_img_orig(res_9_9)

res_21_21 = mean_filter(img, 21); 
print("21x21"); 
plot_img_orig(res_21_21)

# In[22]:

# read image as a grayscale image (parameter 0)
img = cv2.imread('images/testpattern-512.png', 0)
plot_img_orig(img)

# In[23]:

# mean filter image
res_3_3 = mean_filter(img, 3); 
print("3x3"); 
plot_img_orig(res_3_3)

res_9_9 = mean_filter(img, 9); 
print("9x9"); 
plot_img_orig(res_9_9)

res_21_21 = mean_filter(img, 21); 
print("21x21"); 
plot_img_orig(res_21_21)


# In[24]:

# filter given image with given m x n mask
def filter_image(img, mask):
    # compute offset / padding size
    m, n = mask.shape # size of the mask (m x n = rows x cols)
    
    if (m % 2 == 0) or (n % 2 == 0):
        print("Mask must have odd size (returning original image)")
        return img # return unfiltered image

    bh = int(m / 2) # border height (rows)
    bw = int(n / 2) # border width (cols)

    # zero padding
    img_pad = cv2.copyMakeBorder(img, bh, bh, bw, bw, cv2.BORDER_CONSTANT) # top, bottom, left, right
    
    # size of padded image
    rows, cols = img_pad.shape
    
    # result image
    res = np.zeros(shape=[rows, cols], dtype=np.float64) # note the data type (0 to 4294967295)
    
    # filtering
    for iy in range(bh, rows-bh):
        for jx in range(bw, cols-bw):
            # get local neighborhood
            nbh = img_pad[iy-bh:iy+bh+1, jx-bw:jx+bw+1]
            
            # multiply and sum up
            tmp = np.multiply(mask, nbh)
            tmp = np.sum(tmp)
            
            # compute sum and assign it to the current pixel
            res[iy, jx] = tmp
            
    # normalization (at the end because it is computationally expensive)
    res = res / (m*n)
    
    # remove extra border
    res = res[bh:rows-bh, bw:cols-bw]
    
    # return final result
    return res

# In[25]:

# read the image as a grayscale image (parameter 0)
img = cv2.imread('images/testpattern-512.png', 0)
plot_img_orig(img)

# In[26]:

# specify box filter mask
mask = np.ones((9, 9))

# mean filter image
t1 = time.time() ##Starting time flag 
res = filter_image(img, mask)
t2 = time.time() ## Ending time flag
print(t1, t2)

# In[27]:

print("Time for normal filtering: " + str(t2-t1) + " seconds")
plot_img_orig(res)

# In[31]:

# check difference to previous task
res_diff = res-res_9_9
plot_img_orig(res_diff)
sum(sum(res_diff))

# In[33]:

# seperate the box filter
mask1 = np.ones((1, 9))
mask2 = np.ones((9, 1))

t1 = time.time()
res_m1 = filter_image(img, mask1)
res_m2 = filter_image(res_m1, mask2)
t2 = time.time()

print("Time for seperated filtering: " + str(t2-t1) + " seconds")
plot_img_orig(res_m2)

# check difference to previous task
res_diff = res_m2 - res_9_9
plot_img_orig(res_diff)

# In[34]:



