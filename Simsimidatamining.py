#!/usr/bin/python
# -*- coding:utf-8 -*-
#encoding = utf-8
#import string
import urllib ,urllib2
from jianfan import jtof, ftoj

urllib2.socket.setdefaulttimeout(30)
f=open('SougouCiku.txt','r')
out=open('Datamining1.txt','a')
count=0

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
    while t<5:
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
        finally:
            if t>=5:
                print "error"+str(t)+"  :"+keyword
                break
    #return wordset
    #print result
    return wordset

def dealrequest(result):
    word=""
    try:
        word=eval(result)["response"]
        #print word
        words=word
        #writetoaiml(keyword,words)
        return words
    except BaseException:
        return words

def writetoaiml (input,outputset):
    global out,count
    out.write("  <category>\n")
    out.write("    <pattern>")
    #out.write(input)
    words=input.replace("&","&amp;")
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
    
if __name__=='__main__':
    while True:
        text=f.readline().strip()
        if len(text)==0:
            break
        i=0
        word=text
        temp=""
        wordset=set() #当前索引词的大集合
        wordlist=set() #目前放进去词搜索产生的集合，也就是要接下来搜索
        wordlist1=set() #临时存储2级结点生成的词典
        wordlist2=set() #临时当前词simsimi返回生成的当前词典
        wordlist.add(word)
        #print wordlist

        while True:
            wordlist1=wordlist.copy()
            for word in wordlist:
                wordlist1.remove(word)
                #print word
                #word="力量"
                wordlist2=searchsimsimi(word.replace(' ','+'))
                #print wordlist
                if len(wordlist2)==0:
                    break
                if (wordset&wordlist2)==wordlist2:
                    break
                wordlist1|=wordlist2
                if len(wordlist2)>0:
                    writetoaiml(word,wordlist2)
                    wordset.add(word)

            i += 1
            wordset|=wordlist1
            wordlist=set()|wordlist1
            if len(wordlist)==0:
                break
            if  i>=12:
                print "i到达指定层数 break"
                break
    print "finish"
    f.close()
    out.close()

