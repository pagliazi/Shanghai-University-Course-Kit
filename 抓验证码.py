# -*- coding:UTF-8 -*-
'''
Script Name     : downLoadImage.py
Author          : svoid
Created         : 2015-03-14
Last Modified   : 
Version         : 1.0
Modifications   : 
Description     : 网站爬取图片
'''

import requests
import threading
import time

"""
Description    : 将网页图片保存本地
@param imgUrl  : 待保存图片URL
@param imgName : 待保存图片名称
@return 无
"""
def saveImage( imgUrl,imgName ="default.jpg" ):
    response = requests.get(imgUrl, stream=True)
    image = response.content
    DstDir="D:\\chap\\"
    print("Save Validateimg to"+DstDir+imgName+"\n")
    try:
        with open(DstDir+imgName ,"wb") as jpg:
            jpg.write( image)     
            return
    except IOError:
        print("IO Error\n")
        return
    finally:
        jpg.close        
for i in range(0,14776336):
    saveImage('http://xk.autoisp.shu.edu.cn/Login/GetValidateCode?%20%20+%20GetTimestamp()',str(i)+'.jpg')
