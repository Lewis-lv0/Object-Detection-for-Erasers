'''
Author: Yixing
Date: 2021-07-20 14:25:23
'''

'''
test bug
'''
with open(r'dataset\annotation_yolo\00031.txt') as f:
    lines = f.readlines()
    for line in lines:
        temp = line.split(' ')
        label, xcenter, ycenter, objw, objh = temp[0], temp[1], temp[2], temp[3], temp[4]
        print(label, xcenter, ycenter, objw, objh)