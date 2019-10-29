#!/usr/bin/env python
# coding: utf-8
# @Author  : Mr.K
# @Software: PyCharm Community Edition
# @Description: 用来爬取"食品安全网-食品咨询-国内监管"下的内容(url=http://foodsafeguard.com/news/list-2.html)

import requests
from bs4 import BeautifulSoup
import time
import re

# 保存的txt文件名
TXT_FILE_NAME = "食品安全网10-10.txt"

def main():#主函数
    print("采集开始")
    time_start = time.time()
    # 设置要爬取的页码
    for page in range(61, 70):
        dispose_page(page)
    time_end = time.time()
    print("程序处理完毕")
    print('总共耗时：%d分钟'%((time_end-time_start)/60))


def dispose_page(page):
    """
    处理url，可以择取出待处理的url
    """
    try:
        print("正在处理第%d页" % page)
        url = "http://foodsafeguard.com/news/list-2.html?page=%d"%page
        response = requests.get(url, timeout=20)
    except Exception as e:
        # 遇到异常(可能被限制速度)延时5秒再继续
        time.sleep(5)
        dispose_page(page)
    response.encoding = "utf-8"
    text = response.text#将所有前端代码保存为txt
    soup = BeautifulSoup(text, "html.parser")
    lst_b = soup.find_all("li")
    if lst_b:
        for b in lst_b:
            a = b.find("a")
            if a:
                href = a.get("href")
                if href and "html" in href:
                    dispose_info("http://foodsafeguard.com"+href)
                # if href and "http://" in href:
                # dispose_info(href)

def dispose_info(url):
    """
    信息提取函数，用于提取url中的具体信息
    """
    if not url:
        return
    print("正在采集：%s" % url)
    time.sleep(5)
    try:
        response = requests.get(url, timeout=5) # 执行网络请求
        response.encoding = "utf-8"
        text = response.text
        soup = BeautifulSoup(text, "html.parser")
        # if "http://foodsafeguard.com" in url:
        #     content = dispose_health(soup)
        # else:
        #     content = dispose_shipin(soup)
        content = dispose_title_content(soup)
        print(content)
        save_txt(TXT_FILE_NAME, content)# 保存到txt中
    except Exception as e:
        # 遇到异常（可能被限制速度）延迟5秒再继续
        print('连接异常，延时5秒')
        time.sleep(5)
        dispose_info(url)

def dispose_title_content(soup):
    """
    提取出文章的标题与正文
    """
    if not soup:
        return
    content = ""

    #提取出标题与正文
    div = soup.find("div", class_="news-content")#必须用find_all，不然链接出错
    if div:
        #提取标题
        h1=div.find("h1")
        if h1:
            content=h1.get_text()
        #提取正文
        p=div.find_all("p")
        for each_p in p:
           content+=each_p.get_text()

    '''
    #其实找标题也可以这么写，更为简洁，但是不如上面写法成体系
    h1=soup.find("h1")
    if h1:
        content = h1.get_text() + "\n"  # 获取标题文本内容存到content中
    '''
    # 提取出文章的标题
    # div = soup.find_all("div", class_="news-content")#找到news_content类的div标签
    # if div:
    #     # h1 = soup.find("h1")
    #     h1 = div[0].find("h1")# 找到h1后面的标题内容，注意div格式是list，因此需要加上[0]
    #     if h1:
    #         content = h1.get_text() + "\n"  # 获取标题文本内容存到content中

    # #提取出文章的正文
    # p=soup.find_all("p")#找到p标签
    # if p:#提取p中的内容
    #    for each_p in p:
    #        content += each_p.get_text() + "\n"
    #content = re.sub("关键词免责声明：① 凡本网所有原始文章及图片、图表的版权均属食品安全网所有，如要转载，需注明“信息来源：食品安全网”。② 凡本网注明“信息来源：XXX（非食品安全网）”的作品，均转载自其他媒体，转载目的在于传递更多的信息，并不代表本网赞同其观点和对其真实性负责。联系电话：400-690-8568", " ", content)
    content += "\n"#每篇文章末尾再空一个行
    return content


def save_txt(file_name, content):
    """
     保存内容到txt文件中
    """
    if not file_name or not content:
        return
    # lst_data是一个二维列表
    with open(file_name, "a", encoding="utf-8", newline="") as file:
        file.write(content + "\n")

# 程序入口
if __name__ == '__main__':
    main()









#-----------------------------------------------------------------------------------------------------------------------
# def dispose_shipin(soup):
#     """
#     处理食品频道的，返回text
#     :param soup:
#     :return:
#     """
#     if not soup:
#         return
#     content = ""
#     # 提取文章标题
#     h1 = soup.find("h1")
#     if h1:
#         content =  "///" + h1.get_text() + "\n"
#
#     # 提取出文章内容所在div
#     div = soup.find("div", id="news-content")
#     if div:
#         # 去除正文html中的style元素及script元素
#         [x.extract() for x in div.findAll('script')]
#         [x.extract() for x in div.findAll('style')]
#         content += div.get_text(strip=True, separator="\n")
#     # 每章结尾空两行
#     content += "\n\n"
#     return content