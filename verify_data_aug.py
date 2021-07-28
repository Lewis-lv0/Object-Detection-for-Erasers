'''
Author: Yixing
Date: 2021-07-28 10:04:45
'''

'''
verify data augmentation (by visualization)
'''
import shutil
import os
from yolo_tool import yolo_tool

tool = yolo_tool()

labeledImageFolder = r"dataset\raw imgs"# 筛选出所有标注过的图片
txtFolder = r"dataset\annotation_yolo"# txt文件保存的路径

#检查转换的最终结果
dstLabeledImagePathList = tool.getAllImagePath(labeledImageFolder)
for imagePath in dstLabeledImagePathList:
    tool.showLabelFromTxt(imagePath,txtFolder)
