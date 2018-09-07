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
import csv

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
    name = "piplv3spider"
    allowed_domains = ["pipl.com"]
    start_urls = (
        'http://www.pipl.com/',
    )

    def read_csv(self, file):
        mf = open(file,'rb')
        reader = csv.reader(mf)
        # cols = reader.next()
        return reader

    def parse(self, response):
        # file = 'propertylist.xls'
        file = 'VA_FindPhoneNumer.csv'

        #Getting phone numbers from sheet2 of contacts.xlsx file
        rows = self.read_csv(file)
        print "here in self"
        """
            Modifying the existing xls file
        """

        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-javascript")
            options.add_argument("--disable-java")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-images")
            driver = webdriver.Chrome('c://chromedriver.exe',chrome_options = options)

            cols = rows.next()
            myf = open('pipldatamissingafter658.csv','wb')
            fobj = csv.writer(myf)
            fobj.writerow(cols)
            rows = list(rows)
            for ctr,row in enumerate(rows,start=658):
                print ctr
                row = rows[ctr]

                city_col = row[23]
                st = row[24]
                if not city_col:
                    city_col = 'Tallahassee'
                    st = 'Florida'
                    # fobj.writerow(row)
                    #continue
                else:
                    fobj.writerow(row)
                    continue

                name_col = row[1].lower()
                full_name = name_col

                name = urllib.quote_plus(name_col)
                location = urllib.quote_plus(city_col+', '+st)
                driver.get('https://pipl.com/search/?q={}&l={}&sloc=&in=6'.format(name,location))

                html = driver.page_source
                hxs = fromstring(html)

                # with open('profile.html','wb') as hf:
                #     hf.write(html)
                """
                If No Result Found for then skipping
                """
                no_results = hxs.xpath('//div[class="header no_results"]')
                if no_results:
                    continue
                    time.sleep(2)


                #print "sheet name %s" % full_name
                flag = False
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

                            career = hxs.xpath('//ul[@class="jobs"]/li/text()')

                            row[-1] = phones
                            fobj.writerow(row)
                            flag = True
                        else:
                            flag = False

                if not flag:
                    fobj.writerow(row)

                time.sleep(1)

        except Exception as e:
            print e



