#!/usr/bin/python
# chengsq123@gmail.com


import os

import re 
import urllib
import urllib2 
import cookielib
from BeautifulSoup import *
import time 
from urllib2 import URLError,HTTPError 

def Debugprint(info):
	debug = 1
	if debug:
		print info


def logfilewrite(info):
	logfile = open("log.txt",'a+')
	info = str(info)+'\r\n'
	logfile.write(info)
	
	

class Renren:
	def __init__(self,debug = 0):
		self.debug = debug
		if self.debug :
			print "__init__ exited "
		return 

	def  login(self,logfile_name,user,passwd):
		#logfile.write(str(datatime.datatime.now())+ 'renren/r/n')
		cj = cookielib.CookieJar()
		post_data = urllib.urlencode({'email':user,'password':passwd,'origURL':'http://www.renren.com/Home.do','domain':'renren.com'})
		path = "http://www.renren.com/PLogin.do" 
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		self.opener = opener
		urllib2.install_opener(opener)
		req = urllib2.Request(path,post_data)
		
		
		#print req
		logfile = open("log.txt",'w')
		try:
		   conn = urllib2.urlopen(req)
		except URLError,e:
			print "UrlError"
			logfile.write("URlError:"+str(e.code)+'/r/n')
			return False
		except HTTPError,e:
			print "HTTPError"
			logfile.write("HTTPError:"+str(e.code)+'/r/n')
			return False	
			
		if self.debug:
			print self.home_page 
		if conn.geturl() == "http://www.renren.com/222097841":
			print "success"
			logfile.write("login success"+conn.geturl()+'\r\n')
			self.home_page = conn.geturl()
			self.content = conn.read()
			if self.debug:
			  print self.content
			#open('login_renren.html','w').write(conn.read())
			return  
		else: 
			print "login failed"
			logfilewrite("login faild /r/n")
			return 	
	

	def get_opener(self):
		return 	self.opener 
		
        def get_homepage(self):
		if self.debug:
		   print self.home_page
		return self.home_page
		
	def get_content(self):
		return  self.content	

	def open(self,url):
		conn = urllib2.urlopen(url)
		data = conn.read()
	        return data	
	        
class albummain():
	def __init__(self,data):
		self.url = []
		self.soup = BeautifulSoup(data)
		#self.resp =resp
	        return 


	def get_AlbumOwner(self):
		owner = self.soup.findAll('title')
		self.owner = owner[0].string 
		#print owner[0].string
		return owner
		
	def get_AlbumInfo(self):
		AlbumInfo = self.soup.findAll("a",attrs={'class':'album-title'})
		#print len(AlbumInfo),AlbumInfo
		return AlbumInfo


	def MakeOwnerDir(self):
		dirname = str(self.owner)
		if not os.path.exists(dirname):
                	os.makedirs(dirname)

	def  downloadAlbums(self):
		AlbumInfo = self.get_AlbumInfo()
		#print "ccccc",AlbumInfo
		i = 0
		owner = self.get_AlbumOwner()
		#print owner[0].string
		self.MakeOwnerDir()
		while (i < len(AlbumInfo)):
			al =albumInfo(AlbumInfo[i])
			Debugprint(al.get_AlbumUrl())
			aldata = al.get_AlbumPage()
			name = al.get_AlbumName()
			print name
			path = self.owner + str('/')
			name =str(i+1)+str('--')+name
			absname = path + name
			album = albums(aldata,absname)
			album.AlbumDir()
			album.downloadAlbum()
			i = i + 1		

	def photoCount(self):
		AlbumInfo = self.get_AlbumInfo()
		self.photoCount = 0
		i = 0
		while(i < len(AlbumInfo)):
			al =albumInfo(AlbumInfo[i])
			al.get_AlbumUrl()
			aldata = al.get_AlbumPage()
			album = albums(aldata,'')
			album.photo()
			self.photoCount = self.photoCount +album.AlbumPhotoCount()
			#print self.photoCount
		return self.photoCount

	def get_anchor(self):
		soup = self.soup
		a = soup.findAll('a')
		self.a = a
		return a
	
	def get_url(self):
		a= self.a
		print len(a)
		i = 0
		link = []
		while(i < len(a)):
			href = a[i]['href']
			#print href 
			if re.match('http://share.*',href) is not None:
				 link.append(href)
		
			i += 1
		self.link = link
		return self.link
		
class  albumInfo():
	
	def __init__(self,info):
		self.info = info
		#print 'albumInfo-->',info
	
	def get_AlbumName(self):
		info = self.info
		#print len(info), info.span.string
		album_name = info.span.string
		if album_name is not None:
			#print album_name
			return album_name.strip()
		else:
		    	#print "cccccc",info.span
			return "ccc"

	def get_AlbumUrl(self):
		url = self.info['href'] 
		self.url = url
		#print 'albumInfo---get_AlbumUrl',url
		return url
		

	def get_AlbumPage(self):
		url = self.url
		conn = urllib2.urlopen(url)
		return conn.read()

class photo:
	def __init__(self,url,savedpath):
		self.url = url
		self.path = savedpath

	def absfilename(self,url):
		filename = url.split('/')
		absfilename = str(self.path)+'/'+filename[-1]
		return absfilename
		
	def download(self):
		url = self.url
		conn = urllib2.urlopen(url)
		data = conn.read()
		soup = BeautifulSoup(data)

		photourl = soup.findAll('div',attrs={'class':'photo-img'})[0].img['src']
		print photourl
		
		filename = self.absfilename(photourl)
		print  filename
		
		logfilewrite(photourl)
		try:
	  		conn = urllib2.urlopen(photourl)
		except HTTPError,e:
			print "HTTPError"
			logfilewrite("HTTPError")
			return

		file_ref = open(filename,'w')
		file_ref.write(conn.read())

			


class albums():
	def __init__(self,albuminfo,album):
		self.info = albuminfo
		#print self.info
		self.count = 0
		self.album = album
		self.soup = BeautifulSoup(albuminfo)
		self.photo()
	
	def AlbumDir(self):
		dirname = str(self.album)
		if not os.path.exists(dirname):
                	os.makedirs(dirname)
		
	def photo(self):
		photoInfo = self.soup.findAll("a",attrs={'class':'picture'})
		self.count = len(photoInfo) 
		self.photoInfo = photoInfo
		return photoInfo

	def photoUrl(self):
		i = 0
		self.photoUrl = []
		while(i < self.count):
			url =self.photoInfo[i]['href']
			#print 'photoUrl--->',url
			self.photoUrl.append(url)
			i = i + 1
		#print self.photoUrl
		return  self.photoUrl

	def downloadAlbum(self):
		self.AlbumDir()
		albumpath = self.album
		self.photo()
		url = self.photoUrl()
		#print "downloadAlbum   --->",url
		
		i = 0
		while(i < self.count):
			#print  url[i]
			p = photo(url[i],albumpath)
			p.download()
			i = i + 1
						
		print "downloadAlbum   ---> ",str(albumpath)

	def AlbumPhotoCount(self):
		return self.count

	def download_main_photo(self):
	    i = 0
	    self.AlbumDir()
	    while(i < self.count):
		url =self.photoInfo[i].img['data-src']
		large_url = url.replace('main','large') 
		absfilename = url.split('/')
		filename = str(self.album)+'/'+absfilename[-1]
		print  filename
		print  url,large_url
		
		try:
	  		conn = urllib2.urlopen(url)
		except URLError,e:
			print "URlError"
			continue
		except HTTPError,e:
			print "HTTPError"
			continue

		file_ref = open(filename,'w')
		file_ref.write(conn.read())
		i = i + 1
		#return conn.read()
		


			


def main():
	begin_time = time.time()
	print  begin_time
	csq = Renren(0)
	csq.login("csq.txt","chengshiqing123@163.com","wawj0539")
	print "csq _homepage :",csq.get_homepage()
 	print 'time-cost:'+str(time.time()-begin_time)	

	
	photo = csq.open("http://photo.renren.com/photo/222362991/album/relatives")# chen hao jie	
	photo = csq.open('http://photo.renren.com/photo/237827221/album/relatives')# wang xun yang
	photo = csq.open("http://photo.renren.com/photo/258183175/album/relatives")
	album_main = albummain(photo)
		
	anchor = album_main.get_anchor()
	link = album_main.get_url()
	albuminfo = album_main.get_AlbumInfo()
	album_main.downloadAlbums()
	#print 'photo count :',album_main.photoCount()	
	print 'time-cost:'+str(int(time.time()-begin_time))	
if __name__ == '__main__': main()
	

#print data


























