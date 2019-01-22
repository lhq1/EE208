#coding:utf-8
import web
from web import form
import jieba
import lucene
import urllib2
import os,sys
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.util import Version
from urllib import urlretrieve
import shit
urls = (
    '/', 'index',
    '/s', 'result',
    '/m', 'detail'
)

login = form.Form(
    form.Textbox('keyword'),
    form.Button('Search'),
)
tupian=form.Form(
    form.Button("select",type="file"),
    form.Button('Search',type="submit")
)
tupian2=form.Form(
    form.Textbox('pic url'),
    form.Button('Submit')
)

def func(command):
    seq = jieba.cut(command)
    command=' '.join(seq)
    return command


render = web.template.render('template')


def run(searcher, analyzer, command):
    while True:
        #command = unicode(command, 'GBK')
        if command == '':
            return
        '''
        command_dict = parsecommand(command)
        lis = jieba.cut(command_dict['contents'])
        command_dict['contents']=' '.join(lis)
        '''
        query = QueryParser(Version.LUCENE_CURRENT, "标题",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        lis = []
        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            #titleHighLight = Highlighter.getBestFragment(analyzer, "title", doc.get("标题"))
            #print titleHighLight
            word = doc.get('名字')
            if len(word)>15:
                word = word[:15]
            lis.append([word,doc.get('图片'),doc.get('评分')])

            #print 'path:', doc.get("path"),  \
                #"title:",doc.get("title"),"url:",doc.get("url"),'score:', scoreDoc.score
            # print 'explain:', searcher.explain(query, scoreDoc.doc)
        return lis

def inf(searcher, analyzer, command):
    if command == '':
        return
    '''
    command_dict = parsecommand(command)
    lis = jieba.cut(command_dict['contents'])
    command_dict['contents']=' '.join(lis)
    '''
    query = QueryParser(Version.LUCENE_CURRENT, "标题",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 50).scoreDocs
    doc = searcher.doc(scoreDocs[0].doc)
    dir = doc.get('导演')
    act=doc.get('主演')
    act=act.split('/')
    act=' '.join(act)
    lis = [doc.get('标题'),doc.get('图片'),doc.get('类型:'),doc.get('评分'),doc.get('导演'),doc.get('片长:'),
            doc.get("上映日期:"), doc.get('语言:'),doc.get("主演"),doc.get("简介")]
    rec = [[],[]]
    query = QueryParser(Version.LUCENE_CURRENT, "导演",
                        analyzer).parse(dir)
    scoreDocs = searcher.search(query, 50).scoreDocs
    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        if doc.get('名字')!=command:
            rec[0].append(doc.get('名字'))
    query = QueryParser(Version.LUCENE_CURRENT, "主演",
                        analyzer).parse(act)
    scoreDocs = searcher.search(query, 50).scoreDocs
    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        if doc.get('名字')!=command:
            rec[1].append(doc.get('名字'))
    print rec[1]
    return lis,rec

class index:
    def GET(self):
        f = login()
        return render.index(f)


class result:
    def GET(self):
        user_data = web.input()
        message=user_data.keyword
        if len(message)>10:
           if (len(message)>3 and message[-3]+message[-2]+message[-1]=='png' or message[-3]+message[-2]+message[-1]=='jpg'):
            urlretrieve(message, 'target.jpg')
            lis1=shit.LSH('target.jpg')
            lis=[]
            vm_env.attachCurrentThread()
            STORE_DIR = 'index'
            directory = SimpleFSDirectory(File(STORE_DIR))
            searcher = IndexSearcher(DirectoryReader.open(directory))
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
            for i in range(len(lis1)):
                lis.append(run(searcher, analyzer, lis1[i])[0])
        else:
            a = func(user_data.keyword)
            STORE_DIR = 'index'
            vm_env.attachCurrentThread()
            directory = SimpleFSDirectory(File(STORE_DIR))
            searcher = IndexSearcher(DirectoryReader.open(directory))
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
            lis = run(searcher, analyzer,a)
        f = login
        return render.movies(f,lis)


class detail:
    def GET(self):
        user_data = web.input()
        a = func(user_data.get('name'))
        f = login()
        STORE_DIR = 'index'
        vm_env.attachCurrentThread()
        directory = SimpleFSDirectory(File(STORE_DIR))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        info,rec = inf(searcher, analyzer, a)
        return render.moviedetails(f, info, rec)


if __name__ == "__main__":
    global vm_env
    vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    app = web.application(urls, globals(),False)
    app.run()