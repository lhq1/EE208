# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urlparse
import urllib2
import sys
import os
import random
import time
import requests
reload(sys)
sys.setdefaultencoding('utf-8')


def get_ip_list(url, headers):
  web_data = requests.get(url, headers=headers)
  soup = BeautifulSoup(web_data.text, 'lxml')
  ips = soup.find_all('tr')
  ip_list = []
  for i in range(1, len(ips)):
    ip_info = ips[i]
    tds = ip_info.find_all('td')
    ip_list.append(tds[1].text + ':' + tds[2].text)
  return ip_list


def get_random_ip(ip_list):
  proxy_list = []
  for ip in ip_list:
    proxy_list.append('http://' + ip)
  proxy_ip = random.choice(proxy_list)
  proxies = {'http': proxy_ip}
  return proxies


def deal(url,name):
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    ]
    user_agent = random.choice(user_agent_list)
    header={'User-Agent':user_agent}
    ip_list = get_ip_list('http://www.xicidaili.com/nn/', headers=header)
    proxy = get_random_ip(ip_list)
    httpproxy_handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(httpproxy_handler)
    req = urllib2.Request(url, headers=header)
    # content = urllib2.urlopen(req)
    content = opener.open(req)
    soup = BeautifulSoup(content, features="html.parser")
    # 标题
    title = soup.find('span',{'property':"v:itemreviewed"}).find(text=True)
    # 信息
    inf = soup.find('div',{'id':'info'})
    # 图片链接
    pic = soup.find('img').get('src','')
    # 评分
    vote = soup.find('strong',{'class':'ll rating_num'}).find(text=True)
    # 简介
    brief = ''
    brief1 = soup.find('span',{'property':'v:summary'})
    for i in brief1.contents:
        if type(i).__name__ == 'NavigableString':
            sub_brief = i
            sub_brief = sub_brief.strip()
            brief += sub_brief
    lis = []
    for i in inf.contents:
        if i !='\n':
            lis.append(i)
    res = []
    num1 = len(soup.findAll('span',{'property': 'v:genre'}))
    num2 = len(soup.findAll('span',{'property': 'v:initialReleaseDate'}))
    num3 = 0

    # 上映日期
    t = soup.find('span',{'property':'v:runtime'})
    while t.nextSibling.find('br'):
        num3 += 1
        print(t.nextSibling)
        t = t.nextSibling

    # 标签
    tag = soup.find('div', {'class':'tags-body'})
    tags = []
    for i in tag.contents:
        if i != '\n':
            tags.append(i.string.strip())
    # 影评
    comments = []
    comments_title = []
    for i in soup.findAll('div',{'class': 'main-bd'}):
        com_req = urllib2.Request(i.contents[1].contents[0].get('href',''),headers=header)
        com_page = opener.open(com_req)
        com_soup = BeautifulSoup(com_page,"html.parser")
        str=''
        comments_title.append(com_soup.find('span',{'property':'v:summary'}).string)
        for j in com_soup.find('div',{'class': 'review-content clearfix'}).contents:
            if j.string != None and j.string != '\n':
                str += j.string.strip()
        comments.append(str)

    for i in lis:
        if i == '\n' or i == ' ':
            continue
        if type(i).__name__ == 'Tag':
            if i.find(text=True) != None:
                res.append(i.find(text=True))
                if len(i.contents)>2:
                    str = ''
                    for j in i.contents[2]:
                        if type(j).__name__ == 'Tag':
                            str += j.find(text=True)
                        else:
                            str += j
                    res.append(str)
        else:
           res.append(i)
    # 链接
    hrefs = []
    for i in soup.findAll('a',{'class':'playBtn'}):
       hrefs.append([i.get('data-cn',''),i.get('href','')])

    str1 = ''.join(res[7:7+2*num1-1])
    str2 = ''.join(res[11+2*num1:10+2*num1+2*num2])
    if num3:
        str3 = ''.join(res[11+2*num1+2*num2:12+2*num1+2*num2+num3])
    new_lis = []
    for i in range(len(res)):
        if 6 <= i <7+2*num1-1 or 10+2*num1 <= i < 10+2*num1+2*num2\
            or(num3 and 10+2*num1+2*num2<=i<12+2*num1+2*num2+num3):
            continue
        else:
            new_lis.append(res[i])

    new_lis.append(res[6])
    new_lis.append(str1)
    new_lis.append(res[10+2*num1])
    new_lis.append(str2)
    if num3:
        new_lis.append(res[10+2*num1+2*num2])
        new_lis.append(str3)

    #写入文件
    f = open('test/'+name+'.txt','w')
    con1 = ["标题", '图片','评分', '简介', '标签']
    con2 = [title, pic, vote, brief, ' '.join(tags)]
    for i in range(5):
        f.write(con1[i])
        f.write(' ')
        f.write(con2[i])
        f.write('\n')

    for i in range(len(new_lis)):
        print(new_lis[i])
        f.write(new_lis[i])
        if i%2:
            f.write('\n')
        else:
            f.write(' ')
    f.write('链接')
    f.write(' ')
    for i in hrefs:
        f.write(i[0])
        f.write(' ')
        f.write(i[1])
        f.write(' ')
    f.write('\n' * 2)
    for i in range(len(comments_title)):
        f.write(comments_title[i])
        f.write('\n')
        f.write(comments[i])
        f.write('\n')
    f.close()


g = open('res.txt')
while True:
    line = g.readline()
    if not line:
        break
    line = line.split()
    print(line[0]+'.txt')
    if line[0]+'.txt' in os.listdir('test'):
        continue
    if len(line) == 2:
        deal(line[1],line[0])
    else:
        deal(line[-1],' '.join(line[0:len(line)-2]))
    time.sleep(random.random()*3)
