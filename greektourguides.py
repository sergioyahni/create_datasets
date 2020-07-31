''' 
Creates a dataset of  tour guides in greece 
registered with the Welcome to the official site of the 
Association of Licensed Tourist Guides 
To my best understanding the robots.txt file at the website (https://www.tourist-guides.gr/robots.txt) 
allows a fair use of the database.
'''
from time import sleep
import requests
from bs4 import BeautifulSoup as bs
import datetime
import pandas as pd

url = 'https://www.tourist-guides.gr/en/guides-profiles.aspx?sort=random&prof=false'
requestPage = requests.get(url)
page = bs(requestPage.text, 'html.parser')

name = page.select('.item .name a')
language = page.select('.item .info .line .spoken')
residence = page.select('.item .info .line .residence')
phone = page.select('.item .info .line .phone')
email = page.select('.item .info .last .mail')

tour_guides_in_greece = []
number_of_items =  len(name)
for n in range (number_of_items):
    # Define items content 
    guide_name = name[n].getText().title()
    guide_language = language[n].getText().replace('Languages: ', '').strip()
    guide_residence = residence[n].getText().replace('Place of residence: ', '').strip()
    guide_phone = phone[n].getText().replace('Telephone: ', '').strip()
    guide_email = email[n].getText().replace('Email:', '').strip()
    guide_email = guide_email.replace(' at ', '@')

    #Create tour guide
    tour_guide = [guide_name, guide_language, guide_residence, guide_phone, guide_email]
    tour_guides_in_greece.append(tour_guide)
    
df = pd.DataFrame(tour_guides_in_greece, columns=['guide_name', 'guide_language', 'guide_residence', 'guide_phone', 'guide_email'])
df.to_csv('tour_guides_in_greece.csv')
