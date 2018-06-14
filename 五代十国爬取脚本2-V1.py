#encoding=utf-8
#作者：大捷龙   csdn : http://blog.csdn.net/koanzhongxue
#http://bbs.tianya.cn/post-no05-440048-1.shtml
#获取天涯的帖子内容
import urllib,urllib2,re

#url ='http://bbs.tianya.cn/post-no05-440048-1.shtml'
url ='http://bbs.tianya.cn/post-no05-440048-1.shtml'
link = urllib2.urlopen(url)
html = link.read()
#获取帖子的基本信息
#正则表达式，用于提取文章标题
gettitle = re.compile(r'<title>(.*?)</title>')
#title是一个tuple,相当于一个数组，需要遍历取出其中的元素进行字符转换
title = re.findall(gettitle,html)
#title中的字符是utf_8型的 
for s in title:
  if isinstance(s, unicode): 
    print "unicode"+s.encode('gb2312') 
  else:
    print "utf-8"+s.decode('utf-8').encode('gb2312')

#正则表达式匹配HTML中的最大页数的信息。
getmaxlength = re.compile(r'<a href=".*?">(\d*)</a>\s*<a href=".*?"\s*class=.*?>下页</a>')
#用正则获取最大页数信息
maxlength = getmaxlength.search(html).group(1)
print u"最大页数："+maxlength

#*************************************************************************
#正则匹配 除所有的帖子内容
#每一页除第一个帖子以外的所有帖子
gettext = re.compile(r'<div class="bbs-content">\s*([\S\s]*?)\s*</div>')  #[\S\s]匹配任意字符
#gettext1:每一页的第一个帖子
gettext1 = re.compile(r'<div class="bbs-content clearfix">\s*(.*?)\s*</div>')
getpagemsg = re.compile(r'<div class="atl-info">\s*<span>(.*?)<a href="http:.*uname="(.*)">.*\s*<span>时间：(.*?)</span>')
getnextpagelink = re.compile(r'<a href="(.*?)"\s*class.*?>下页</a>')
#遍历每一页,获取发帖作者，时间，内容，并打印
#re.sub('[\/:*?"<>|]','-',title[0])去掉非法字符  
filepath ='F:\python\tianyacode\\'+re.sub('[\/:*?"<>|]','-',title[0])+'.txt' #utf-8编码，需要转为gbk .decode('utf-8').encode('gbk')
filehandle = open(filepath.decode('utf-8').encode('gbk'),'w')

#打印文章标题
print "title[0]:"+title[0].decode('utf-8').encode('gbk')
print "filePath:"+ filepath.decode('utf-8').encode('gbk')

filehandle.write(title[0].decode('utf-8','ignore').encode('gbk','ignore') +'\n')

str1 = ""
tempstr = "tempstr"
print int(maxlength)+1
#x=input()
for pageno in range(1,int(maxlength)+1):
  #tempstr = tempstr + pageno 为什么这里不能加这句语句，一加就报错
    i = 0
    filehandle.write('\n\n\n\n\n')    
    str1 = '============================'+'第 '+ str(pageno)+' 页'+'=============================='
    filehandle.write(str1.decode('utf-8','ignore').encode('gbk','ignore') +'\n')
    #获取每条发言的信息头，包含作者，时间
    pagemsg = re.findall(getpagemsg,html)
    if  pageno is 1:
        #获取第一个帖子正文
        text1 = re.findall(gettext1,html)
         #因为第一条内容由text1获取，text获取剩下的，所以text用i-1索引
    #获取帖子正文
    text = re.findall(gettext,html)    
    #ones:页码遍历基数
    for ones in pagemsg:
        if pageno > 1:
            if ones is pagemsg[0]:
                continue   #若不是第一页，跳过第一个日期
              #ones[0]是第pageno行的pagemsg的第0列
        if 'host' in ones[0]:
            str1= '楼主：'+ ones[1] +'     时间:' + ones[2]
            #filehandle.write(str1.decode('utf-8','ignore').encode('gbk','ignore') +'\n')            
        else:           
            str1= ones[0] + ones[1] + '    时间:' + ones[2]
            #filehandle.write(str1.decode('utf-8','ignore').encode('gbk','ignore') +'\n')
    filehandle.write('111111111111' +'\n')
    break
    if  pageno is 1: #第一页特殊处理
        if i is 0:
            str1= text1[0].replace('<br>','\n')
            #filehandle.write(str1.decode('utf-8','ignore').encode('gbk','ignore') +'\n')
            filehandle.write('text0' +'\n')
        else:
            str1 = text[i-1].replace('<br>','\n')
            #filehandle.write(str1.decode('utf-8','ignore').encode('gbk','ignore') +'\n')
            filehandle.write('text1' +'\n')    
    else:  #非第一页的处理
        filehandle.write('text2' +'\n')
        break    
        '''try:
            str1 =  text[i].replace('<br>','\n')
            filehandle.write(str1.decode('utf-8','ignore').encode('gbk','ignore') +'\n')                  
        except IndexError,e:
            print 'error occured at >>pageno:'+str(pageno)+'   line:'+str(i)
            print '>>'+text[i-1]
            print e'''


                                
    i = i +1    
    if pageno < int(maxlength):
        #获取帖子的下一页链接，读取页面内容
        nextpagelink = 'http://bbs.tianya.cn'+getnextpagelink.search(html).group(1)
        link = urllib2.urlopen(nextpagelink)
        html = link.read() 
filehandle.close()

#tempstr.decode('utf-8','ignore').encode('gbk','ignore')

x=input()
