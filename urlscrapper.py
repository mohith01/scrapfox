import requests
import re
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import messagebox
import os
import pandas as pd
def filetext():
	os.system('gedit /home/s4i/temp/mangascript/geek.txt &')

window = tk.Tk()
window.geometry("200x200")

clean = re.compile('<.*?>')

def format(input1):
	temp1 = []
	b = input1.replace('//',' ').replace(':',' ').replace("'"," ").split()
	for i in range(len(b)):
		temp = list(b[i])
		e = []
		for j in range(len(temp)):
			if temp[j].isalpha() or temp[j].isnumeric() or temp[j]=='-':
				e.append(temp[j])
		temp1.append(''.join(e))
	return '-'.join(temp1).lower()
			
	

def remove_html(text):
	temp1 = []
	for i in text:
		temp1.append(re.sub(clean,'',i))
	return temp1

	
def soup_to_list(rem):
	return [str(i) for i in rem]



def float_or_int(num):
	return int(float(num)) if int(float(num)) == float(num) else float(num)



def scrap(manga):
	temp1 = requests.get(manga)
	soup = BeautifulSoup(temp1.content,features="html.parser")
	x = soup.find('div',attrs={'class':'_3QCtP col-md-9 col-sm-8 col-xs-6'})
	a1 = list(x)[0]
	a2 = list(x)[1]
	y1 = remove_html(soup_to_list(a2.findAll('span',{'class':'_3SlhO'})))
	y2 = remove_html(soup_to_list(a2.findAll('span',{'class':''})))
	y2[-1] = float_or_int(y2[-1].split(' ')[-1])
	res = dict(zip(y1,y2))
	res['alt_name'] = None if len(list(a1.small))==0 else list(a1.small)[0].split(';') 
	res['genre'] = remove_html(soup_to_list(a2.findAll('a',{'class':'label genre-label'})))
	return res



def results(url):
	list1 = []
	temp1 = requests.get(url)
	soup2 = BeautifulSoup(temp1.content,features="html.parser")
	y = soup2.find_all('div',attrs={'class':'_1KYcM col-sm-6 col-xs-12'})
	for i in y:
		list1.append(i.findAll('a',href=True)[0]['href'])
	return list1


#csv_columns = ['No','Name','Country'] #shd be changed
#csv_file = "Names.csv"
#try:
#    with open(csv_file, 'w') as csvfile:
#        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#        writer.writeheader()
#        for data in dict_data:
#            writer.writerow(data)
#except IOError:
#    print("I/O error")

#try:
#     with open(csv_file,'w') as cv:
#             writer = csv.DictWriter(cv,fieldnames=csv_rows)
#             writer.writeheader()
#             for i in range(1,15):
#                     for j in results("https://mangafox.fun/search/page/"+str(i)+"?q=&order=ALPHABET&genre=all"):
#                             writer.writerow(scrap(j))
# except IOError:
#     print("I/O error")

df = pd.read_csv("/home/s4i/temp/mangascript/hi.csv")


def temp1(test,test2):
	try:
		res = scrap("https://mangahub.io/manga/"+format(test))
		if res['Latest']>test2:
			return res['Latest']
		else:
			return test2
	except:
		if test[0]=='#':
			return test2

def update():
	df['ChapRead'] = pd.Series(list(map(temp1,df['Manga'],df['ChapRead'])))
	df.to_csv('/home/s4i/temp/mangascript/hi.csv',index=None)

file1 = open('/home/s4i/temp/mangascript/geek.txt','a')
file1.truncate(0)
count=0
with open('/home/s4i/temp/mangascript/hi.csv') as mangafile1:
	csv_reader = csv.DictReader(mangafile1)
	for row in csv_reader:
		if row['Manga'][0]=='#':
			print(row['Manga'])
			pass
		else:
			print(row['Manga'])
			res = scrap("https://mangafox.fun/manga/"+format(row['Manga']))
			if res['Latest']-float_or_int(row['ChapRead'])>0:
				count+=1
				file1.write("The manga "+row['Manga']+" from Chap "+row['ChapRead']+ ' '+str(res['Latest']-float_or_int(row['ChapRead'])) +' chaps to read\n')
file1.close()
if (count>0):
	messagebox.showinfo('Mangas','You have '+str(count) +' mangas updated.Check the geek.txt file')
	b = tk.Button(window,text="The text file list",justify='center',padx=2,pady=2,command=filetext)
	b.pack()
	b2 = tk.Button(window,text="Update stuff",justify='center',padx=2,pady=4,command=update)
	b2.pack()
	window.mainloop()	


#https://mangafox.fun/search/page/2?q=&order=ALPHABET&genre=all
#813 pages




