
# In[1]:
import numpy as np
# In[2]:
# initial dictionary
dict = np.array(['a', 'b', 'c'])

# create input 
input = np.array(['a', 'b', 'a', 'b', 'c'])

# empty code output
code = np.array([], dtype=np.uint8)

# check if passed seq(uence) is in dictionary and return index
def in_dict(seq):
    if seq in dict:
        return np.where(dict == seq)[0] # take 1st element [0] because result is tuple
    else:
        return 0

# process input
last_seq = input[0]
for i in range(1, input.size):
    seq = last_seq + input[i]
    
    # check if this sequence is in the dictionary
    if in_dict(seq) == False:
        dict = np.append(dict, seq)
        code = np.append(code, in_dict(last_seq))
        last_seq = input[i]
    else: # sequence has been found
        last_seq = seq
        
    # just print last element
    if i == input.size-1:
        code = np.append(code, in_dict(input[i]))
        
print("dict = " + str(dict))
print("code = " + str(code))


# In[5]:


# initial dictionary (arange can not be used to get a string representation)
dict = np.array([], dtype=object)
for i in range(256):
    dict = np.append(dict, str(i))

# read the image as a grayscale image (parameter 0)
img = cv2.imread('images/upb-logo.png', 0)
img_flat = img.copy().flatten()
    
# empty code output
code = np.array([], dtype=object)

# process input
last_seq = img_flat[0]
for i in range(1, img_flat.size):
    seq = str(last_seq) + "|" + str(img_flat[i])
    
    # check if this sequence is in the dictionary
    if in_dict(seq) == False:
        dict = np.append(dict, seq)
        code = np.append(code, in_dict(last_seq))
        last_seq = str(img_flat[i])
    else: # sequence has been found
        last_seq = seq
        
    # just print last element
    if i == input.size-1:
        code = np.append(code, in_dict(input[i]))

# compare the number of pixels and the size of the dictionary.
#np.set_printoptions(threshold=np.inf)
print("dict = " + str(dict))
print("code = " + str(code))

# comparison of pixels and code entries
print(img_flat.size)
print(dict.size)

# compute the compression ratio and relative data redundancy
cr = img_flat.size / code.size
rdr = 1-(1/cr)
print("Compression ratio: " + str(cr))
print("Relative data redundancy: " + str(rdr))


# In[ ]:




