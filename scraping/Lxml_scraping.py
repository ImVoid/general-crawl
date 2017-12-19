# --coding:utf-8--

import lxml.html
from basic.Download import *

url = 'http://example.webscraping.com/places/default/view/239'
html = download(url)
#构建bom树
tree = lxml.html.fromstring(html)
#定位单元格，使用css选择器与jQuery如出一辙
td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
#获得文本
area = td.text_content()
print area