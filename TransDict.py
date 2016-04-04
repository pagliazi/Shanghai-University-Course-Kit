s = '''Host: xk.shu.edu.cn:8080
Connection: keep-alive
Content-Length: 60
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Origin: http://xk.shu.edu.cn:8080
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2552.0 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Referer: http://xk.shu.edu.cn:8080/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: _ga=GA1.3.548295607.1450860734; Hm_lvt_444bf10f6d7469654b7f41f9f9f9c301=1449989162,1449989164,1451806133,1452091199; ASP.NET_SessionId=x53rq4glf3mvhntzscj1r1ji
'''
s = s.strip().split('\n')
s = {x.split(': ')[0] : x.split(': ')[1] for x in s}
print(s)