# -*- coding: UTF-8 -*-

import os
import os.path
from PIL import Image
from svmutil import *
import threading
model_dir = r'C:\Users\digge\Desktop\model'
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
def image_to_data(img):
    label = 318
    SN = 0
    pixel = img.load()
    data_dict = {}
    point = 0
    for  x in range(img.size[0]):
            point_x = 0
            for y in range(img.size[1]):
                if pixel[x,y] < 127:
                    point = point+1
                    point_x = point_x+1
            SN = SN+1
            data_dict[SN] = point_x
    #计算每一行的点数
    for  y in range(img.size[1]):
        point_y = 0
        for x in range(img.size[0]):
            if pixel[x,y] < 127:
                point_y = point_y+1
        SN = SN+1
        data_dict[SN] = point_y
    #总点数 
    SN = SN+1
    data_dict[SN] = point
    return [318],[data_dict]

def hyper_classifer(model_dict,train_data):
    score = [0]*256
    tlabel = train_data[0]
    tdata = train_data[1]
    for model_name in model_dict:
        p_label,p_acc, p_val = svm_predict(tlabel,tdata,model_dict[model_name],'-q')
        if int(p_label[0]) == 0:
            score[int(model_name.split('_')[0])] += 1
        if int(p_label[0]) == 1:
            score[int(model_name.split('_')[1])] += 1
    return chr(score.index(max(score)))

def Auto_CHPTCHA(org_validate_img, model_dict):
    files = os.listdir(model_dir)
    img = Image.open(org_validate_img)
    img = binaryzation(img)
    img_list = split_image(img)
    validate_code = ''
    for i in xrange(4):
        validate_code = validate_code + hyper_classifer(model_dict,image_to_data(img_list[i]))
    return validate_code


    
