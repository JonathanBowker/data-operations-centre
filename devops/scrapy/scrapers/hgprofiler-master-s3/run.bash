#!/bin/bash
#usage: create usernames.txt then do ./run.bash
#you should have usernames.txt line separated

wget -O- -q  https://s3-eu-west-1.amazonaws.com/isis-tweets/usernames.txt | while read line

do
	echo "Running against username: $line"
	scrapy crawl profiler_spider -a usernames=$line -o s3://isis-tweets/out/${line}.json -t json
done

