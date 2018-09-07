import time
import random
import scrapy
import threading
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.item import Item, Field
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware




class myItem(Item):
    name = Field()
    description = Field()
    url = Field()





class lechat(CrawlSpider):
    name = 'lechat'
    start_urls = ['']
    msg_file = open('messages.txt', 'r')
    messages = msg_file.read().split('\n')


    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'nick': 'megatron', 'pass': 'transformer', 'action': 'login', 'colour': 'F5F5DC'},
            callback=self.after_login
        )

    def after_login(self, response):
        print response.url
        url_head = response.url[0:response.url.rfind("/")+1]

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

            if (random.randint(0,22) == 3):
                return scrapy.FormRequest.from_response(response,
                                                        formdata={'action': 'post', 'session': session_id, 'postid': post_id, 'multi': '',  
                                                                  'message': msg, 'sendto': '*'}, callback=self.chat_submit)
            else:
                    return scrapy.FormRequest.from_response(response,
                                                        formdata={'action': 'post', 'session': session_id, 'postid': post_id, 'multi': '',  
                                                                  'message': '', 'sendto': '*'}, callback=self.chat_submit)
            

        return;


#http://doc.scrapy.org/en/latest/topics/selectors.html
