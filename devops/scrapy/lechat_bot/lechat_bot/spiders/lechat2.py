import time
import random
import scrapy
import threading
import urllib
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.item import Item, Field
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware




class lechat(CrawlSpider):
    name = 'lechat2'
    random.seed(time.time());
    start_urls = ['']
    msg_file = open('messages.txt', 'r')
    messages = msg_file.read().split('\n')
    user_file = open('users.txt', 'r')
    users = user_file.read().split('\n')
    nick = users[random.randint(0,len(users)-1)]
    pass_file = open('pass.txt', 'r')
    passwords = pass_file.read().split('\n')
    passwd = passwords[random.randint(0,len(passwords)-1)]
    print "Logging in as " + nick + "/" + passwd


    def parse(self, response):
        challenge = response.xpath('//input[contains(@name, "challenge")]/@value').extract()[0]
        ts = response.xpath('//input[contains(@name, "ts")]/@value').extract()[0]
        img_src = response.url[0:response.url.rfind("/")+1] + response.xpath('//img[contains(@src, "captcha")]/@src').extract()[0]
        urllib.urlretrieve(img_src, "captcha.jpg")
        captcha = raw_input("put captcha in manually>") 
        print challenge + " " + ts + " " + img_src

        f = open('comments.txt', 'a+')
        f.write("\n Logging in as %s \n" % lechat.nick); 
        f.close()


        return scrapy.FormRequest.from_response(
            response,
            formdata={'action': 'login', 'challenge': challenge, 'ts': ts, 'nick': lechat.nick, 'pass': lechat.passwd,  'captcha': captcha, 'colour': ''},
            callback=self.after_login
        )

    def after_login(self, response):
        print response.url
        url_head = response.url[0:response.url.rfind("/")+1]

        if (response.body.find("invalid captcha") > 0):
            print "Error: Invalid Captcha"
            return


        links = response.css('frame').xpath('@src').extract()
        for index, link in enumerate(links):
            if (link.startswith('http') == True):                
                next_link = link
            else:
                next_link = url_head + link
            print "link: " + next_link
            yield scrapy.Request(next_link,self.chat_submit,dont_filter=True)

        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)

        return


    # Doesn't work...
    def sleep_submit_worker(self, response):
        print ("IN SLEEP SUBMIT WORKER\n")
        session_id = response.xpath('//input[contains(@name, "session")]/@value').extract()[0]
        post_id = response.xpath('//input[contains(@name, "postid")]/@value').extract()[0]
        
        time.sleep(5)
        print ("DONE SLEEPING IN SLEEP SUBMIT WORKER\n")
        msg = lechat.messages[random.randint(0,len(lechat.messages)-1)]
        print (msg + "\n")
        return scrapy.FormRequest.from_response(response,
                                                formdata={'action': 'post', 'session': session_id, 'postid': post_id, 'multi': '',  
                                                          'message': msg, 'sendto': '*'}, callback=self.chat_submit)
    


    def chat_submit(self, response):
#        if (response.body.find("name=\"action\" value=\"post\"") > 0):

        if (response.body.find("talk to") > 0):

#            t = threading.Thread(target=self.sleep_submit_worker, args=(response,))
#            t.start()

            session_id = response.xpath('//input[contains(@name, "session")]/@value').extract()[0]
            post_id = response.xpath('//input[contains(@name, "postid")]/@value').extract()[0]
            
            time.sleep(5)
            msg = lechat.messages[random.randint(0,len(lechat.messages)-1)]

            if (random.randint(0,3) == 1):
                return scrapy.FormRequest.from_response(response,
                                                        formdata={'action': 'post', 'session': session_id, 'postid': post_id, 'multi': '',  
                                                                  'message': msg, 'sendto': '*'}, callback=self.chat_submit)
            else:
                    return scrapy.FormRequest.from_response(response,
                                                        formdata={'action': 'post', 'session': session_id, 'postid': post_id, 'multi': '',  
                                                                  'message': '', 'sendto': '*'}, callback=self.chat_submit)
            

        return;



