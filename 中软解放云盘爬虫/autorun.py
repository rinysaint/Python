"""
功能：下载指定url内的所有的pdf
语法：将含有pdf的url放到脚本后面执行就可以了
"""
import json
import os
import time
import jsonpath
import requests

try:
    root_url = "https://pan.jfunbox.com/pre/idocv/getFile?baseurl=http://192.168.3.226:8080"
    view_url = "/view/GnaPJvf.json?start=1&size=0&=&type=imgall"
except:
    print("please input url behind the script!!")
    exit()

def getTagA(root_url,view_url):
    res = requests.get(root_url+view_url)
    jsontostr = json.loads(res.text)
    urls = jsonpath.jsonpath(jsontostr, "$..url")
    filename = jsonpath.jsonpath(jsontostr, "$.name")
    totalsize = jsonpath.jsonpath(jsontostr, "$.totalSize")
    return urls,filename,totalsize

def downPdf(root_url,list_a):
    number = 1
    Foldername = time.time();
    if list_a:
        if list_a[2]:
            totalsize = int(list_a[2][0])
        if list_a[0]:
            for url in list_a[0]:
                if url:
                    if url.lower().endswith(".png"):
                        filename = url[url.rindex('/')+1:]
                        print("Download the %d/%d png immdiately!!!"%(number,totalsize),end='  ')
                        print(filename+' downing.....')
                        number += 1
                         ##因为要下载的是二进制流文件，将strem参数置为True
                        if list_a[1]:
                            if not os.path.exists(list_a[1][0]):
                                os.makedirs(list_a[1][0])
                            else:
                                response = requests.get(root_url + url, stream="TRUE")
                                open(list_a[1][0] +"/"+ filename, 'wb').write(response.content)
                                del response
                        else:
                            os.makedirs(Foldername)
                            response = requests.get(root_url + url, stream="TRUE")
                            open(Foldername +"/"+ filename, 'wb').write(response.content)
                            del response

if __name__ == "__main__":
    downPdf(root_url,getTagA(root_url,view_url))