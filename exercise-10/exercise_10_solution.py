import cv2
import numpy as np

# compute transfer function of ideal lowpass filter (ILPF) with cutoff frequency (radius) d0
def tf_ilpf(rows, cols, d0):
    # create empty image
    res = np.zeros(shape=[rows, cols], dtype=np.float64) # init with zeros

    # compute center coordinates
    cm = int(rows / 2)
    cn = int(cols / 2)
    
    # iterate trough image
    for u in range(rows):
        for v in range(cols):
            d = np.sqrt((u-cm)**2 + (v-cn)**2) # distance to the center
            
            if d <= d0:
                res[u, v] = 1

    # return result
    return res


# multiply given image by (-1)^(x+y) 
def center(img):
    # create empty image
    rows, cols = img.shape # image size
    res = np.zeros(shape=[rows, cols], dtype=np.float64) # init with zeros
    
    # iterate trough image
    for x in range(rows):
        for y in range(cols):
            res[x, y] = img[x, y] * (-1)**(x+y)

    # return result
    return res


# compute centered spatial representation h(x,y) of a given transfer function H(u,v)
def spatial_repr(img):
    # create empty image
    rows, cols = img.shape # image size
    res = np.zeros(shape=[rows, cols], dtype=np.float64) # init with zeros
    
    # multiply H(u,v) by (-1)^(u+v)
    res = center(img)
    
    # IDFT and real part
    res = np.fft.ifft2(res)
    res_re = np.real(res)  
    
    # multiply h(x,y) by (-1)^(x+y)
    res = center(res_re)
    
    # return result
    return res


# compute transfer function of Butterworth lowpass filter (BLPF) w/ cutoff frequency d0 and order n
def tf_blpf(rows, cols, d0, n):
    # create empty image
    res = np.zeros(shape=[rows, cols], dtype=np.float64) # init with zeros

    # compute center coordinates
    cm = int(rows / 2)
    cn = int(cols / 2)
    
    # iterate trough image
    for u in range(rows):
        for v in range(cols):
            d = np.sqrt((u-cm)**2 + (v-cn)**2) # distance to the center
            res[u, v] = 1 / (1 + (d/d0)**(2*n))

    # return result
    return res


# compute transfer function of Gaussian lowpass filter (BLPF) w/ cutoff frequency d0
def tf_glpf(rows, cols, d0):
    # create empty image
    res = np.zeros(shape=[rows, cols], dtype=np.float64) # init with zeros

    # compute center coordinates
    cm = int(rows / 2)
    cn = int(cols / 2)
    
    # iterate trough image
    for u in range(rows):
        for v in range(cols):
            d = np.sqrt((u-cm)**2 + (v-cn)**2) # distance to the center
            res[u, v] = np.exp(-d*d / (2*(d0**2)))

    # return result
    return res


# pad image with zeros
def zero_pad_img(img):
    rows, cols = img.shape # get image size
    res = cv2.copyMakeBorder(img, 0, rows, 0, cols, cv2.BORDER_CONSTANT) # top, bottom, left, right
    return res


# crop image
def crop_img(img):
    rows, cols = img.shape # get image size

    # compute center coordinates
    cm = int(rows / 2)
    cn = int(cols / 2)
    
    # crop and return image
    res = img[0:cm, 0:cn]
    return res


# filter image with given filter (image and filter must have the same size)
def filter_img(img, tf_filter):
    # DFT of image
    img_dft = np.fft.fft2(img) # compute DFT (no normalization to 1/MN)
    img_dft_shift = np.fft.fftshift(img_dft) # shift FFT to the center
    
    # filter the image
    img_filtered_uv = np.multiply(img_dft_shift, tf_filter)

    # inverse DFT (IDFT)
    img_dft_backshift = np.fft.ifftshift(img_filtered_uv) # shift centered FFT back to top left
    img_idft = np.fft.ifft2(img_dft_backshift) # compute IDFT
    img_back = np.real(img_idft) # take only real part, as all imaginary parts are parasitic
    
    return img_back
