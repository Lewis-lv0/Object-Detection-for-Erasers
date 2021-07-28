'''
Author: Yixing
Date: 2021-07-16 11:38:46
Software: VS Code
'''

'''
utility functions for managing dataset
'''

import os
import shutil
import cv2
from PIL import Image


##########################################
# add more images to the dataset
# src_path: source folder
# dst_path: path of the dataset
##########################################
def add_to_dataset(src_path, dst_path):
    # current number of images in the dataset
    file_count = len(os.listdir(dst_path))
    print('There are already %d files in this folder\nAdding more files...'%file_count)
    for f in os.listdir(src_path):
        # extract all image files
        if os.path.isfile(f) and f.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
            new_name = str(file_count).zfill(5)
            new_fname = new_name + '.jpg'
            file_count += 1
            current_fpath = os.path.join(src_path, f)
            new_fpath = os.path.join(dst_path, new_fname)
            shutil.move(current_fpath, new_fpath)
    print('Adding successfully!\nThere are %d files in this folder\n'%file_count)



###########################################
# format the file name of all images
###########################################
def manage_dataset(dst_path):
    print('There are %d files in this folder'%len(os.listdir(dst_path)))
    print('Starting managing the dataset...')
    f_index = 0
    flist = os.listdir(dst_path)
    flist.sort(key= lambda x:int(x[:-4]))
    for filename in flist:
        new_name = str(f_index).zfill(5)
        f_index += 1
        new_fname = new_name + '.jpg'
        os.rename(os.path.join(dst_path, filename), os.path.join(dst_path, new_fname))
    print('Finish managing the dataset')


##########################################
# labelme cannot handle rgba images
# convert rgba to rgb
##########################################
def rgba2rgb(dst_path):
    count = 0 # #rgba images
    flist = os.listdir(dst_path)
    for f in flist:
        img_path = os.path.join(dst_path, f)
        img = Image.open(img_path)
        img_md = img.mode
        if img_md.lower() == 'rgba':
            count+=1
            img = img.convert('RGB')
            img.save(img_path)
        elif img_md.lower() == 'rgb':
            pass # do nothing

        else:
            raise IOError("Please double check the image format!")
        img.close()

    print('There are %d RGBA images\n%d RGBA images have been converted to RGB'%(count, count))
    manage_dataset(dst_path)


# main
if __name__ == '__main__':
    rgba2rgb(r'dataset\raw imgs')
    



