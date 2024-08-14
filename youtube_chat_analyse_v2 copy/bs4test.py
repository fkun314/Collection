from bs4 import BeautifulSoup
import ast
import requests
import requests_html  # <= 追加
import re
import sys
import os
from pprint import pprint
import glob
import json
from pathlib import Path
import math
import collections
import numpy as np
import japanize_matplotlib
import matplotlib.pyplot as plt
import datetime
import time
import datetime
import MeCab
import datetime
from googleapiclient.discovery import build
import csv
from wordcloud import WordCloud
from urllib.parse import urlparse, parse_qs


dt_now = datetime.datetime.now()

def sec_min(sec):
    hour = int(sec / 3600)
    sec %= 3600
    min = int(sec/ 60)
    sec %= 60
    # print("{h:02}:{m:02}:{s:02}".format(h=hour,m=min,s=sec))
    return "{h:02}:{m:02}:{s:02}".format(h=hour,m=min,s=sec)

# API_KEY = 'hogehoge'
# APIは変更ずみです...
# YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
# CHANNEL_ID = 'UC8C1LLhBhf_E2IBPLSDJXlQ'
VIDEO_ID_LIST = [sys.argv[1]]
# VIDEO_ID_LIST = str(VIDEO_LIST).replace('https://www.youtube.com/watch?v=','')
# VIDEO_ID_LIST = VIDEO_LIST

# print(VIDEO_ID_LIST)

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
)

line_count = 0
with open("./db/data.csv", "r", encoding="utf-8") as f:
    for line in f:
        line_count += 1
f.close()

line_count += 1
print(line_count)
get_data = []
get_data.append(line_count)


class MACDData():
    def __init__(self, f, s, t):
        self.f = f
        self.s = s
        self.t = t

    def calc_macd(self, freq_list):
        n = len(freq_list)
        self.macd_list = []
        self.signal_list = []
        self.histgram_list = []

        for i in range(n):

            if i < self.f:
                self.macd_list.append(0)
                self.signal_list.append(0)
                self.histgram_list.append(0)
            else:
                macd = sum(freq_list[i-self.f+1:i+1])/len(freq_list[i-self.f+1:i+1]) - sum(
                    freq_list[max(0, i-self.s):i+1])/len(freq_list[max(0, i-self.s):i+1])
                self.macd_list.append(macd)
                signal = sum(self.macd_list[max(
                    0, i-self.t+1):i+1])/len(self.macd_list[max(0, i-self.t+1):i+1])
                self.signal_list.append(signal)
                histgram = macd - signal
                self.histgram_list.append(histgram)


# Verify user supplied a YouTube URL.
if len(sys.argv) == 1:
    print("Please provide a YouTube URL (e.g. ./YoutubeChatReplayCrawler.py YOUTUBE_VIDEO_URL)")
    sys.exit(0)


# Produce a valid filename (from Django text utils).
def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


# Set up variables for requests.
youtube_id = sys.argv[1]
# youtube_id = VIDEO_ID_LIST
# youtube_id = str(str(youtube_id).replace('https://www.youtube.com/watch?v=',''))
print(youtube_id)
target_url = "https://www.youtube.com/watch?v=" + sys.argv[1]
dict_str = ''
next_url = ''
comment_data = []
# session = requests.Session()
session = requests_html.HTMLSession()
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

# Get the video page.
# html = session.get(target_url)
# resp = session.get(target_url,proxies= {"http": "http://wproxy.net.sendai-nct.ac.jp:8080","https": "https://wproxy.net.sendai-nct.ac.jp:8080"},verify = False)
resp = session.get(target_url)
resp.html.render(sleep=3)
# soup = BeautifulSoup(html.text, 'html.parser')

# Retrieve the title and sanitize so it is a valid filename.
# title = soup.find_all('title')
title = resp.html.find('title')
title = title[0].text.replace(' - YouTube', '')
title = get_valid_filename(title)

already = 0


if os.path.exists('./txt/all/'+youtube_id+'.txt'):
    print("That video has downloaded.")
    already = 1
else:
    print("Start Download")
    # Regex match for emoji.
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

    # Find any live_chat_replay elements, get URL for next live chat message.
    # for iframe in soup.find_all("iframe"):
    #     if("live_chat_replay" in iframe["src"]):
    #         next_url = iframe["src"]
    for iframe in resp.html.find("iframe"):
        if("live_chat_replay" in iframe.attrs["src"]):
            next_url= "".join(["https://www.youtube.com", iframe.attrs["src"]])


    if not next_url:
        print("Couldn't find live_chat_replay iframe. Maybe try running again?")
        sys.exit(1)

    # TODO - We should fail fast if next_url is empty, otherwise you get error:
    # Invalid URL '': No schema supplied. Perhaps you meant http://?

    # TODO - This loop is fragile. It loops endlessly when some exceptions are hit.
    while(1):

        try:
            html = session.get(next_url, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')

            # Loop through all script tags.
            # for script in soup.find_all('script'):
            #     script_text = str(script)
            #     if 'ytInitialData' in script_text:
            #         dict_str = ''.join(script_text.split(" = ")[1:])

            for scrp in soup.find_all("script"):
                if "window[\"ytInitialData\"]" in scrp.next:
                    dict_str = scrp.next.split(" = ", 1)[1]

            # Capitalize booleans so JSON is valid Python dict.
            dict_str = dict_str.replace("false", "False")
            dict_str = dict_str.replace("true", "True")

            # Strip extra HTML from JSON.
            dict_str = re.sub(r'};.*\n.+<\/script>', '}', dict_str)

            # Correct some characters.
            dict_str = dict_str.rstrip("  \n;")

            # TODO: I don't seem to have any issues with emoji in the messages.
            # dict_str = RE_EMOJI.sub(r'', dict_str)

            # Evaluate the cleaned up JSON into a python dict.
            dics = ast.literal_eval(dict_str)

            # TODO: On the last pass this returns KeyError since there are no more
            # continuations or actions. Should probably just break in that case.
            continue_url = dics["continuationContents"]["liveChatContinuation"][
                "continuations"][0]["liveChatReplayContinuationData"]["continuation"]
            print('Found another live chat continuation:')
            print(continue_url)
            next_url = "https://www.youtube.com/live_chat_replay?continuation=" + continue_url

            # Extract the data for each live chat comment.
            # for samp in dics["continuationContents"]["liveChatContinuation"]["actions"][1:]:
            for samp in dics["continuationContents"]["liveChatContinuation"]["actions"]:
                comment_data.append(str(samp) + "\n")

        # next_urlが入手できなくなったら終わり
        except requests.ConnectionError:
            print("Connection Error")
            continue
        except requests.HTTPError:
            print("HTTPError")
            break
        except requests.Timeout:
            print("Timeout")
            continue
        except requests.exceptions.RequestException as e:
            print(e)
            break
        except KeyError as e:
            error = str(e)
            if 'liveChatReplayContinuationData' in error:
                print('Hit last live chat segment, finishing job.')
            else:
                print("KeyError")
                print(e)
            break
        except SyntaxError as e:
            print("SyntaxError")
            print(e)
            break
        except KeyboardInterrupt:
            break
        except Exception:
            print("Unexpected error:" + str(sys.exc_info()[0]))

        # Write the comment data to a file named after the title of the video.
        with open("./json/"+youtube_id + ".json", mode='w', encoding="utf-8") as f:
            f.writelines(comment_data)

        print('Comment data saved to ' + youtube_id + '.json')