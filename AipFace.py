import base64
import datetime
import gc
import os
import socket
import sys
import time
import queue
import threading
import numpy as np

from showWinMsg import ShowMsg
from io import BytesIO
import cv2
from PIL import Image
from aip import AipBodyAnalysis
from aip import AipFace


class from_obj(object):
    def __init__(self):
        self.qe = queue
        self.q = self.qe.Queue(maxsize=5)

        """ 你的人流量统计 APPID AK SK """
        self.APP_ID = '16193424';
        self.API_KEY = 'eqZCDofIR6FXWaMHr5bszls6';
        self.SECRET_KEY = 'CIlH54Ro1HvpZwQR4nQbetQEcnPqWbUQ';

        self.aipBodyAnalysis = AipBodyAnalysis(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        # self.aipFace = AipFace(Aself.PP_ID, self.API_KEY, self.SECRET_KEY)
        self.cap = cv2.VideoCapture("http://49.90.255.4:10001/8.ts");
        # http://192.168.4.121/action/stream?subject=mjpeg&user=admin&pwd=12345
        # rtsp://192.168.4.121:554/live/main

def catchp():
    # print("start CatchPicture")
    while True:
        if not obj.q.empty():
            bodytracking();


def bodytracking():
    fq = obj.q.get()
    try:
        if int(time.time()) % 10 == 0:
            content = "";
            # print(timeC)
            # print(datetime.now())
            imgarr = Image.fromarray(fq)  # 将每一帧转为Image
            output_buffer = BytesIO()  # 创建一个BytesIO
            imgarr.save(output_buffer, format='JPEG')  # 写入output_buffer
            byte_data = output_buffer.getvalue()  # 在内存中读取

            btoptions = {}
            btoptions["type"] = "gender"
            content = obj.aipBodyAnalysis.bodyAttr(byte_data, btoptions);
            if content:
                if 'person_num' in content.keys():
                    # if int(content['person_count']['in']) > 0 or int(content['person_count']['out']) > 0:
                    #     udpsent(content, 1)
                    udpsent(content, 0);
                    # showframe(content)
            del content;
            del btoptions;
    except :
        pass
    obj.q.task_done();
    del fq;
    gc.collect();
    # print(datetime.now())


def showframe(content):
    img_b64decode = base64.b64decode(content['image'])  # base64解码
    img_array = np.fromstring(img_b64decode, np.uint8)  # 转换np序列
    frame = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 转换Opencv格式
    cv2.imshow("showframe", frame)


def receive():
    # print("start Reveive")
    ret = obj.cap.read()
    while ret:
        try:
            if int(time.time()) % 300 == 0:
                restart_program();
            ret, frame = obj.cap.read()
            obj.q.put_nowait(frame)
            del frame;
            gc.collect();
        except:
            pass


def udpsent(content,type):
    BUFSIZE = 1024
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_port2 = ('127.0.0.1', 9999)
    ip_port = ('117.83.83.140', 54323)
    time_str = hex(int(time.time()))[2:].zfill(8)
    pnum = hex(content['person_num'])[2:].zfill(2)
    if type == 0:
        sendmsg2 = 'AC0A0000000000000001' + pnum + '00' + '00' + time_str
        client.sendto(bytes.fromhex(sendmsg2), ip_port)
        client.sendto(bytes.fromhex(sendmsg2), ip_port2)
        del sendmsg2;
    if type == 1:
        innum = hex(content['person_count']['in'])[2:].zfill(2)
        outnum = hex(content['person_count']['out'])[2:].zfill(2)
        sendmsg2 = 'AC0A0000000000000001' + pnum + innum + outnum + time_str
        client.sendto(bytes.fromhex(sendmsg2) , ip_port)
        del innum;
        del outnum;
        del sendmsg2;
    # if (int(content['person_num']) > 0):
        # p3 = threading.Thread(target=os.system("python E:\pywork\SkyWellFaceRecByBaiDu\showWinMsg.py %s" % content['person_num']))
        # p3 = threading.Thread(target=ShowMsg(content['person_num']))
        # p3.start()
        # p3.join()
        # ShowMsg(content);
    client.close()
    del ip_port;
    del time_str;
    del pnum;
    del client;
    gc.collect();


def restart_program():
    python = sys.executable
    os.execl(python, python,* sys.argv)

if __name__ == '__main__':
    theday = datetime.strptime("2019-09-01","%Y-%m-%d")
    if datetime.datetime.now().strftime("%Y-%m-%d") < theday:
        obj = from_obj();
        p1 = threading.Thread(target=receive)
        p2 = threading.Thread(target=catchp)
        p1.start()
        p2.start()
    else:
    	todayis = "1972-09-05"