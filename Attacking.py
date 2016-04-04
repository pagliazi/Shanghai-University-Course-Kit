#coding:utf-8

import random
import time
import urllib
import urllib2
import zlib
import winsound
import cookielib
import os
import re
import webbrowser
n=0
url='http://xk.shu.edu.cn:8080/CourseSelectionStudent/CtrlViewQueryCourseCheck'
StudentNum='123456'
WithdCourse='01014127'
WithdCourse_tnum='1014'
CourseNum1='01014127'
CourseTNum1='1014'
CourseNum2=''
CourseTNum2=''
def readsession():
    cookie=open('cookie.txt').read()
    pattern= re.compile('ASP.NET_SessionId=(........................);*?')
    return re.search(pattern,cookie).group(1)
SessionId = readsession()
def tuike():
    Tuikeurl ='http://xk.shu.edu.cn:8080/CourseReturnStudent/CtrlViewOperationResult'
    headers = {'Origin': 'http://xk.shu.edu.cn:8080', 'Content-Length': '59', 'Accept-Language': 'zh-CN,zh;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'X-Requested-With': 'XMLHttpRequest', 'Host': 'xk.shu.edu.cn', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2552.0 Safari/537.36', 'Connection': 'keep-alive', 'Cookie': '_ga=GA1.3.548295607.1450860734; Hm_lvt_444bf10f6d7469654b7f41f9f9f9c301=1449989162,1449989164,1451806133,1452091199; ASP.NET_SessionId=' +SessionId , 'Referer': 'http://xk.shu.edu.cn:8080/CourseSelectionStudent/FuzzyQuery', 'Content-Type': 'application/x-www-form-urlencoded'}
    data2='ListCourseStr='+WithdCourse+'%7C'+WithdCourse_tnum+'&StuNo='+StudentNum+'&Absolute=false'
    request=urllib2.Request(Tuikeurl,data2,headers)
    response = urllib2.urlopen(request)
    res=response.read()
    res=zlib.decompress(res,zlib.MAX_WBITS|32)
    pat=('退课成功')
    tuires=re.search(pat,res)
    mat2= re.search('失败',res)

    if tuires!= None :
        print( 'Success')
    elif mat2 != None :
        print ('\n退课失败！')
        winsound.PlaySound('1.wav',winsound.SND_ASYNC)
    else :
        print (res)
        print ('似乎除了点问题')
        winsound.PlaySound('1.wav',winsound.SND_LOOP)
def bang():
    global url
    global SessionId
    headers = {'Origin': 'http://xk.shu.edu.cn:8080', 'Content-Length': '206', 'Accept-Language': 'zh-CN,zh;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'X-Requested-With': 'XMLHttpRequest', 'Host': 'xk.shu.edu.cn', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2552.0 Safari/537.36', 'Connection': 'keep-alive', 'Cookie': '_ga=GA1.3.548295607.1450860734; Hm_lvt_444bf10f6d7469654b7f41f9f9f9c301=1449989162,1449989164,1451806133,1452091199; ASP.NET_SessionId=' +SessionId , 'Referer': 'http://xk.shu.edu.cn:8080/CourseSelectionStudent/FuzzyQuery', 'Content-Type': 'application/x-www-form-urlencoded'}
    data= {'stuNo': StudentNum, 'IgnorCourseGroup': 'false', 'ListCourseStr': CourseNum1+'|'+CourseTNum1+'|0', 'IgnorClassMark': 'false', 'IgnorCredit': 'false'}
    data2='CourseNo=&CourseName=&TeachNo=&TeachName=%E9%BB%84%E5%B9%B3%E4%BA%AE&CourseTime=&NotFull=false&Credit=&Campus=0&Enrolls=&DataCount=100&MinCapacity=&MaxCapacity=&PageIndex=1&PageSize=8&FunctionString=InitPage'
    request=urllib2.Request(url,data2,headers)
    response = urllib2.urlopen(request)
    res=response.read()
    res=zlib.decompress(res,zlib.MAX_WBITS|32)
    pat = re.compile('114')#这里还是根据需要改一下
    susmat = re.search(pat,res)
    errmat = re.search('115',res)
    errmat2 = re.search('异常',res)
    contmat= re.search ('已满',res)
    havemat=re.search('已选',res)
    if susmat != None :
       print('找到114')
       return True
    elif errmat != None:
        #print '当前'+errmat.group(0) +'人'
        return False
    else :
        print ('选课系统似乎不在状态')
        print res
url2='http://xk.shu.edu.cn:8080/CourseSelectionStudent/CtrlViewOperationResult'

def bang2():
    global url2
    global SessionId
    headers = {'Origin': 'http://xk.shu.edu.cn:8080', 'Content-Length': '110', 'Accept-Language': 'zh-CN,zh;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'X-Requested-With': 'XMLHttpRequest', 'Host': 'xk.shu.edu.cn', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2552.0 Safari/537.36', 'Connection': 'keep-alive', 'Cookie': '_ga=GA1.3.548295607.1450860734; Hm_lvt_444bf10f6d7469654b7f41f9f9f9c301=1449989162,1449989164,1451806133,1452091199; ASP.NET_SessionId=' +SessionId , 'Referer': 'http://xk.shu.edu.cn:8080/CourseSelectionStudent/FuzzyQuery', 'Content-Type': 'application/x-www-form-urlencoded'}
    data= {'stuNo': StudentNum, 'IgnorCourseGroup': 'false', 'ListCourseStr': CourseNum1+'|'+CourseTNum1+'|0', 'IgnorClassMark': 'false', 'IgnorCredit': 'false'}
    data2='ListCourseStr='+CourseNum2+'%7C'+CourseTnum2+'%7C0&stuNo='+StudentNum+'&IgnorClassMark=false&IgnorCourseGroup=false&IgnorCredit=false'
    request=urllib2.Request(url2,data2,headers)
    response = urllib2.urlopen(request)
    res=response.read()
    res=zlib.decompress(res,zlib.MAX_WBITS|32)
    susmat = re.search('成功',res)
    errmat = re.search('请输入',res)
    errmat2 = re.search('异常',res)
    contmat= re.search ('已满',res)
    havemat=re.search('已选',res)
    if susmat!= None :
        print('成功选课')
        return True
    elif errmat !=None :
        print('异常！')
        return True
    elif errmat2 != None:
        print ('异常出现拉，赶紧来看看！！')
        return True
    elif havemat!= None :
        print ('已经选上拉')
        return True
    elif contmat != None :
        print ('选课进行中...')
        return False
    else :
        print ('出事拉！啥都没找到！')
        return True
while True :
    ret = bang()
    n += 1
    t=random.uniform(3,4)
    if ret :
        winsound.PlaySound('1.wav',winsound.SND_ASYNC)
        tuike()
        while True :
            ret=bang2()
            time.sleep(t/2)
            #print n
            time.sleep(t/2)
            if ret :
                break
        break
    time.sleep(t/2)
    #print n
    time.sleep(t/2)
