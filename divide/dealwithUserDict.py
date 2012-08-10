#encoding=utf-8


f=open('ICTCLAS.txt','r')
i=1
filename='Ciku%s.txt'
out=open(filename%i,'w')
amount=len(f.readlines())
print amount
f.close()
f=open('ICTCLAS.txt','r')
part=amount/10+1
line=0
while True:
    text=f.readline()
    if len(text)==0:
        break
    line+=1
    if (line<part*i) and line>part*(i-1):
        out.flush()
        out=open(filename % i,'w')
        i+=1
    out.write(text)
f.close()
#out.close()
