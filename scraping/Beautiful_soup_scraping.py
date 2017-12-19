# --coding:utf-8--
from bs4 import BeautifulSoup
from basic.Download import *

url = 'http://example.webscraping.com/places/default/view/239'
html = download(url)
soup = BeautifulSoup(html, 'html.parser')
# 定位行
tr = soup.find(attrs={'id':'places_area__row'})
# 定位单元格
td = tr.find(attrs={'class':'w2p_fw'})
area = td.text
print area