import lxml.html
import urllib
import re
import requests
import sqlite3
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
dict={}
db = sqlite3.connect('olxhondacity_Sele.db')

def intodb(make,model,year,kilo,price):
    
    cursor = db.cursor()
    params = (make,model,year,kilo,price)
    cursor.execute('''CREATE TABLE IF NOT EXISTS
                         cars(make TEXT, model TEXT,year TEXT,kilo TEXT,price TEXT)''')
    cursor.execute("INSERT INTO cars VALUES(?,?,?,?,?)", params)
    db.commit()

def assign(dict):
	print dict
	try:
		m_make = dict['Make:']
	except:
		m_make = "None"
	try:
		m_model = dict['Model:']
	except:
		m_model = "None"
	try:
		m_year = dict['Year:']
	except:
		m_year = "None"
	try:
		m_kilo = dict['kms']
		m_kilo = m_kilo[1:-1]
	except:
		m_kilo = "None"
	try:
		m_price = dict['price']
		m_price = m_price[1:-1]
	except:
		m_price = "None"
	
	intodb(m_make,m_model,m_year,m_kilo,m_price)
	


def scrap(page):
	#page = requests.get(url)
	#print page
	#print page.text
	doc = lxml.html.document_fromstring(page)
	year = ""
	make = ""
	model = ""
	kilo = ""
	price = ""

	for i in range(1,31):
		assign(dict)
		dict.clear()

		try:
			price_xpath = '//*[@id="itemListContent"]/div/div['+str(i)+']/div[2]/div[2]/span[2]/text()'
			price_text = doc.xpath(price_xpath)
			price_t = price_text[0]
			price = price_t.split()
			price.append("price")
			dict[price[1]] = price[0]
		except:
			price = "N/A"
			


		try:
			year_xpath = '//*[@id="itemListContent"]/div/div['+str(i)+']/div[2]/div[1]/div/span[1]/text()'
			year_text = doc.xpath(year_xpath)
			string1 = year_text[0]
			year = string1.split()
			dict[year[0]] = year[1]
		except:
			year = "N/A"
			

		try:
			make_xpath = '//*[@id="itemListContent"]/div/div['+str(i)+']/div[2]/div[1]/div/span[2]/text()'
			make_text = doc.xpath(make_xpath)
			make_t = make_text[0]
			make = make_t.split()
			dict[make[0]]=make[1]
		except:
			make = "N/A"
			

		try:

			model_xpath = '//*[@id="itemListContent"]/div/div['+str(i)+']/div[2]/div[1]/div/span[3]/text()'
			model_text = doc.xpath(model_xpath)
			model_t = model_text[0]
			model = model_t.split()
			dict[model[0]]=model[1]
		except:
			model = "N/A"
			

		try:
			kilo_xpath = '//*[@id="itemListContent"]/div/div['+str(i)+']/div[2]/div[1]/div/span[4]/text()'
			kilo_text = doc.xpath(kilo_xpath)
			kilo_t = kilo_text[0]
			kilo = kilo_t.split()
			dict[kilo[1]]=kilo[0]
		except: 
			kilo = "N/A"
			

for p in range(1,500):
	url = 'http://www.olx.in/nf/search/honda%2Bcity/-p-'+str(p)
	driver = webdriver.Chrome(executable_path="/users/mithun/Downloads/chromedriver")
	driver.get(url)
	scrap(driver.page_source)
	driver.quit()