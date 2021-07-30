'''
Reference: https://www.jianshu.com/p/574755718e51

Revised by Yixing:
1. modify functions for my preferences
2. fix bugs in imageAugment_flip() and showLabelFromTxt()
3. add comments

#####################################
Many utility function:
managing dataset (visualization etc.)
data augmentation
#####################################
'''


import os
import numpy as np
import cv2
import shutil
import json
import random

'''
Image augmentation for yolov5
'''
class yolo_tool():
    def __init__(self, help_=False):
        if help_:
            self.getHelp()
    
    ###################################################################
    # managing dataset
    ###################################################################
    '''
    get all image paths in a folder
    '''
    def getAllImagePath(self, folder, recursion=False):
        expandName = ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG", "bmp", "BMP"]
        imagePathList = []
        if not recursion:
            for item in os.listdir(folder):
                # make sure it is a file, not a dir
                if os.path.isdir(os.path.join(folder, item)):
                    continue
                if item.rsplit(".",1)[-1] in expandName:
                    imagePathList.append(os.path.join(folder, item))
            return imagePathList
        else:
            for item in os.listdir(folder):
                if os.path.isdir(os.path.join(folder, item)):
                    subPathList = self.getAllImagePath(os.path.join(folder, item), True)
                    imagePathList.extend(item for item in subPathList)
                else:
                    if item.rsplit(".",1)[-1] in expandName:
                        imagePathList.append(os.path.join(folder, item))
            return imagePathList

    '''
    get all json paths in a folder
    '''
    def getAllJsonFilePath(self, folder):
        jsonPathList = []
        for item in os.listdir(folder):
            if item.rsplit(".",1)[-1] == 'json':
                jsonPathList.append(os.path.join(folder, item))
        return jsonPathList

    '''
    get all txt paths in a folder
    '''
    def getAllTxtPath(self, folder):
        txtPathList = []
        for item in os.listdir(folder):
            if item.rsplit(".",1)[-1] == 'txt':
                txtPathList.append(os.path.join(folder, item))
        return txtPathList

    '''
    use json file to look for corresponding images
    @param jsonPathList: path list of all json files
    @param imageFolder: folder of images
    '''
    def fromJsonFileToSearchImage(self, jsonPathList, imageFolder):
        imagePathList = []
        for item in jsonPathList:
            with open(item, "r", encoding='utf-8') as f:
                jsonData = json.load(f)
                imageName = jsonData["imagePath"].rsplit("\\",1)[-1]
            # jsonName = item.rsplit("\\",1)[-1]
            imagePath = os.path.join(imageFolder, imageName)
            # print(imagePath)
            imagePathList.append(imagePath)
        return imagePathList

    '''
    Copy all labeled Image to new folder
    '''
    def copyAllLabeledImageToNewFolder(self, imagePathList, saveFolder):
        for item in imagePathList:
            imageName = item.rsplit("\\",1)[-1]
            savePath = os.path.join(saveFolder, imageName)
            print("copyAllLabeledImageToNewFolder: srcPath", item)
            print("copyAllLabeledImageToNewFolder: dstPath", savePath)
            shutil.copyfile(item, savePath)


    '''
    rename all raw images and txt annotations
    '''
    def renameAllLabeledImageAndTxt(self, txtFolder, labeledImageFolder,  n=5, startN=0):
        ''' 
        extendName是图像后缀名，n用于zfill(n)
        e.g. n = 5 -> 00001, 00002....
        '''
        i = startN
        imagePathList = self.getAllImagePath(labeledImageFolder)
        for imagePath in imagePathList:
            imageName_dst = str(i).zfill(n) + "." + imagePath.rsplit(".",1)[-1]
            image_srcPath = imagePath
            image_dstPath = os.path.join(labeledImageFolder, imageName_dst)
            txtName_src = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] +".txt"
            txtName_dst = str(i).zfill(n) + ".txt"
            txt_srcPath = os.path.join(txtFolder, txtName_src)
            txt_dstPath = os.path.join(txtFolder, txtName_dst)
            i += 1
            try:
                if not os.path.exists(image_dstPath):
                    os.rename(image_srcPath, image_dstPath)
                if not os.path.exists(txt_dstPath):
                    os.rename(txt_srcPath, txt_dstPath)
                print("renameAllLabeledImageAndTxt")
                print("image_srcPath:", image_srcPath)
                print("image_dstPath:", image_dstPath)
                print("txt_srcPath:", txt_srcPath)
                print("txt_dstPath:", txt_dstPath)
            except:
                print("ERROR:renameAllLabeledImageAndTxt error")
                print("image_srcPath:", image_srcPath)
                print("image_dstPath:", image_dstPath)
                print("txt_srcPath:", txt_srcPath)
                print("txt_dstPath:", txt_dstPath)

    '''
    Annotation
    convert from json to txt
    '''
    def changeLabelFromJsonToTxt(self, jsonPath, txtSaveFolder):
        with open(jsonPath, "r", encoding='utf-8') as f:
            jsonData = json.load(f)
            img_h = jsonData["imageHeight"]
            img_w = jsonData["imageWidth"]
            txtName = jsonPath.rsplit("\\",1)[-1].rsplit(".",1)[0] + ".txt"
            txtPath = os.path.join(txtSaveFolder, txtName)
            with open(txtPath, "w") as f:
                for item in jsonData["shapes"]:
                    label = item["label"]
                    pt1 = item["points"][0]
                    pt2 = item["points"][1]
                    xCenter = (pt1[0] + pt2[0]) / 2
                    yCenter = (pt1[1] + pt2[1]) / 2
                    obj_h = pt2[1] - pt1[1]
                    obj_w = pt2[0] - pt1[0]
                    f.write(" {} ".format(label))
                    f.write(" {} ".format(xCenter / img_w))
                    f.write(" {} ".format(yCenter / img_h))
                    f.write(" {} ".format(obj_w / img_w))
                    f.write(" {} ".format(obj_h / img_h))
                    f.write(" \n")

    '''
    display images with their labels (json)
    '''
    def showLabelFromJson(self, jsonPath, imageFolder):
        cv2.namedWindow("img", 0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        with open(jsonPath, "r") as f:
            jsonData = json.load(f)
            imageName = jsonData["imagePath"].rsplit("\\",1)[-1]
            imagePath = os.path.join(imageFolder, imageName)
            img = cv2.imread(imagePath)
            print("showLabelFromJson: image path:", imagePath)
            for item in jsonData["shapes"]:
                label = item["label"]
                p1 = (int(item["points"][0][0]), int(item["points"][0][1]))
                p2 = (int(item["points"][1][0]), int(item["points"][1][1]))
                cv2.putText(img, label, (p1[0], p1[1] - 10), font, 1.2, (0, 0, 255), 2)
                cv2.rectangle(img, p1, p2, (0, 255, 0), 2)
                cv2.imshow("img", img)
            cv2.waitKey(0)
            cv2.destroyWindow("img")

    '''
    display images with their labels (txt)
    '''
    def showLabelFromTxt(self, imagePath, txtFolder):
        # label xcenter ycenter w h
        txtName = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + ".txt"
        txtPath = os.path.join(txtFolder, txtName)
        print("showLabelFromTxt: image path:", imagePath)
        img = cv2.imread(imagePath)
        h, w = img.shape[:2]
        cv2.namedWindow("img", 0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        with open(txtPath, "r") as f:
            lines = f.readlines()
            for line in lines:
                tempL = line.split()
                label = tempL[0]
                obj_w = float(tempL[3])
                obj_h = float(tempL[4])
                topLeftx = (float(tempL[1]) - obj_w / 2) * w
                topLefty = (float(tempL[2]) - obj_h / 2) * h
                bottomRightx = (float(tempL[1]) + obj_w / 2) * w
                bottomRighty = (float(tempL[2]) + obj_h / 2) * h
                p1 = (int(topLeftx), int(topLefty))
                p2 = (int(bottomRightx), int(bottomRighty))
                cv2.putText(img, label, (p1[0], p1[1] - 10), font, 1.2, (0, 255, 255), 2)
                cv2.rectangle(img, p1, p2, (0, 255, 0), 2)
                cv2.imshow("img", img)
            cv2.waitKey(0)
            cv2.destroyWindow("img")




    ######################################################
    # data augmentation util functions
    ######################################################

    '''
    image blur
    '''
    def imageAugment_smooth(self, imagePath, txtFolder, labeledImageFolder,n=5):
        txtName = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + ".txt"
        txtPath = os.path.join(txtFolder, txtName)
        print("smooth: image path:", imagePath)
        img = cv2.imread(imagePath)
        # 新路径名：在原图路径名后面加上_smooth
        imageName_smooth = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_smooth." + imagePath.rsplit(".",1)[-1]
        imagePath_smooth = os.path.join(labeledImageFolder, imageName_smooth)#平滑图像保存路径
        txtName_smooth = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_smooth.txt"
        txtPath_smooth = os.path.join(txtFolder, txtName_smooth)#标签保存路径
        shutil.copyfile(txtPath, txtPath_smooth) # blur后，矩形框坐标不变
        print("imageAugment_smooth: source txtPath", txtPath)
        print("imageAugment_smooth: dst txtPath", txtPath_smooth)
        print("imageAugment_smooth: source imagePath", imagePath)
        print("imageAugment_smooth: dst imagePath", imagePath_smooth)
        dst = cv2.blur(img, (n, n))
        cv2.imwrite(imagePath_smooth, dst)
        print('--------------------------------')


    '''
    flip images

    Usage:
    flag = 0    水平翻转 
    flag = 1    竖直翻转, 
    flag = 2  水平翻转+竖直翻转
    '''
    def imageAugment_flip(self, imagePath, txtFolder, labeledImageFolder,flag=0):
        txtName = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + ".txt"
        txtPath = os.path.join(txtFolder, txtName)
        print("imageAugment_flip: image path:", imagePath)
        img = cv2.imread(imagePath)
        # 水平翻转
        if flag == 0:
            imageName_flip = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + "_flipx." + imagePath.rsplit("\\",1)[-1].rsplit(".",1)[-1]
            imagePath_flip = os.path.join(labeledImageFolder, imageName_flip)
            txtName_flip = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_flipx.txt"
            txtPath_flip = os.path.join(txtPath.rsplit("\\",1)[0:-1][0], txtName_flip)
        # 竖直翻转
        elif flag == 1:
            imageName_flip = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + "_flipy." + imagePath.rsplit("\\",1)[-1].rsplit(".",1)[-1]
            imagePath_flip = os.path.join(labeledImageFolder, imageName_flip)
            txtName_flip = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_flipy.txt"
            txtPath_flip = os.path.join(txtPath.rsplit("\\",1)[0:-1][0], txtName_flip)
        # 水平+竖直翻转
        elif flag == 2:
            imageName_flip = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + "_flipxy." + imagePath.rsplit("\\",1)[-1].rsplit(".",1)[-1]
            imagePath_flip = os.path.join(labeledImageFolder, imageName_flip)
            txtName_flip = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_flipxy.txt"
            txtPath_flip = os.path.join(txtPath.rsplit("\\",1)[0:-1][0], txtName_flip)

        # 打开原来的txt标签文件，修改坐标信息，并保存
        with open(txtPath, "r") as fsrc:
            with open(txtPath_flip, "w") as f:
                lines = fsrc.readlines()
                for line in lines:
                    temp = line.split()
                    # info about the rectangle label
                    label, xcenter, ycenter, objw, objh = temp[0], temp[1], temp[2], temp[3], temp[4]
                    if flag == 0:
                        xcenter = 1 - float(xcenter)
                    elif flag == 1:
                        ycenter = 1 - float(ycenter)
                    elif flag == 2:
                        xcenter = 1 - float(xcenter)
                        ycenter = 1 - float(ycenter)
                    f.write(" {} ".format(label))
                    f.write(" {} ".format(xcenter))
                    f.write(" {} ".format(ycenter))
                    f.write(" {} ".format(objw))
                    f.write(" {} ".format(objh))
                    f.write(" \n")
        if flag == 0:
            dst = cv2.flip(img, 1)
        elif flag == 1:
            dst = cv2.flip(img, 0)
        elif flag == 2:
            dst = cv2.flip(img, 1)
            dst = cv2.flip(dst, 0)
        cv2.imwrite(imagePath_flip, dst)
        print('Finishing writing file\n-----------------------------------------------')


    '''
    gamma transformation
    改变亮度信息
    '''
    def imageAugment_gamma(self, imagePath, txtFolder, labeledImageFolder,gamma=2):
        txtName = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + ".txt"
        txtPath = os.path.join(txtFolder, txtName)
        print("imageAugment_gamma: image path:", imagePath)
        img = cv2.imread(imagePath)
        imageName_gamma = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + "_gamma{}.".format(gamma) + imagePath.rsplit("\\",1)[-1].rsplit(".",1)[-1]
        imagePath_gamma = os.path.join(labeledImageFolder, imageName_gamma)
        txtName_gamma = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_gamma{}.txt".format(gamma)
        txtPath_gamma = os.path.join(txtPath.rsplit("\\",1)[0:-1][0], txtName_gamma)
        shutil.copyfile(txtPath, txtPath_gamma)
        print("source txtPath", txtPath)
        print("dst txtPath", txtPath_gamma)
        print("source imagePath", imagePath)
        print("dst imagePath", imagePath_gamma)
        table = []
        for i in range(256):
            table.append(((i / 255.0) ** gamma) * 255)
        table = np.array(table).astype("uint8")
        dst = cv2.LUT(img, table)
        cv2.imwrite(imagePath_gamma, dst)

    '''
    train-test divide
    '''
    def devideTrainSetAndTestSet(self, imagePathList, saveFolder, prePath="", prop=0.8):
        # paths to train and test images
        trainTxt = saveFolder + "/train.txt"
        testTxt = saveFolder + "/test.txt"
        with open(trainTxt, "w") as ftrain:
            with open(testTxt, "w") as ftest:
                for item in imagePathList:
                    imagePath = prePath + item.rsplit("\\",1)[-1]
                    if random.random() < prop:
                        ftrain.write(imagePath)
                        ftrain.write("\n")
                    else:
                        ftest.write(imagePath)
                        ftest.write("\n")

    def getHelp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Function:\t ")
        print("parameter：")
        print("\t _\t \t _")
        print("return:")
        print("\t _\t \t _")
        print("================================================================================\n")

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Function:\t getAllImagePath(folder,recursion=False)")
        print("parameter：")
        print("\t folder:\t \t search path")
        print(
            "\t recursion = False:\t \t default parameters,if recursion = True it will  recursively search the folder")
        print("return:")
        print("\t imagePathLIst\t \t  image file path list")
        print("================================================================================\n")

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Function:\t getAllJsonPath(self,folder)")
        print("parameter：")
        print("\t folder\t \t folde rcontains json file ")
        print("return:")
        print("\t jsonPathLIst\t \t  json file path list")
        print("================================================================================\n")

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Function:\t fromJsonFileToSearchImage(jsonPathList,imageFolder,extendName = '.jpg')")
        print("parameter：")
        print("\t jsonPathList \t \t jsonPathList")
        print("\t imageFolder\t \t 存放图片的文件夹")
        print("\t extendName\t \t 图片扩展名")
        print("return:")
        print("\t imagePathList\t \t 标注过的图片的路径")
        print("================================================================================\n")

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Function:\t changeLabelFromJsonToTxt(self,jsonPath,txtSaveFolder)")
        print("txt文件内的保存模式为：label xcenter ycenter width height,坐标全是相对坐标")
        print("parameter：")
        print("\t jsonPath:\t \t json file path")
        print("\t txtSaveFolder\t \t txt file save folder")
        print("return:")
        print("\t None\t \t ")
        print("================================================================================\n")
