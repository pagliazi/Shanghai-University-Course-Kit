# -*- coding: UTF-8 -*-

import os
import os.path
from PIL import Image
from svmutil import *


org_validate_img = r'C:\Users\digge\Desktop\validate code\test.jpg'
model_dir = r'C:\Users\digge\Desktop\model'
data_dir = 'C:\\Users\\digge\\Desktop\\validate code\\'

def check(img,x,y):
    if (x < 0 or y < 0 or x > img.size[0] - 1 or y > img.size[1] - 1):
        return True
    if img.getpixel((x,y)) == 0:
        return False
    return True

def binaryzation(img):
    img_bin = img.convert("L")
    threshold = 60
    for x in range(img_bin.size[0]):
        for y in range(img_bin.size[1]):
            if img_bin.getpixel((x,y)) > threshold:
                img_bin.putpixel((x,y),255)
            else:
                img_bin.putpixel((x,y),0)
    for x in range(img_bin.size[0]):
        for y in range(img_bin.size[1]):
            if check(img_bin,x-1,y) and check(img_bin,x-1,y-1) and check(img_bin,x,y+1) and check(img_bin,x+1,y-1) and check(img_bin,x+1,y) and check(img_bin,x+1,y+1)  and check(img_bin,x,y+1) and check(img_bin,x-1,y+1):
                img_bin.putpixel((x,y),255)
    return img_bin

def split_image(img):
    box_0 = (0,0,16,22)
    box_1 = (14,0,30,22)
    box_2 = (29,0,45,22)
    box_3 = (43,0,59,22)
    box = [box_0,box_1,box_2,box_3]
    image_list = []

    for i in range(4):
        image_list.append(img.crop(box[i]))
    return image_list
def image_to_data(img,data_file):
    label = 318
    SN = 0
    pixel = img.load()
    data_file.write(str(label)+' ')
    point = 0
    for  x in range(img.size[0]):
            point_x = 0
            for y in range(img.size[1]):
                if pixel[x,y] < 127:
                    point = point+1
                    point_x = point_x+1
            SN = SN+1
            data_file.write(str(SN)+':')
            data_file.write(str(point_x)+' ')
    #计算每一行的点数
    for  y in range(img.size[1]):
        point_y = 0
        for x in range(img.size[0]):
            if pixel[x,y] < 127:
                point_y = point_y+1
        SN = SN+1
        data_file.write(str(SN)+':')
        data_file.write(str(point_y)+' ')
    #总点数 
    SN = SN+1
    data_file.write(str(SN)+':')
    data_file.write(str(point))
    data_file.write("\n")
    data_file.close()
    return None

def hyper_classifer(model_dir,data_file):
    files = os.listdir(model_dir)
    os.chdir(model_dir)
    tlabel,tdata = svm_read_problem(data_file)
    score = [0]*256
    for file in files:
        model = svm_load_model(file)
        p_label,p_acc, p_val = svm_predict(tlabel,tdata,model,'-q')
        if int(p_label[0]) == 0:
            score[int(str(file).strip('.model').split('_')[0])] += 1
        if int(p_label[0]) == 1:
            score[int(str(file).strip('.model').split('_')[1])] += 1
    os.remove(data_file)
    return chr(score.index(max(score)))

img = Image.open(org_validate_img)
img = binaryzation(img)
img_list = split_image(img)
for i in range(4):
    data_file = data_dir + str(i)
    image_to_data(img_list[i],open(data_file,'w'))
    print hyper_classifer(model_dir,data_file),
