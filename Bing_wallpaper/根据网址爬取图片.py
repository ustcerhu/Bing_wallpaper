import os
import requests
import re
header={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
#这个模块用于根据图片的url下载图片存在当前文件夹下的pic文件夹中
def Get_Pic(url):
    d=os.getcwd()+'\\pic\\'
    path=d+url.split('/')[-1]#下载的图片文件名，保留原文件名
    try:
        if not os.path.exists(d):
            os.makedirs(d)#如果文件夹不存在，就新建一个
        if not os.path.exists(path):
            r=requests.get(url,headers=header)#如果文件不存在，继续
            r.raise_for_status()#判断是否成功根据图片网址获取图片
            with open(path,'wb')as f:
                f.write(r.content)
                f.close()
                print('图片保存成功')
        else:
            print('图片已存在')
    except:
        print('图片获取失败')

raw_url='http://h1.ioliu.cn/bing/FlowingClouds_ZH-CN0721854476_1920x1080.jpg?imageslim'
url=raw_url.split('?')[-2]#举个例子

Get_Pic(url)