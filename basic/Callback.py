# --coding:utf8--

import re
import csv
import lxml.html

class ScraeCallback:
    """抓取数据写入cvs文件"""
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))
        self.fields = ('area', 'population', 'iso', 'country',
                       'capital', 'continent', 'tld', 'currency_code',
                       'currency_name', 'phone', 'postal_code_format',
                       'postal_code_regex', 'languages', 'neighbours')
        self.writer.writerow(self.fields)

    # 当调用类名()时，自动调用此函数
    def __call__(self, url, html):
        if re.search('/view', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                try:
                    row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
                except IndexError as e:
                    print '解析失败：', e
            self.writer.writerow(self.fields)