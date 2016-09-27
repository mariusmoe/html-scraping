from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
from time import sleep
from config import *

myBigList = []

_strakkId = 7743
def html_scraping(strakkId):
	html = urlopen( url_part1 + str(strakkId) + url_part2)
	bsObj = BeautifulSoup(html)
	# Grab data in lists
	titles = bsObj.findAll("h1", {"class":"pname"})
	intros = bsObj.findAll("div", {"class":"pattern_intro"})
	prices = bsObj.findAll("p", {"class":"cost1"})
	txts = bsObj.findAll("div", {"class":"pattern_text"})
	oteherImg = bsObj.findAll("img")

	# try to find cover photo - regex thet select all imglinks with '/drops/mag' and ends with .jpg
	images = bsObj.findAll("img", {"src":re.compile('/drops/mag.*\.jpg')})
	print("-------------")
	# print(images)
	#the shortes url matching is always cover photo
	shortestImgUrl = len(images[0]["src"])
	target = images[0]["src"]   # target is the cover photo
	for image in images:
	    if len(image["src"]) < shortestImgUrl:
	        shortestImgUrl = len(image["src"])
	        target = image["src"]
	print("###############")
	print(target)

	# write cover photo to file
	resource = urlopen( url_img + target)
	output = open("img/cover/c" + str(strakkId) + ".jpg","wb")        # write binary
	output.write(resource.read())
	output.close()


	print("^^^^^^^^^^^^")
	thisDatapoint = []
	# becouse title is in a list we have to unpack it to be able to use get_text()
	for title in titles:
	    print(title.get_text().strip())     # remove leading spaces, have been a problem
	    thisDatapoint.append(str(title.get_text().strip()))
	for intro in intros:
	    print(intro.get_text())
	    thisDatapoint.append(str(intro.get_text()))
	for txt in txts:
	    print(txt.get_text())
	    thisDatapoint.append(txt.get_text())
	for price in prices:
	    print(price.get_text())
	    thisDatapoint.append(price.get_text())
	thisDatapoint.append("img/cover/c" + str(strakkId) + ".jpg")


	myBigList.append(thisDatapoint)

for n in range(1000,1020):
	try:
		html_scraping(n)
	except:
		pass
	sleep(1)


with open("output.csv", "a", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['title','intro','txt','price','img'])
    writer.writerows(myBigList)