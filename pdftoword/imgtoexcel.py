import os  # 加载操作系统模块
from aip import AipOcr  # 调用百度Ocr模块
import requests  # 调用反馈模块
import time  # 调用时间模块
import tkinter as tk  # 调用GUI图形模块
from tkinter import filedialog

# KEY信息，请输入自己申请的应用信息
APP_ID = '24021012'
API_KEY = 'T8oEPkt9eLbl09i6hTCeGMER'
SECRET_KEY = 'Z7UuZfCE9E49IVbpDbpbHnEDbeb1aLlr'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


# 读取文件函数(返回读取结果)
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 文件下载函数
def file_download(url, file_path):
    r = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(r.content)


root = tk.Tk()
root.withdraw()
data_dir = filedialog.askdirectory(title='请选择图片文件夹') + '/'  # 用对话框选择图片存储文件夹
result_dir = filedialog.askdirectory(title='请选择输出文件夹') + '/'  # 自选输出文件夹
num = 0

for name in os.listdir(data_dir):
    print('{0}: {1} 正在处理：'.format(num + 1, name.split('.')[0]))
    image = get_file_content(os.path.join(data_dir, name))  # 调用读取图片子程序
    res = client.tableRecognitionAsync(image)  # 调用表格文字识别
    req_id = res['result'][0]['request_id']  # 获取识别ID号
    for count in range(1, 10):  # OCR识别也需要一定时间，设定10秒内每隔1秒查询一次
        res = client.getTableRecognitionResult(req_id)  # 通过ID获取表格文件XLS地址
        print(res['result']['ret_msg'])
        if res['result']['ret_msg'] == '已完成':
            break  # 云端处理完毕，成功获取表格文件下载地址，跳出循环
        else:
            time.sleep(1)
    url = res['result']['result_data']
    xls_name = name.split('.')[0] + '.xls'
    file_download(url, os.path.join(result_dir, xls_name))  # 调用文件下载子程序
    num = num + 1
    print('{0}: {1} 下载完成。'.format(num, xls_name))
    time.sleep(1)