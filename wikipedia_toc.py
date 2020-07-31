'''
Navigates to a wikipedia page and creates a HTML clickable Table of Contents using Selenium, requests and BeautifulSoup.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep
import requests
import bs4 as bs
import datetime

# Report variables
datestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
dateOfSearch = datetime.datetime.now().strftime('%Y-%m-%d')

header = \
"""
<!DOCTYPE html>
<html>
<head>
<title>Wikipedia Search</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<div style="max-width: 900px; background-color: #EEEEEE; padding:50px">
<h2 style="text-align: center;"><strong>Wikipedia Search Results</strong></h2>
"""
tableHead = \
"""
<p><strong>Table of Contents:</strong></p>
<table style="border-color: #ffa500;" border="5" cellspacing="0" cellpadding="5">
<tbody>
<tr><td style="text-align: center;"><strong>TOC Item</strong></td>
<td style="text-align: center;"><strong>URL</strong></td>
</tr>
"""
footer = \
"""
</tbody>
</table>
<p>&copy; <a title="masaccio.io" href="http://masaccio.io/" target="_blank" rel="noopener">masaccio.io</a></p>
</div>
</body>
</html>
"""
# Start Application
print('This application returns a list of subtitles for a term in Wikipedia')
term = input('Input term to search in Wikipedia: ')

# Navigate to the page and retrive the page of the wished term in Wikipedia
options = Options()
options.headless = True
browser = webdriver.Firefox(options=options, executable_path='webdriver/geckodriver')
browser.get('https://www.wikipedia.org/')
browser.find_element_by_id('searchInput').send_keys(term)
browser.find_element_by_id('searchInput').send_keys(Keys.RETURN)
sleep(2)

# Request the term page from Wikipedia for analysis
url = browser.current_url
res = requests.get(url)
pageContent = bs.BeautifulSoup(res.text, 'html.parser')

# Get the page title
pageTitle = pageContent.select('#firstHeading')

for t in pageTitle:
    title = t.getText()

# Create file to save report
filename = title + datestamp + '.html'
f=open(filename, "a+")
f.write(header)
f.write(f'<p><strong>Date of Search:</strong> {dateOfSearch}</p>')
f.write(f'<p><strong>The term you searched in Wikipedia: </strong>{title}</p><p><strong>\
Term URL:</strong><a href="{url}" name="{url}" target="_blank">{url}</a></p>')
f.write(tableHead)


# Get Table of Contents (First Level)
toc = pageContent.select('.toclevel-1 a')
for item in toc:
    link = url + item['href']
    f.write(f'<tr><td>{item.getText()}</td>\
    <td><a title="{link}"\
    href="{link}" target="_blank" rel="noopener">{link}</a></td></tr>')
sleep(5)
f.write(footer)
browser.close()
f.close()
print('>>> END OF PROCESS <<<')
