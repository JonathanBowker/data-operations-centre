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
class PiplspiderSpider(scrapy.Spider):
    name = "piplspider"
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
        for row_idx in range(1, xl_sheet.nrows):    # Iterate through rows
            row_obj = xl_sheet.row(row_idx)
            rows.append(row_obj)

        return rows

    def parse(self, response):
        file = 'Spread-NewList09-29-15.xls'
        #Getting phone numbers from sheet2 of contacts.xlsx file
        rows = self.read_xls(file)
        """
            Modifying the existing xls file
        """
        rb = open_workbook(file)
        wb = copy(rb)
        sheet = wb.get_sheet(0)
        # sheet.write(0,23,'Phone')
        print sheet


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
                row = rows[ctr]
                # print row
                phone_col = row[47].value
                first_name = row[1].value
                middle_name = row[2].value
                last_name = row[3].value
                full_name = ' '.join([first_name,last_name])
                print ctr

                """
                Checks if no is float converts to int, else gets the phone value, if phone blank that row is skipped
                """
                try:
                    phone = float(phone_col)
                    phone = int(phone)
                except ValueError:
                    # print "Not a float"
                    phone = phone_col
                    if not phone_col:
                        # print ctr
                        print "blank row"
                        continue
                phone = str(phone)
                sheet_phone = phone
                phone = urllib.quote_plus(phone)
                driver.get('https://pipl.com/search/?q={}&l=&sloc=&in=6'.format(phone))

                html = driver.page_source
                hxs = fromstring(html)
                """
                If No Result Found for then skipping
                """
                no_results = hxs.xpath('//div[class="header no_results"]')
                if no_results:
                    continue
                    time.sleep(2)


                print "sheet name %s" % full_name
                profiles_container = hxs.xpath('//div[@id="profile_container"]')
                for profile_container in profiles_container:
                    name = profile_container.xpath('normalize-space(./div/div[@id="profile_summary"]/div/text())')
                    phones = profile_container.xpath('//ul[@class="phones"]/li/a/text()')
                    pipl_phones = [re.sub('\D*','',phone) for phone in phones]
                    print phones
                    print pipl_phones
                    sheet_phone = re.sub('\D*','',sheet_phone)
                    """
                    if total digits are greater than 10 strip left digit to get only 10 digit
                    """
                    if len(sheet_phone) > 10:
                        sheet_phone = sheet_phone[1:10]
                    print sheet_phone
                    if name:
                        # pipl_name = re.sub('\W*\s*[\(\)]','',name)
                        pipl_name = re.sub('\s*\(.*\)|\W*\s*[\(\)]','',name)
                        print "pipl name %s" % pipl_name
                        fl_name = ' '.join([first_name,last_name])

                        """
                        checking if sheet name and site name are matched then putting address data to xls
                        """
                        if all(x in full_name.split() for x in pipl_name.split()) or all(x in pipl_name.split() for x in full_name.split()) or sheet_phone in pipl_phones:
                            print "name matched exactly"
                            json_addresses = hxs.xpath('//ul[@class="addresses"]/li')


                            """
                            Removing dupes
                            """
                            # json_addresses = list(set(json_addresses))
                            # print json_addresses
                            """
                            if addresses more than 4 but getting first 4 and inserting as we have 4 cols
                            """
                            if len(json_addresses) >= 4:
                                json_addresses = json_addresses[:4]
                            """
                            Getting address fields available on pipl.com
                            """
                            counter = 4
                            for col_no,address in enumerate(json_addresses,start=4):
                                # add = address.attrib['data-address']
                                add = address.xpath('./@data-address')
                                if add:
                                    add = add[0] #to get dict from list with 1 elem
                                    add = json.loads(add)
                                    display = add['display']
                                    print display
                                    if add['state'] == "PA" and display:
                                        sheet.write(ctr+1,counter,display)
                                        counter += 1
                                print add

                            wb.save('file.xls')

                time.sleep(2)

        except Exception as e:
            print e


        pass
