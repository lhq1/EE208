from bs4 import BeautifulSoup
import urllib2
import urlparse
import os
def valid_filename(s):
    import string
    valid_chars = "-_() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    if len(s)>=40:
        a=s[0:40]+'.txt'
    else:
        a=s+'.txt'
    return a
def add_page_to_folder(page, biaoti,content):
    index_filename = 'index.txt'
    folder = 'html'
    filename = valid_filename(page)
    index = open(index_filename, 'a')
    index.write(biaoti.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()

    if not os.path.exists(folder):
        os.mkdir(folder)

    f = open(os.path.join(folder, filename), 'w')

    l=str(page).encode('utf-8')+'\t'+content.encode('utf-8')
    try:
        f.write(l)
    except:
        f.write('mei you wen jian')
    else:
        f.close()
def parseAqiyi(content):
    soup=BeautifulSoup(content,features="html.parser")
    for i in soup.findAll("ul", {"class": 'site-piclist site-piclist-180236 site-piclist-auto'}):
        for child in range(30):
            print child
            try:
                links = i.contents[2 * child + 1].contents[1].a.get('href')
                req = urllib2.Request(links, None, {'User-agent': 'Custom User Agent'})
                content = urllib2.urlopen(req).read()
                soup2 = BeautifulSoup(content, features="html.parser")
                for j in soup2.findAll('div', {'class': "album-head-info clearfix"}):
                    haibao = 'http:' + j.contents[1].a.img.get('src')
                    biaoti = j.contents[3].h1.contents[1].string
                    neirong = j.contents[3].contents[5]
                    flag = 0
                    try:
                        yuanbieming = neirong.findAll('div', {'class': 'info-title-name'})
                    except AttributeError:
                        flag = 1
                        print 2
                    if flag == 1:
                        break
                    yuanbieming = neirong.findAll('div', {'class': 'info-title-name'})
                    if yuanbieming:
                        yuanming = yuanbieming[0].findAll('div', {'class': 'info-title-englishName'})
                        bieming = yuanbieming[0].findAll('div', {'class': 'info-title-otherName'})
                        if yuanming:
                            yuanming = yuanming[0].span.string
                        else:
                            yuanming = 'None'
                        if bieming:
                            bieming = bieming[0].span.string
                        else:
                            bieming = 'None'
                    else:
                        yuanming = bieming = "None"
                    biaoqian = neirong.findAll('div', {'class': 'episodeIntro-item clearfix'})[0]
                    diqu = biaoqian.contents[1].contents[1].contents[3].string.strip(' ').rstrip('\n')
                    shouying = biaoqian.contents[1].contents[3].span.string.strip(' ').rstrip('\n')
                    yuyan = biaoqian.contents[3].contents[1].span.string.strip(' ').rstrip('\n')
                    luying = biaoqian.contents[3].contents[3].span.string.strip(' ').rstrip('\n')
                    pianchang = biaoqian.contents[5].contents[1].span.string.strip(' ').split(' ')[0].rstrip('\n')
                    daoyan = biaoqian.contents[7].p.contents[3].string
                    jianjie = neirong.findAll('div', {'class': 'shortWordIntro-brief', 'data-moreorless': "moreinfo"})
                    if jianjie:
                        jianjie = jianjie[0].span.string.strip(' ')
                    else:
                        jianjie = neirong.findAll('div', {'class': 'shortWordIntro-brief', 'data-moreorless': "lessinfo"})[
                            0]
                        jianjie = jianjie.span.string.strip(' ')
                    lianjie = j.contents[3].contents[9].a.get('href')
                    everything="wangzhi:\t"+links+"\thaibao:\t"+haibao+'\tbiaoti:\t'+biaoti+'\tyuanming:\t'+yuanming+'\tbieming:\t'+bieming+'\tdiqu:\t'+diqu\
                    +'\tshouying:\t'+shouying+'\tyuyan:\t'+yuyan+'\tluying:\t'+luying+'\tpianchang:\t'+pianchang+'\tdaoyan:\t'+daoyan\
                        +"\tjianjie:\t"+jianjie+'\tlianjie:\t'+lianjie
                    print biaoti
                    add_page_to_folder(links,links,everything)
            except:
                print 0




def working():
    for i in range(100-17-3-7-70):
        print 'the page is: '+str(i)
        wangzhan="http://www.iqiyi.com/lib/dianying/%2C%2C_4_"+str(i+18+3+7+70)+".html"
        req=urllib2.Request(wangzhan,None,{'User-agent':'Custom User Agent'})
        content=urllib2.urlopen(req).read()
        parseAqiyi(content)
working()