#!/usr/bin/python
# -*- coding:utf-8 -*-
#encoding = utf-8
#import string
import urllib2
import threading
from jianfan import ftoj
from Queue import Queue

urllib2.socket.setdefaulttimeout(30)
cookie="sagree=true; selected_nc=ch; JSESSIONID=A27B1B45016B6242EE7D3A9E829E91C6; __utma=119922954.1058608435.1343057253.1344838700.1344874176.3; __utmb=119922954.3.9.1344874201643; __utmc=119922954; __utmz=119922954.1343057253.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)"
cookie2="sagree=true; selected_nc=ch; JSESSIONID=C6C18F376C2ED1D571B99F3BD50C7A1C; __utma=119922954.1058608435.1343057253.1344838700.1344874176.3; __utmb=119922954.4.9.1344874929222; __utmc=119922954; __utmz=119922954.1343057253.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)"
filename="Ciku%s.txt"
outfilename='Datamining%s.txt'
outlongfilename='Datamining%s-long.txt'
filecount=1
f=open(filename % filecount,'r')
out=open(outfilename % filecount,'a')
out2=open(outlongfilename % filecount,'a')
maxwordlength=40
maxthreads=20
count=0
maxretry=6
#treedeep=1
lock1=threading.RLock()
lock2=threading.RLock()
threads=Queue(maxthreads)
def searchsimsimi(keyword):

    url_ch='http://www.simsimi.com/func/req?lc=ch&msg='
    url_zh='http://www.simsimi.com/func/req?lc=zh&msg='
    request = urllib2.Request(str(url_ch)+keyword)
    request2 = urllib2.Request(str(url_zh)+keyword)
    request.add_header("Referer","http://www.simsimi.com/talk.htm")
    request.add_header("Cookie",cookie)
    request2.add_header("Referer","http://www.simsimi.com/talk.htm")
    request2.add_header("Cookie",cookie2)
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
            if t>3:
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
        self.wordset=set() #当前答案
        self.word=""

    def run(self):
        #self.i=0
        self.word=threads.get(1,10)
        try:
            self.wordset=searchsimsimi(self.word)
            if len(self.wordset)>0 :
                if len(self.word.strip())<=maxwordlength:
                    lock1.acquire()
                    writetoaiml(self.word,self.wordset)
                    lock1.release()
                else:
                    lock2.acquire()
                    writetoaiml2(self.word,self.wordset)
                    lock2.release()
            else:
                pass
        except BaseException:
            pass

        threads.task_done()


if __name__=='__main__':
    #global f,out,out2,filename,filecount
    for filecount in range(1,11):
        f=open(filename % filecount,'r')
        out=open(outfilename % filecount,'a')
        out2=open(outlongfilename % filecount,'a')
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
out2.close()

