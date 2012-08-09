#encoding=utf-8
__author__ = 'zxz'
#import string

f=open('SougouCiku.txt','r')
out=open('ICTCLAS.txt','w')
out2=open('MMSEG.txt','w')
while True:
    text=f.readline()
    if len(text)==0:
        break
	searchsimsimi(text)

    out.write(dealedtext)
    out2.write(str((len(dealedtext)-1)/3)+' '+dealedtext)

f.close()
out.close()
out2.close()


def searchsimsimi(keyword):
    titles=[]
    url_ws='http://www.simsimi.com/func/req?lc=zh&msg='
    #urllib2.Request()
    request = urllib2.Request(str(url_ws)+keyword)
    request.add_header("Referer","http://www.simsimi.com")
    #request.add_header('Accept', 'application/json')
    #request.get_method = lambda: 'PUT'
    result = urllib2.urlopen(request).read()
    print result
    try:
        print eval(result)["response"]
    except BaseException:
        print "小黄鸡也不知道"
	