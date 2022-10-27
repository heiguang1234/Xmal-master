# 开发者： Hei Guang
# 开发时间：2022/10/21 10:52
import html
import re
import requests
from bs4 import BeautifulSoup
from lxml import etree

if __name__ == "__main__":
    list = []
    url = 'https://developer.android.google.cn/reference/android/Manifest.permission'
    headers = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '306',
        # 'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'cloud_sessionID=a133a2ac8bab050b523cd85ffbf1215a; _csrf-cloud=6b38af1871c36da35d2d4d7691adcb3b10c1fa1960dc8be43afa7407a2a94825a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22_csrf-cloud%22%3Bi%3A1%3Bs%3A32%3A%22aERns0rEOGwqT1XWWg0X_9oIh3qAChPE%22%3B%7D',
        # 'Host': 'yun.ujs.edu.cn',
        # 'Origin': 'http://yun.ujs.edu.cn',
        # 'Referer': 'http://yun.ujs.edu.cn/xxhgl/yqsb/grmrsb?v=5413',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0'
    }
    # response = requests.get(url=url, headers=headers)
    # content = response.text
    # parser = etree.HTMLParser(encoding="utf-8")
    # tree = etree.parse('/Users/linzi/PycharmProjects/Xmal-master/Code/permssion.html', parser=parser)
    # list = tree.xpath('//a/@href')
    # list=tree.xpath('//*[@id="constants"]/tbody/tr[2]/td[2]/code/a//@href')
    # print(list)
    # for item in list:
    #     if '/reference/android/Manifest.permission#' in item:
    #         permission=item.split("/")[3]
    #         with open('permssion.txt','a') as ps:
    #             ps.write(permission+'\n')
    #         print(item)
    # soup=BeautifulSoup('permission.html','html.parser')
    # for k in soup.find_all('div',id='jd-content'):
    #     print(k)
    # with open("permssion.html",'w') as ht:
    #     ht.write(content)

o = open("permssion.txt", 'r')
line = o.readline()

while line:
    print(line.replace("Manifest.permission#",''),end='')
    line=o.readline()
o.close()
# print(list)
