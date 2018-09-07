# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from lxml.html import fromstring
import xlrd
import urllib
from xlrd import open_workbook
from xlutils.copy import copy

from scrapy.http import Request

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import re
import json

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

class Piplv2spiderSpider(scrapy.Spider):
    name = "piplv2spider"
    allowed_domains = ["pipl.com"]
    start_urls = (
        'http://www.pipl.com/',
    )

    def read_xls(self,file,col_no=5):
        # Open the workbook
        xl_workbook = xlrd.open_workbook(file)
        # List sheet names, and pull a sheet by name
        sheet_names = xl_workbook.sheet_names()
        print('Sheet Names', sheet_names)

        xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
        # num_cols = xl_sheet.ncols   # Number of columns

        row = xl_sheet.row(0)  # 1st row

        # num_cols = xl_sheet.ncols   # Number of columns

        rows = []
        for row_idx in range(0, xl_sheet.nrows):    # Iterate through rows
            row_obj = xl_sheet.row(row_idx)
            rows.append(row_obj)

        return rows



    def parse(self, response):
        # file = 'propertylist.xls'
        file = 'records.xls'
        #Getting phone numbers from sheet2 of contacts.xlsx file
        rows = self.read_xls(file)
        print "here in self"
        """
            Modifying the existing xls file
        """
        rb = open_workbook(file)
        wb = copy(rb)
        sheet = wb.get_sheet(0)
        # sheet.write(0,23,'Phone')
        print sheet
        # sheet.write(0,42,'Phone(pipl.com)')
        # sheet.write(0,24,'Phone(pipl.com)')



        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-javascript")
            options.add_argument("--disable-java")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-images")
            driver = webdriver.Chrome('c://chromedriver.exe',chrome_options = options)

            # start = 90
            # rows = rows[start:]

            for ctr,row in enumerate(rows,start=1):
                print ctr
                row = rows[ctr]
                #row_col = row[5].value
                first_name = row[2].value
                last_name = row[4].value
                middle_name = row[3].value
                full_name = ' '.join([first_name,last_name]).lower()
                # if middle_name:
                #     full_name = ' '.join([first_name,middle_name,last_name])

                city_col = row[6].value
                st = row[7].value

                #name_col = row[11].value
                name_col = full_name

                name = urllib.quote_plus(name_col)
                location = urllib.quote_plus(city_col+', '+st)
                driver.get('https://pipl.com/search/?q={}&l={}&sloc=&in=6'.format(name,location))

                html = driver.page_source
                hxs = fromstring(html)

                with open('profile.html','wb') as hf:
                    hf.write(html)
                """
                If No Result Found for then skipping
                """
                no_results = hxs.xpath('//div[class="header no_results"]')
                if no_results:
                    continue
                    time.sleep(2)


                #print "sheet name %s" % full_name
                profiles_container = hxs.xpath('//div[@id="profile_container"]')
                for profile_container in profiles_container:
                    pipl_name = profile_container.xpath('./div/div[@id="profile_summary"]/div/span[@class="highlight"]/text()')
                    print "pipl name is:%s" % pipl_name
                    # pipl_name = profile_container.xpath('normalize-space(./div/div[@id="profile_summary"]/text())')
                    phones = profile_container.xpath('//ul[@class="phones"]/li/a/text()')
                    pipl_phones = [re.sub('\D*','',phone) for phone in phones]
                    #print phones
                    print pipl_phones
                    # sheet_phone = re.sub('\D*','',sheet_p  hone)
                    """
                    if total digits are greater than 10 strip left digit to get only 10 digit
                    """
                    # if len(sheet_phone) > 10:
                    #     sheet_phone = sheet_phone[1:10]
                    # print sheet_phone
                    # print pipl_name
                    if pipl_name:
                        # pipl_name = re.sub('\s*\(.*\)|\W*\s*[\(\)]','',name)
                        pipl_name = ' '.join(pipl_name)
                        pipl_name = pipl_name.lower()
                        print ctr
                        print "pipl name %s" % pipl_name

                        """
                        checking if sheet name and site name are matched then putting address data to xls
                        """
                        print 'Full name:%s' % full_name

                        if all(x in full_name.split() for x in pipl_name.split()) or all(x in pipl_name.split() for x in full_name.split()):
                            print "name matched exactly"
                            sheet.write(ctr,11,', '.join(pipl_phones))
                            wb.save('file.xls')

                time.sleep(1)

        except Exception as e:
            print e



