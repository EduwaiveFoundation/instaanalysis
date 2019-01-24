from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd
import sys

user_names = []
user_comments = []
Post_id=[]
class InstagramBot():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.url='https://www.instagram.com/'
        #self.email = email
        #self.password = password

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(1)
        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(4)

    def fetch_comments(self,postid):
        time.sleep(4)
        comment = self.browser.find_elements_by_class_name('gElp9 ')
        for c in comment:
        	Post_id.append(postid)
        	container = c.find_element_by_class_name('C4VMK')
        	name = container.find_element_by_class_name('_6lAjh').text
        	content = container.find_element_by_tag_name('span').text
        	content = content.replace('\n', ' ').strip().rstrip()
        	user_names.append(name)
        	user_comments.append(content)
        
		
		

    def visit_profile(self,name,lim):
        url1=self.url + name
        self.browser.get(url1)
        time.sleep(3)
        posts = self.browser.find_elements_by_class_name('_9AhH0')
        count=0
        lim=int(lim)
        if len(posts)<lim:
        	print('Not Enough Posts')
        	self.browser.close()
        	sys.exit()
       	for post in posts:
       		post.click()
       		postid=str(self.browser.current_url).replace(self.url+'p','')
       		postid=postid.replace('/','')
       		self.fetch_comments(postid)
       		self.browser.execute_script("window.history.go(-1)")
       		count += 1
       		if count==lim:
       			break
       		time.sleep(1)
       	self.browser.close()	

    def tocsv(self,name):
    	df=pd.DataFrame()
    	profileName=[name]*len(user_names)
    	df['Profile']=profileName
    	df['Post_ID']=Post_id
    	df["Commentor's Name"]= user_names
    	df['Comment']= user_comments
    	filename=name + '.csv'
    	df.to_csv(filename,encoding ='utf-8',index=False)   		   		
         

bot=InstagramBot()
bot.visit_profile(sys.argv[1],sys.argv[2])        
bot.tocsv(sys.argv[1])
