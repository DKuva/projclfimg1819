import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
import csv


def get_images_and_labels(datadir,train_data,imtype=-1,bgr2rgb=False,resolution=(0,0),crop=False):
    '''
    Reads traffic sign data for German Traffic Sign Recognition Benchmark.
    Arguments: 
        datadir    -- path to the traffic sign data directory
        train_data -- is data for training
                      True  - train data
                      False - test data
        imtype     -- the way image should be read
                      1 - color image (BGR, not RGB)
                      0 - grayscale
                     -1 - channels as it is (default)
        bgr2rgb    -- if imtype is color image convert BGR to RGB order
                      boolean (default False)
        resolution -- scale all images to given resolution (w,h)
                      (0,0) - leave resolution as it is (default)
        crop       -- crop sign from image
                      boolean (default False)
    Returns:
	    list of images, list of corresponding labels
    '''
    images = []
    labels = []
    num_of_classes = 43 if train_data else 1
    for c in range(0,num_of_classes):
        # subdirectory for class
        dir_name = format(c,'05d') if train_data else ''
        csv_name = 'GT-'+((format(c,'05d')) if train_data else 'final_test') +'.csv'
        prefix = os.path.join(datadir,dir_name) 
        with open(os.path.join(prefix,csv_name)) as csv_file:
            gt_reader = csv.reader(csv_file, delimiter=';')
            # skip csv header
            next(gt_reader)
            # loop over all images in current annotations file
            for row in gt_reader:
                # the 1th column is the filename
                img = cv2.imread(os.path.join(prefix,row[0]),imtype);
                # do operations on image if necessary
                if crop:
                    x1,y1 = int(row[3]),int(row[4])
                    x2,y2 = int(row[5]),int(row[6])
                    img = img[y1:y2,x1:x2]
                if imtype!=0 and bgr2rgb:
                    #b,g,r = cv2.slice(img)
                    #img = cv2.merge((r,g,b))
                    img = img[:,:,::-1]
                if resolution != (0,0):
                    # resize by liner interpolation method
                    img = cv2.resize(img,resolution)
                images.append(img) 
                # the 8th column is the label
                labels.append(row[7]) 
            if c==0:
                break
    return images, labels


  
train_data = True
datadir="../data/train_images"
imtype=-1
bgr2rgb=True
resolution=(128,128)
crop=True


t,l = get_images_and_labels(datadir,train_data,imtype,bgr2rgb,resolution,crop)


print(len(l), len(t),l[2])
plt.imshow(t[50],cmap='gray')
plt.show()


for img in t:
    print(str(imgCount))
    #imgAnal.analyzeImg(img)
    brute_force(t[0],img)
    imgCount += 1



