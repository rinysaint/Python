import json
import os
import requests
import urllib3


#urllib3.disable_warnings()
videosfolder = "videos"


web_url = input("输入视频下载址: ")# "http://cache.gensee.com/gsgetrecord/recordcz133.gensee.net/gsrecord/33162/sbr/2021_04_05/HkH3KgIXnb_1617584245/hls/seg2_"
title_name = input("输入视频名称: ")# "任务3：第四章、第五章内容讲解（上）： 项目整合管理、项目范围管理"
download_path = "./" + videosfolder + "/" + title_name


def download():
    for i in range(1,10):
        base_url = web_url.rsplit("/",1)[0] + "/"
        # m3u8_name = "record{}.m3u8".format(i)
        m3u8_name = web_url.rsplit("/",1)[1] + "{}.m3u8".format(i)
        m3u8_url =  base_url + m3u8_name
        print("下载 %s" % m3u8_name)
        resultnum = download_file(m3u8_url,m3u8_name)
        if(resultnum == 0): break
        ts_urls = get_ts_urls(download_path+ "/"+ m3u8_name, base_url)
        print("开始下载 %s 个文件" % len(ts_urls))
        for j in range(len(ts_urls)):
            ts_url = ts_urls[j]
            file_name = ts_url.split("/")[-1]
            # print("开始下载 %s" % file_name)
            resultnum = download_file(ts_url,file_name)
            if (resultnum == 0): break
        print("%s 完成 下载" % m3u8_name)
    if os.path.exists(download_path):
        combine(download_path, download_path + "/combine/", title_name)


def download_file(get_url,file_name):
    try:
        response = requests.get(get_url, stream=True, verify=True)
        if response:
            file_path = download_path + "/{0}".format(file_name)
            if not os.path.exists("./"+videosfolder):
                os.mkdir("./"+videosfolder)
            if not os.path.exists(download_path):
                os.mkdir(download_path)
            if not os.path.exists(file_path):
                with open(file_path, "wb+") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
            return 1
        else:
            print("异常请求：%s" % response.status_code)
            return 0
    except Exception as e:
        print("异常请求：%s" % e.args)
        return 0


def get_ts_urls(m3u8_path,base_url):
    urls = []
    with open(m3u8_path,"r") as file:
        if not os.path.exists(download_path):
            return
        lines = file.readlines()
        for line in lines:
            if line.endswith(".ts\n"):
                urls.append(base_url + line.strip("\n"))
    return urls


def file_walker(path):
    file_list = []
    for filename in os.listdir(path):
        if filename.endswith('.ts'):
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath):
                file_list.append(filepath)
                # print(filename)
    return file_list


def combine(ts_path, combine_path, file_name):
    file_list = file_walker(ts_path)
    file_path = combine_path + file_name + '.ts'
    if not os.path.exists(combine_path):
        os.mkdir(combine_path)
    print("开始合并 %s" % file_name)
    with open(file_path, 'wb+') as fw:
        for i in range(len(file_list)):
            fw.write(open(file_list[i], 'rb').read())


if __name__ == "__main__":
    download()