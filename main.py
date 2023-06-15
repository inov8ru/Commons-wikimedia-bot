import os
from env import *
import feedparser
import telebot
import re
from time import sleep
from datetime import timedelta

bot = telebot.TeleBot(os.getenv('BOT_KEY'))
channel = os.getenv('CHANNEL')
wait_time_in_seconds = 30
wait_time = timedelta(seconds=wait_time_in_seconds)
feed_url = os.getenv('FEED_URL')
messages_list1 = []
messages_list2 = []
last_sent_message = ''
sent_msg_cnt = 0

def parse_url(feed, i):
  url = feed.entries[i].id
  url = re.search('^[^&]*', url)[0]
  return url

while True:
  if len(messages_list1) == 0:
    print('No messages in messages_list1. Collecting...')
    d = feedparser.parse(feed_url)
    message = parse_url(d, 0)
    while message == last_sent_message:
      print('last_sent_message founded. Waiting...')
      sleep(3)
      d = feedparser.parse(feed_url)
      message = parse_url(d, 0)
    else:
      for i in range (50):
        message = parse_url(d, i)
        if message == last_sent_message:
          break
        else:
          messages_list1.append(message)
          print(i, 'messages added to messages_list1')
  else:
    for m in reversed(messages_list1):
      bot.send_message(channel, m)
      sent_msg_cnt += 1
    #   if sent_msg_cnt % 5 == 0:
      print(sent_msg_cnt, 'messages sent. Last sent message:', m)
      last_sent_message = m
      d = feedparser.parse(feed_url)
      for i in range (50):
        message = parse_url(d, i)
        if message in messages_list1:
          break
        else:
          if message in messages_list2:
            break
          else:
            messages_list2.append(message)
      sleep(3)
    messages_list1 = messages_list2
    messages_list2 = []