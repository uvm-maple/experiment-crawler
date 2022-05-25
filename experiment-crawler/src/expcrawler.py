import requests
import lxml
from bs4 import BeautifulSoup

# Boostrap with search engines by domain
# Start with a bound name; loop through text later

# Basic instructions from here: https://www.topcoder.com/thrive/articles/web-crawler-in-python

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
} 
# parameterize this query in the future (make news a variable)
# Note that you can copy the url below and drop it into the browser
f = requests.get('https://www.google.com/search?q=news', headers=headers)

soup = BeautifulSoup(f.content,'lxml')
# I found the cite tag by:
# 1. going to the section that I might want to expand in Chrome
# 2. right clicking on that section and selecting 'Inspect Element"
# 3. scrolling through the HTML
#
# You should play around with this more, following the example linked above. 
# Track what you see and what you try in a notes file 
results = soup.find('cite')
print(results)