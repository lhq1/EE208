# -*- coding:utf-8 -*-
#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"
import sys, os, lucene, threading, time
from datetime import datetime
import jieba
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from bs4 import BeautifulSoup
"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print 'commit index'
        t=threading.Thread(target=ticker.run)
        t.start()
        t.join(10)
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setIndexed(False)
        t1.setStored(True)
        t1.setTokenized(False)
        
        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        i = 0

        for j in os.listdir(root):
            filename = root + '/' +j
            print filename
            print "adding", filename
            file = open(filename,'r')
            doc = Document()
            doc.add(Field('名字',j[:-4],t2))
            while True:
                    line = file.readline()
                    line = line.split()
                    if not line:
                        break

                    if len(line) > 1:
                        if line[0] == '标题' or line[0] == '导演' or line[0]=='主演' or line[0]=='类型:':
                            doc.add(Field(line[0],' '.join(line[1:]),t2))
                        else:
                            doc.add(Field(line[0], ' '.join(line[1:]),t1))
            writer.addDocument(doc)
            file.close()
            i += 1
            print i


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    IndexFiles('files', "index")
    end = datetime.now()
    print end - start

