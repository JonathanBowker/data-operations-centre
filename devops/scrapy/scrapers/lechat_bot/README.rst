======
lechat_bot
======

This is a Scrapy project to scrape lechat websites.
It has two spiders:
 lechat: used for in-situ testing against an SRI lechat server without captcha

To solve captcha when prompted, open the captcha.jpg file
Output gets saved in comments.txt  (example included)

bot uses messages.txt for keep-alive phrases
usernames and passwords are obtained from users.txt and pass.txt,

Usage
=====

torsocks scrapy crawl lechat2
