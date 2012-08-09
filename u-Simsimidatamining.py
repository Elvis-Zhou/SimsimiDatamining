#!/usr/bin/python
# -*- coding:utf-8 -*-
#encoding = utf-8
#import string
import urllib ,urllib2
import re

urllib2.socket.setdefaulttimeout(30)
f=open('ICTCLAS.txt','r')
out=open('Datamining.txt','a')
count=0
def searchsimsimi(keyword):
    #titles=[]
    #values = {
    #"msg":keyword
    #}
    #data = urllib.urlencode(values)
    url_ws='http://www.simsimi.com/func/req?lc=zh&msg='
    #keyword=urllib.urlencode(keyword,'utf-8')
    request = urllib2.Request(str(url_ws)+keyword)
    print keyword
    request.add_header("Referer","http://www.simsimi.com")
    t=0
    while t<30:
        try:
            t=t+1
            result = urllib2.urlopen(request).read()
            break
        except BaseException:
            pass
        finally:
            if t>=30:
                print "error"+str(t)
    
    #print result
    word=""
    try:
        word=eval(result)["response"]
        print word
        words=word
        words=words.replace("&","&amp")
        words=words.replace("<","&lt")
        words=words.replace(">","&gt")        
        words=words.replace("'","&apos")
        words=words.replace('"',"&quot")
        
        writetoaiml(keyword,words)
        return word
    except BaseException:
        return word
    return word

def writetoaiml (input,output):
    global out,count
    out.write("  <category>\n")
    out.write("    <pattern>")
    out.write(input)
    out.write("</pattern>\n")
    out.write("    <template>\n")
    out.write(output+'\n')
    out.write("    </template>\n")
    out.write("  </category>\n")
    out.flush()
    count=count+1
    print count
    
if __name__=='__main__':
    while True:
        text=f.readline().strip()
        if len(text)==0:
            break
        i=0
        word=text
        temp=""
        wordlist=[]
        while True:
            #global word
            extemp=temp
            temp=word
            word=searchsimsimi(word.replace(' ','+'))
            i=i+1
            if word=="":
                break
            if temp==word:
                break
            if extemp==word:
                break
            if word in wordlist:
                break
            if  i>=500:
                break
            wordlist.append(word)
    print "finish"
    f.close()
    out.close()

