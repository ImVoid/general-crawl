import re
from basic.Download import *

url = 'http://example.webscraping.com/places/default/view/239'
html = download(url)
print re.findall('<td class="w2p_fw">(.*?)</td>', html)