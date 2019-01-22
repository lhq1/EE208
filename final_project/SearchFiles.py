#coding:utf-8
#!/usr/bin/env python


INDEX_DIR = "IndexFiles.index"

import sys, os, lucene
import jieba
import re
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.search.highlight import Highlighter
from org.apache.lucene.util import Version
reload(sys)
sys.setdefaultencoding('UTF-8')
"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def parsecommand(command):
    allowed_opt = ['site']
    command_dict = {}
    opt = '标题'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict


def run(searcher, analyzer):
    while True:
        print
        print "Hit enter with no input to quit."
        command = raw_input("Query:")
        #command = unicode(command, 'GBK')
        if command == '':
            return
        '''
        command_dict = parsecommand(command)
        lis = jieba.cut(command_dict['contents'])
        command_dict['contents']=' '.join(lis)
        '''
        print "Searching for:", command
        query = QueryParser(Version.LUCENE_CURRENT, "演员",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        print "%s total matching documents." % len(scoreDocs)
        lis = []
        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            #titleHighLight = Highlighter.getBestFragment(analyzer, "title", doc.get("标题"))
            #print titleHighLighthttps://img1.doubanio.com/view/photo/s_ratio_poster/public/p2502530749.jpg
            lis.append([doc.get('标题'),doc.get('图片'),doc.get('评分'),doc.get("上映日期:"),doc.get("类型:")])
            lis.sort(key=lambda x:x[2],reverse=True)
            #print 'path:', doc.get("path"),  \
                #"title:",doc.get("title"),"url:",doc.get("url"),'score:', scoreDoc.score
            # print 'explain:', searcher.explain(query, scoreDoc.doc)
        return lis


if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    lis = run(searcher, analyzer)
    for i in lis:
        for j in i:
            print j
    del searcher
