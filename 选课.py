# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import re
import time
import webbrowser
import zlib
from Auto_CHPTCHA import *

class sim_client:
    def __init__(self, username, password, model_dict):
        self.model_dict = model_dict
        self.TxtUsername = username
        self.TxtPassword = password
        self.IndexUrl = 'http://xk.autoisp.shu.edu.cn/'
        self.CodeUrl = 'http://xk.autoisp.shu.edu.cn/Login/GetValidateCode?%20%20+%20GetTimestamp()'
        self.IndexBody = {'txtUserName':self.TxtUsername,'txtPassword':self.TxtPassword}
        self.cookie = cookielib.LWPCookieJar()
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookieHandler, urllib2.HTTPHandler)
    def run(self):
        self.opener.open(self.IndexUrl)
        temp_file = open('temp_code.jpg', 'wb')
        temp_file.write(self.opener.open(self.CodeUrl).read())
        temp_file.close()
        validate_code = Auto_CHPTCHA('temp_code.jpg',model_dict)
        self.IndexBody['txtValiCode'] = str(validate_code)
        content = self.login()
        return content
    def login(self):
        Indexbody = urllib.urlencode(self.IndexBody)
        request = urllib2.Request(self.IndexUrl,Indexbody)
        response = self.opener.open(request)
        content = response.read()
        return content
    
def client_login(username, password , model_dcit):
    client = sim_client(username, password, model_dict)
    content = client.run()
    while content.find('Validate') != -1:
        content = client.run()
    return client
#for course inquire, the parameter is class name. for course selection,it's the list of class
def request_constructor(username, request_type, parameter):
    query_url = 'http://xk.autoisp.shu.edu.cn/StudentQuery/CtrlViewQueryCourse'
    select_url = 'http://xk.autoisp.shu.edu.cn/CourseSelectionStudent/CtrlViewOperationResult'
    if request_type == 'query_course':
        raw_data_sheet = 'CourseName=%' + urllib.quote(parameter) + '&'
        access_url = query_url
    if request_type == 'select_course':
        raw_data_sheet = 'IgnorClassMark=False&IgnorCourseGroup=False&IgnorCredit=False&StudentNo=' + username + '&'
        for i in range(len(parameter)):
            raw_data_sheet = raw_data_sheet + 'ListCourse%5B' + str(i) + '%5D.CID=' + parameter[i]['classid'] + '&ListCourse%5B' + str(i) + '%5D.TNo=' + parameter[i]['teacherid'] + '&'
        access_url = select_url
    return urllib2.Request(access_url,raw_data_sheet)

def course_attack(username, password, model_dcit, class_list, idle_time = 2, reset_time = 50):
    client = client_login(username, password, model_dict)
    request = request_constructor(username, 'select_course', class_list)
    vain = client.opener.open('http://xk.autoisp.shu.edu.cn/CourseSelectionStudent/FastInput')
    flag = True
    embark = time.time()
    while flag:
        reponse = client.opener.open(request).read()
        if len(re.findall('已选此课程', reponse)) == len(class_list):
            print 'check'
            flag = True
        #if len(re.findall('已选此课程', reponse)) != 0:
            #vain = client.opener.open('http://xk.autoisp.shu.edu.cn/CourseSelectionStudent/FastInput')
        if len(re.findall('限制', reponse)) != 0:
            print 'hypocritical'
            return None 
        if time.time() - embark > reset_time:
            print 'farewell'
            client = client_login(username, password, model_dict)
            vain = client.opener.open('http://xk.autoisp.shu.edu.cn/CourseSelectionStudent/FastInput')
            embark = time.time()
        time.sleep(idle_time)
    print 'peace'
    return None

def wise_course_attack(username, password, model_dcit, class_list, idle_time = 2, reset_time = 100):
    client = client_login(username, password, model_dict)
    request = request_constructor(username, 'select_course', class_list)
    vain = client.opener.open('http://xk.autoisp.shu.edu.cn/CourseSelectionStudent/FastInput')
    flag = True
    embark = time.time()
    while flag:
        #print client.opener.open(request).read()
        client.opener.open('http://xk.autoisp.shu.edu.cn/Login/Logout')
        vain = client.opener.open('http://xk.autoisp.shu.edu.cn/Login/Index')
        client = client_login(username, password, model_dict)
        if client.opener.open('http://xk.autoisp.shu.edu.cn/StudentQuery/QueryEnrollRank').read().find('排名') != -1:
            print time.time()
        vain = client.opener.open('http://xk.autoisp.shu.edu.cn/CourseSelectionStudent/FastInput')
        #print vain.read()
    print 'peace'
    return None

test_list = [{'classid' : '00874008', 'teacherid' : '1018'}]

#preload svm model
model_dir = os.getcwd() + '\\model'
files = os.listdir(model_dir)
model_dict = {}
for file in files:
    temp_model = svm_load_model(model_dir + '\\' + file)
    model_dict[str(file).strip('.model')] = temp_model

#get input
username = raw_input('enter student id:')
password = raw_input('enter passphrase:')
class_number = input('enter the number of class:')
class_list = [{'classid' : '', 'teacherid' : ''} for i in range(class_number)]

for i in range(class_number):
    class_list[i]['classid'] = raw_input('the id of class ' +str(i) + ':')
    class_list[i]['teacherid'] = raw_input('the id of teacher ' +str(i) + ':')
class_list = test_list
course_attack(username, password, model_dict, class_list)
