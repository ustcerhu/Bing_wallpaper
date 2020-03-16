import pandas as pd
import numpy as np
import os
import re
from selenium import webdriver
import time
import requests

#访问网址前亮明身份，提供header信息，模拟浏览器进行网页访问
header={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}

#打开浏览器
browser = webdriver.Chrome()
#等待10秒加载
browser.implicitly_wait(20)

#打开网页
browser.get('https://bing.ioliu.cn/')#打开图片所在网址
#使用get_attribute()方法获取对应属性的属性值，src属性值就是图片地址，图片有两种情况，一种是img标签，src属性是图片地址；另一种是其他标签（a，div等等），图片地址放在css的background-image属性中。
#browser.find_elements_by_tag_name('img')#这个方式可以直接获取图片，但是打印内容为空

#这个模块用于根据图片的url下载图片存在当前文件夹下的pic文件夹中；urllib有个retrieve属性也可以实现
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

#获取单页图片列，根据url列表进行循环获取，通过定位元素的路径，找到其对应的属性，获取图片网址，需要注意，一定是网址前面最近的标签作为本参数第二个标签值，需要注意标签值有时候并非真实图片地址，需要进行分析和加工
url_list=browser.find_elements_by_xpath('//div[@class="card progressive"]/img[@class="progressive__img progressive--is-loaded"]')
def Get_Page_Pic(url_list):
    for i in range(len(url_list)):
        url_raw=url_list[i].get_attribute('src')#获取每个图片的网址,或者包含该图片网址（以.jpg结尾）这个案例是在链接里面的？之前部分
        url=url_raw.split('?')[-2]#获取真实的图片链接地址
        Get_Pic(url)

Get_Page_Pic(url_list)#获取首页的图片

#接下来，点击‘下一页’，根据需要的页数进行设置总共的需要爬取的页数
for i in range(123):
     try:
         new=browser.find_element_by_link_text('下一页')
         new.click()
         url_list=browser.find_elements_by_xpath('//div[@class="card progressive"]/img[@class="progressive__img progressive--is-loaded"]')
         Get_Page_Pic(url_list)
     except:
         new=None

browser.quit()#下载完之后，关闭浏览器

#这个程序潜在的问题：1.网页加载时间可能来不及每页的图片都下载完，可能有漏的；2.服务器会禁止下载，所以经过两次下载后获取了110页的图片，其中还有些漏的