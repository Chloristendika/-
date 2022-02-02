from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import time
import os
import re

url = "https://www.chinanews.com.cn"
cnt = 0

def getNews():
	html = urlopen(url + '/world')
	bs = BeautifulSoup(html.read(), 'html.parser', from_encoding = "GBK")
	newsList = bs.find_all('a', href = re.compile('^(/gj/)(.)*(.shtml)$'))
	for new in newsList:
		newLink = url + new.attrs['href']
		#print(newLink)
		getPage(newLink)
		#print(new.get_text())

def getPage(link):
	global cnt # 新闻计数
	html = urlopen(link)
	bs = BeautifulSoup(html.read(), 'html.parser')
	Title = bs.find('input', {'id': 'newstitle', 'name': 'newstitle', 'type': 'hidden'})
	if Title == None:
		return None
	try:
		newsTitle = Title.attrs['value']
	except AttributeError as e:
		print(Title)
	#print(newsTitle)
	Contents = bs.find_all('p')
	# print(len(Contents))
	day = time.strftime("%Y-%m-%d", time.localtime())
	try:
		os.mkdir('D:/News/' + day)
	except FileExistsError as e:
		pass
	Path = 'D:/News/' + day + '/'
	filename = day + '-News' + str(cnt + 1) + '.txt'
	#print(Path + filename)
	f = open(Path + filename, 'w', encoding = 'utf-8')
	f.write(newsTitle + '\n' + '\n') # 打印标题
	for content in Contents:
		if 'class' in content.parent.attrs:
			if content.parent.attrs['class'] == ['left_zw']:
				f.write('  ') # 打印段首空格
				con = content.get_text().strip(' ')
				Length = len(con); point = 0
				while point <= Length - 1: # 每段每行最多30词，每段分行打印
					f.write(con[point : min(point + 30, Length)] + '\n')
					point += 30

	cnt += 1


if __name__ == '__main__':
	getNews()