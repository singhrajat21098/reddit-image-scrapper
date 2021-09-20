#!/usr/bin/env python
# coding: utf-8

# In[2]:


print("Importing Libraries...")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import os.path
import time
import urllib.request
import re
from datetime import date
import random
import unicodecsv as csv


# In[5]:


class Reddit_image_scrapper:
    
    def __init__(self, folder_path, num_scrolls, page_link):
        self.folder_path = str(folder_path)
        self.num_scrolls = int(num_scrolls)
        self.page_link = str(page_link)
        
        self.date_stamp = str(date.today().strftime('%m%d%Y')) + str(random.randint(100,999))
        
        

        
        self.open_webpage()
        self.html_parser()
        self.save_images()
        self.generate_captions()
        self.generate_output()
        self.driver.close()
    
    
    
        
    def open_webpage(self):
        self.driver = webdriver.Chrome()
        print('Opening Webpage')
        self.driver.get(self.page_link)
        for i in range(0,self.num_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Scrolling " + str(i))
            time.sleep(2)
            
    def html_parser(self):
        self.soup = bs(self.driver.page_source, 'html.parser')
        self.subreddit = '/r/'+self.page_link.split('/')[4]
        
    def generate_captions(self):
        
        def text_filter(text):
            regrex_pattern = re.compile(pattern = "["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                               "]+", flags = re.UNICODE)
            st = re.sub('[^A-Za-z0-9 ]+', '',regrex_pattern.sub(r'',text))
            return re.sub('[^A-Za-z0-9 ]+', '', st)
        self.output = []
        all_headings = [heading.string for heading in self.soup.find_all('h3')]
        filtered_headings = [text_filter(heading).lower() for heading in all_headings]
        for i in range(len(self.list_of_captions)):
            if self.list_of_captions[i] == ' ':
                self.output.append([self.date_stamp+'#'+str(i), str("\U00002665")])
                continue
            for j in range(len(filtered_headings)):
                if filtered_headings[j].startswith(self.list_of_captions[i]):
                    self.output.append([self.date_stamp+'#'+str(i), str(all_headings[j])])
                    break
        print(self.output)
        
    def generate_output(self):
        fields = ['id','text']
        filename = self.date_stamp+str(".csv")
        completeName = os.path.join(self.folder_path, filename)
        with open(completeName, 'wb') as csvfile:  
            # creating a csv writer object  
            csvwriter = csv.writer(csvfile)  

            # writing the fields  
            csvwriter.writerow(fields)  

            # writing the data rows  
            csvwriter.writerows(self.output) 
        
        
                    
                    
        
        
    def save_images(self):
        self.list_of_post_image = [ x for x in self.soup.find_all('img') if x.get('alt') == 'Post image' and self.subreddit in x.parent.parent.parent['href']]
        self.list_of_captions = []
        for count,link in enumerate(self.list_of_post_image):
            try:     
                caption = link.parent.parent.parent['href'].split('/')[-2].replace('_',' ')
                self.list_of_captions.append(caption)
                print('Image ',count,'saved')
                completeName = os.path.join(self.folder_path, self.date_stamp+'#'+str(count)+ " "+ caption+ ".jpg")
                urllib.request.urlretrieve(link.get('src'),completeName )
                
            except Exception as e:
                print('Image',count,e)
                
                pass
            
        
        
        


# In[6]:





# In[ ]:




