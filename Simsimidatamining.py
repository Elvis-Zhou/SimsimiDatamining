#!/usr/bin/python
# -*- coding:utf-8 -*-
#encoding = utf-8
#import string
import urllib2
import threading
from jianfan import ftoj
from Queue import Queue

urllib2.socket.setdefaulttimeout(30)
f=open('Ciku1.txt','r')
out=open('Datamining1.txt','a')
out2=open('Datamining1-long.txt','a')
maxwordlength=40
maxthreads=2
count=0
maxretry=2
treedeep=2
lock1=threading.RLock()
lock2=threading.RLock()
threads=Queue(maxthreads)
def searchsimsimi(keyword):
    #titles=[]
    #values = {
    #"msg":keyword
    #}
    #data = urllib.urlencode(values)
    url_ch='http://www.simsimi.com/func/req?lc=ch&msg='
    url_zh='http://www.simsimi.com/func/req?lc=zh&msg='
    #keyword=urllib.urlencode(keyword,'utf-8')
    request = urllib2.Request(str(url_ch)+keyword)
    request2 = urllib2.Request(str(url_zh)+keyword)
    #print keyword
    request.add_header("Referer","http://www.simsimi.com")
    request2.add_header("Referer","http://www.simsimi.com")
    t=0
    wordset=set()
    while t<maxretry:
        try:
            t+=1
            result = urllib2.urlopen(request).read()
            result2 = urllib2.urlopen(request2).read()
            result=dealrequest(result)
            result2=dealrequest(result2)
            wordset.add(result)
            wordset.add(result2)
            if t>4:
                return wordset
                #break
        except BaseException:
            pass

        if t>=maxretry:
            print "error:"+str(t)+" :"+keyword
            return wordset
                #break
    #return wordset
    #print result
    return wordset

def dealrequest(result):
    word=""
    try:
        word=eval(result)["response"]
        return word
    except BaseException:
        return word

def writetoaiml (input,outputset):
    global out,count
    out.write("  <category>\n")
    out.write("    <pattern>")
    words=ftoj(input.decode('utf-8')).encode('utf-8')
    words=words.replace("&","&amp;")
    words=words.replace("<","&lt;")
    words=words.replace(">","&gt;")
    words=words.replace("'","&apos;")
    words=words.replace('"',"&quot;")
    out.write(words)
    out.write("</pattern>\n")
    out.write("    <template>\n")
    if len(outputset)>=1:
        out.write("      <random>\n")
        for x in outputset:
            print input
            print ftoj(x.decode('utf-8')).encode('utf-8')
            out.write("        <li>")
            words=x.replace("&","&amp;")
            words=words.replace("<","&lt;")
            words=words.replace(">","&gt;")
            words=words.replace("'","&apos;")
            words=words.replace('"',"&quot;")
            words=ftoj(words.decode('utf-8')).encode('utf-8')
            out.write(words)
            out.write("</li>\n")
            count += 1
        out.write("      </random>\n")
    else:
        print input
        x=outputset.pop()
        print ftoj(x.decode('utf-8')).encode('utf-8')
        words=x.replace("&","&amp;")
        words=words.replace("<","&lt;")
        words=words.replace(">","&gt;")
        words=words.replace("'","&apos;")
        words=words.replace('"',"&quot;")
        words=ftoj(words.decode('utf-8')).encode('utf-8')
        out.write(words+'\n')

        count += 1
    out.write("    </template>\n")
    out.write("  </category>\n")
    out.flush()
    #count += 1
    print count

def writetoaiml2 (input,outputset):
    global out,count
    out2.write("  <category>\n")
    out2.write("    <pattern>")
    words=ftoj(input.decode('utf-8')).encode('utf-8')
    words=words.replace("&","&amp;")
    words=words.replace("<","&lt;")
    words=words.replace(">","&gt;")
    words=words.replace("'","&apos;")
    words=words.replace('"',"&quot;")
    out2.write(words)
    out2.write("</pattern>\n")
    out2.write("    <template>\n")
    if len(outputset)>=1:
        out2.write("      <random>\n")
        for x in outputset:
            print input
            print ftoj(x.decode('utf-8')).encode('utf-8')
            out2.write("        <li>")
            words=x.replace("&","&amp;")
            words=words.replace("<","&lt;")
            words=words.replace(">","&gt;")
            words=words.replace("'","&apos;")
            words=words.replace('"',"&quot;")
            words=ftoj(words.decode('utf-8')).encode('utf-8')
            out2.write(words)
            out2.write("</li>\n")
            count += 1
        out2.write("      </random>\n")
    else:
        print input
        x=outputset.pop()
        print ftoj(x.decode('utf-8')).encode('utf-8')
        words=x.replace("&","&amp;")
        words=words.replace("<","&lt;")
        words=words.replace(">","&gt;")
        words=words.replace("'","&apos;")
        words=words.replace('"',"&quot;")
        words=ftoj(words.decode('utf-8')).encode('utf-8')
        out2.write(words+'\n')

        count += 1
    out2.write("    </template>\n")
    out2.write("  </category>\n")
    out2.flush()
    #count += 1
    print count


class DMthread(threading.Thread):
    global threads
    def __init__(self):
        threading.Thread.__init__(self)
        self.wordset=set() #当前索引词的大集合
        self.wordlist=set() #目前放进去词搜索产生的集合，也就是要接下来搜索
        self.wordlist1=set() #临时存储2级结点生成的词典
        self.wordlist2=set() #临时当前词simsimi返回生成的当前词典
        self.i=0
        self.word=""

    def run(self):
        self.i=0
        self.word=threads.get(1,10)
        self.wordlist.add(self.word)

        while True:
            self.wordlist1=self.wordlist.copy()
            for word in self.wordlist:
                self.wordlist1.remove(word)
                #print word
                #word="力量"
                self.wordlist2=searchsimsimi(word.replace(' ','+'))
                #print wordlist
                if not len(self.wordlist2):
                    break
                if (self.wordset&self.wordlist2)==self.wordlist2:
                    break
                self.wordlist1|=self.wordlist2
                if len(self.wordlist2)>0:
                    self.wordset.add(word)
                    if len(word.strip())<=maxwordlength:
                        lock1.acquire()
                        writetoaiml(word,self.wordlist2)
                        lock1.release()
                    else:
                        lock2.acquire()
                        writetoaiml2(word,self.wordlist2)
                        lock2.release()
            self.i += 1
            self.wordset|=self.wordlist1
            self.wordlist=set()|self.wordlist1
            if not len(self.wordlist):
                #threads.task_done()
                break
            if  self.i>=treedeep:
                print "treedeep arrive:"+str(treedeep) + " break at keyword: "+self.word,"  "
                print self.wordlist1
                break
        threads.task_done()


if __name__=='__main__':

    #count=0
    while True:
        text=f.readline().strip()
        if len(text)==0 and (threads.qsize()>0):
            k=threads.qsize()
            for j in range(0,k):
                try:
                    t=DMthread()
                    t.start()
                except RuntimeError:
                    print "threads had started "
            threads.join()
            #threads.remove(t)
            #count=0
        if len(text)==0 and (threads.qsize()==0):
            break

        if threads.qsize()<maxthreads:
            #t=DMthread()
            threads.put(text,1)
            #count+=1
        if threads.qsize()>=maxthreads:
            k=threads.qsize()
            for j in range(0,k):
                try:
                    t=DMthread()
                    t.start()
                    #threads.task_done()
                except RuntimeError:
                    print "threads had started "
            threads.join()
            #count=0
            #threads=[]
    print "finish"
    f.close()
    out.close()

