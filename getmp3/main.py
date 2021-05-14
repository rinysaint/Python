import os
import time
import requests
from scrapy.selector import Selector


class wangyiyun():
  def __init__(self):
    self.headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    self.main_url='http://music.163.com/'
    self.session = requests.Session()
    self.session.headers=self.headers

  def get_songurls(self,playlist):
    url=self.main_url+'playlist?id=%s'% playlist
    re= self.session.get(url)  #直接用session进入网页，懒得构造了
    sel=Selector(text=re.text)  #用scrapy的Selector，懒得用BS4了
    songurls=sel.xpath('//ul[@class="f-hide"]/li/a')
    return songurls

  def download_song(self, songurls):
    urllist = []
    namelist =[]
    hrefs = songurls.xpath('@href').extract()
    names = songurls.xpath('text()').extract()
    for i in range(len(songurls)):
        musicUrl = 'http://music.163.com/song/media/outer/url?id=%s.mp3' % hrefs[i].rsplit('id=', 1)[1]
        urllist.append(musicUrl+'\n')
        namelist.append(hrefs[i].rsplit('id=', 1)[1] +' : '+ names[i] + '\n')
        # try:
        #     print('正在下载', names[i])
        #     if musicUrl is None or names[i] is None:
        #         print('参数错误')
        #         return None
        #         # 文件夹不存在，则创建文件夹
        #     folder = os.path.exists('./musics')
        #     if not folder:
        #         os.makedirs('./musics')
        #     # 读取MP3资源
        #     # proxies = {'http': '8.133.191.41:80'}
        #     # res = requests.get(url =musicUrl) #,roxies=proxies
        #     querystring = {"id": hrefs[i].rsplit('id=', 1)[1]+".mp3"}
        #     headers = {
        #         'content-type': "application/x-www-form-urlencoded",
        #         'cache-control': "no-cache",
        #         'postman-token': "bee5c5c0-a3a8-c1a2-ecaa-30f869d748ab"
        #     }
        #     response = requests.request("GET", musicUrl, headers=headers, params=querystring)
        #     # 获取文件地址
        #     file_path = os.path.join('./musics/', names[i]+'.mp3')
        #     print("开始写入文件：%s code: %s" % (file_path,response.text))
        #     # 打开本地文件夹路径file_path，以二进制流方式写入，保存到本地
        #     with open(file_path, 'wb') as fd:
        #         fd.write(response.content)
        #         print(names[i] + ' 成功下载！')
        # except Exception as e:
        #     print("下载失败!" + str(e.args))
    f = open("./musics/urllist.txt", "w")
    f.writelines(urllist)
    f.close()
    f = open("./musics/namelist.txt", "w")
    f.writelines(namelist)
    f.close()

  def work(self, playlist):
    songurls = self.get_songurls(playlist) # 输入歌单编号，得到歌单所有歌曲的url'
    self.download_song(songurls) # 下载歌曲


if __name__ == '__main__':
  d = wangyiyun()
  d.work(2250011882)
  # songlistnum = input("输入歌单ID: ")
  # if songlistnum:
  #   d.work(songlistnum)