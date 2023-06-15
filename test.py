import os
from env import *
import feedparser
import re

feed_url = os.getenv('FEED_URL')
messages_list1 = []
messages_list2 = []
last_sent_message = ''
sent_msg_cnt = 0

d = feedparser.parse(feed_url)
for i in range(50):
    print(i)
    url = d.entries[i].id
    url = re.search('^[^&]*', url)[0]
    print(url)