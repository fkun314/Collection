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

API_KEY = 'AIzaSyC5JrrRgN0U-4RmRDQksQePpgotOwNI3is'
YOUTUBE_API_SERVICE_NAME = 'youtube'
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


    #!/usr/bin/env python3

    filename = youtube_id
    target_id = filename.split('.')[0]
    count_row = 1
    result = ""
    with open("./json/"+filename+'.json', 'r', encoding='utf8') as f:
        lines = f.readlines()[2:]
        for line in lines:
            sys.stdout.write('\rProcessing line %d' % (count_row))
            if 'liveChatTickerPaidMessageItemRenderer' in line:
                continue
            if 'liveChatTextMessageRenderer' not in line and 'liveChatPaidMessageRenderer' not in line:
                continue
            ql = line
            frac = ("#Chat No.%05d " % count_row)
            info = ast.literal_eval(ql)

            # Case Normal Chat
            if 'liveChatTextMessageRenderer' in line:
                try:
                    info['replayChatItemAction']['actions'][0]['addChatItemAction']['item']['liveChatTextMessageRenderer']
                except:
                    pass
                else:
                    info = info['replayChatItemAction']['actions'][0]['addChatItemAction']['item']['liveChatTextMessageRenderer']
                    content = ""
                    if 'simpleText' in info['message']:
                        content = info['message']['simpleText']
                    elif 'runs' in info['message']:
                        for fragment in info['message']['runs']:
                            if 'text' in fragment:
                                content += fragment['text']
                    else:
                        print("no text")
                        continue
                    authorName = info['authorName']['simpleText']
                    time = info['timestampText']['simpleText']
                    frac += "type: NORMALCHAT user: \"" + authorName + \
                        "\" time: " + time + "\n- " + content + "\n"

            # Case Super Chat
            if 'liveChatPaidMessageRenderer' in line:
                info = info['replayChatItemAction']['actions'][0]['addChatItemAction']['item']['liveChatPaidMessageRenderer']
                content = ""
                if 'message' in info:
                    if 'simpleText' in info['message']:
                        content = info['message']['simpleText']
                    elif 'runs' in info['message']:
                        for fragment in info['message']['runs']:
                            if 'text' in fragment:
                                content += fragment['text']
                    else:
                        print("no text")
                        continue

                if 'authorName' in info:
                    authorName = info['authorName']['simpleText']
                else:
                    authorName = "%anonymous%"
                time = info['timestampText']['simpleText']
                purchaseAmout = info['purchaseAmountText']['simpleText']
                frac += "type: SUPERCHAT user: \"" + authorName + "\" time: " + \
                    time + " amount: " + purchaseAmout + "\n- " + content + "\n"
            result += frac
            count_row += 1

    target_id = filename.split('.')[0]
    sys.stdout.write('\nDone!')
    with open("./txt/row/"+target_id + ".txt", 'w', encoding='utf8') as f:
        f.write(result)


    #!/usr/bin/env python3
    # 秒数表示とコメント表示のみ

    filename = youtube_id
    target_id = filename.split('.')[0]
    count = 1
    result = ""
    result_interjection = ""
    result_all = ""
    result_word_only = ""
    count_ij = 0
    most_words = []
    count_w = 0

    with open("./json/"+filename+".json", 'r', encoding='utf8') as f:
        lines = f.readlines()[2:]
        for line in lines:
            sys.stdout.write('\rProcessing line %d' % (count))
            if 'liveChatTickerPaidMessageItemRenderer' in line:
                continue
            if 'liveChatTextMessageRenderer' not in line and 'liveChatPaidMessageRenderer' not in line:
                continue
            ql = line
            # frac = ("#Chat No.%05d " % count)
            frac = ""
            frac_all = ""
            frac_interjection = ""
            frac_word_only = ""
            info = ast.literal_eval(ql)

            # Case Normal Chat
            if 'liveChatTextMessageRenderer' in line:
                try:
                    info['replayChatItemAction']['actions'][0]['addChatItemAction']['item']['liveChatTextMessageRenderer']
                except:
                    pass
                else:
                    info = info['replayChatItemAction']['actions'][0]['addChatItemAction']['item']['liveChatTextMessageRenderer']
                    content = ""
                    if 'simpleText' in info['message']:
                        content = info['message']['simpleText']
                    elif 'runs' in info['message']:
                        for fragment in info['message']['runs']:
                            if 'text' in fragment:
                                content += fragment['text']
                    else:
                        print("no text")
                        continue
                    authorName = info['authorName']['simpleText']
                    time = info['timestampText']['simpleText']
                    t = datetime.time(0, 0, 0, 0)
                    time_sp = time.split(':')
                    if(len(time_sp) == 2):
                        # print(time_sp)
                        try:
                            min = int(time[0])
                        except:
                            print("error")
                        else:
                            t = datetime.time(0, int(time_sp[0]), int(time_sp[1]), 0)
                    else:
                        try:
                            int(time_sp[0])
                        except:
                            print("ValueError")
                            # print(time_sp)
                        else:
                            t = datetime.time(int(time_sp[0]), int(
                                time_sp[1]), int(time_sp[2]), 0)
                    time = t.hour * 3600 + t.minute * 60 + t.second
                    if time != 0:
                        frac_all += (str(time)+","+content + "\n")
                        if("草" in content or "w" in content or "W" in content or "笑" in content):
                            frac += (str(time)+","+content + "\n")
                            count_w += 1
                            frac_word_only += (content+" ")
                        tokenizer = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd")
                        tokenizer.parse("")
                        node = tokenizer.parseToNode(content)
                        keywords = []
                        while node:
                            if node.feature.split(",")[0] == u"感動詞" or node.feature.split(",")[0] == u"形容詞":
                                content = node.surface
                                frac_interjection += (str(time)+","+content + "\n")
                                count_ij += 1
                                origin = node.feature.split(",")[6]
                                if origin != "*":
                                    most_words.append(origin)
                                    frac_word_only += (str(origin)+" ")
                            if node.feature.split(",")[0] == u"名詞":
                                origin = node.feature.split(",")[6]
                                if origin != "*":
                                    most_words.append(origin)
                                    frac_word_only += (str(origin)+" ")
                            node = node.next

                # Case Super Chat
                if 'liveChatPaidMessageRenderer' in line:
                    info = info['replayChatItemAction']['actions'][0]['addChatItemAction']['item']['liveChatPaidMessageRenderer']
                    content = ""
                    if 'message' in info:
                        if 'simpleText' in info['message']:
                            content = info['message']['simpleText']
                        elif 'runs' in info['message']:
                            for fragment in info['message']['runs']:
                                if 'text' in fragment:
                                    content += fragment['text']
                        else:
                            print("no text")
                            continue

                    if 'authorName' in info:
                        authorName = info['authorName']['simpleText']
                    else:
                        authorName = "%anonymous%"
                    time = info['timestampText']['simpleText']
                    t = datetime.time(0, 0, 0, 0)
                    time_sp = time.split(':')
                    purchaseAmout = info['purchaseAmountText']['simpleText']
                    if(len(time_sp) == 2):
                        # print(time_sp)
                        try:
                            min = int(time[0])
                        except:
                            print("error")
                        else:
                            t = datetime.time(0, int(time_sp[0]), int(time_sp[1]), 0)
                    else:
                        try:
                            int(time_sp[0])
                        except:
                            print("ValueError")
                            # print(time_sp)
                        else:
                            t = datetime.time(int(time_sp[0]), int(
                                time_sp[1]), int(time_sp[2]), 0)
                    time = t.hour * 3600 + t.minute * 60 + t.second
                    if time != 0:
                        frac_all += (str(time)+","+content + "\n")
                        if("草" in content or "w" in content or "W" in content or "笑" in content):
                            frac += (str(time)+","+content + "\n")
                            count_w += 1
                            frac_word_only += (content+" ")
                        tokenizer = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd")
                        tokenizer.parse("")
                        node = tokenizer.parseToNode(content)
                        keywords = []
                        while node:
                            if node.feature.split(",")[0] == u"感動詞" or node.feature.split(",")[0] == u"形容詞":
                                content = node.surface
                                frac_interjection += (str(time)+","+content + "\n")
                                count_ij += 1
                                origin = node.feature.split(",")[6]
                                if origin != "*":
                                    most_words.append(origin)
                                    frac_word_only += (str(origin)+" ")
                            if node.feature.split(",")[0] == u"名詞":
                                origin = node.feature.split(",")[6]
                                if origin != "*":
                                    most_words.append(origin)
                                    frac_word_only += (str(origin)+" ")
                            node = node.next
                result += frac
                result_interjection += frac_interjection
                result_all += frac_all
                result_word_only += frac_word_only
                count += 1

    count_words = collections.Counter(most_words)
    target_id = filename.split('.')[0]
    sys.stdout.write('\nDone!')
    with open("./txt/w/"+target_id + ".txt", 'w', encoding='utf8') as f:
        f.write(result)

    with open("./txt/all/"+target_id + ".txt", 'w', encoding='utf8') as f:
        f.write(result_all)

    with open("./txt/interjection/"+target_id + ".txt", 'w', encoding='utf8') as f:
        f.write(result_interjection)

    with open("./txt/word_only/"+target_id + ".txt", 'w', encoding='utf8') as f:
        f.write(result_word_only)

title = ""

CONTENT = ""

most_words = ""

# 単語データを読み込む
with open("./txt/word_only/"+youtube_id + ".txt", 'r', encoding='utf8') as f:
    CONTENT = f.read()
stopwords = [u"いる", u"なら", u"する", u"ある", u"ない", u"こと", u"なっ", u"でき", u"できる", u"これ",
             u"もの", u"よう", u"なる", u"はず", u"なり", u"それ", u"れる", u"られる", u"ここ", u"ため", u"草", u"\n"]
word_cloud = WordCloud(max_font_size=200, width=1280, height=720,
                       font_path="./LightNovelPOPv2.otf", stopwords=set(stopwords)).generate(CONTENT)
word_cloud.to_file("./html_view/plt/wordcloud/"+youtube_id+".png")
if already == 0:
    # p = open("index.html","w",encoding="utf-8")
    # addlist = '<p><a href="./html/'+youtube_id+'.html">'+title+"</p>"
    # p.writelines(row)
    # p.close()
    for youtube_id in VIDEO_ID_LIST:
        response = youtube.videos().list(
            part='snippet,statistics',
            id=youtube_id
        ).execute()

        for item in response.get("items", []):
            if item["kind"] != "youtube#video":
                continue
            # print('*' * 10)
            # print(json.dumps(item, indent=2, ensure_ascii=False))
            # print('*' * 10)
            # print(item["snippet"]["channelId"])
            print('*' * 30)
            print(json.dumps(item, indent=2, ensure_ascii=False))
            print('*' * 30)
            # url = item["snippet"]["thumbnails"]["maxres"]["url"]
            url = "https://img.youtube.com/vi/"+youtube_id+"/maxresdefault.jpg"
            file_name = "./thumbnail/"+youtube_id+"_maxresdefault.jpg"
            title = item["snippet"]["title"]

            response = requests.get(url)
            image = response.content

            with open("./html_view/thumbnail/"+youtube_id+"_maxresdefault.jpg", "wb") as aaa:
                aaa.write(image)

            aaa.close()

            get_data.append(file_name)
            get_data.append(dt_now.strftime("%Y-%m-%d %H:%M:%S"))
            get_data.append(item["snippet"]["title"])
            get_data.append(youtube_id)
            get_data.append(item["snippet"]["publishedAt"].replace(
                'T', ' ').replace('Z', ''))
            get_data.append(item["snippet"]["channelTitle"])
            get_data.append(item["statistics"]["viewCount"])
            get_data.append(count_row)
            get_data.append(count_w)
            get_data.append(count_ij)
            try:
                item["statistics"]["likeCount"]
            except:
                get_data.append("0")
            else:
                get_data.append(item["statistics"]["likeCount"])

            try:
                item["statistics"]["dislikeCount"]
            except:
                get_data.append("0")
            else:
                get_data.append(item["statistics"]["dislikeCount"])
            try:
                round((int(item["statistics"]["likeCount"])/(int(item["statistics"]
                                                                 ["likeCount"])+int(item["statistics"]["dislikeCount"])))*100, 2)
            except:
                get_data.append("0")
            else:
                get_data.append(round((int(item["statistics"]["likeCount"])/(int(
                    item["statistics"]["likeCount"])+int(item["statistics"]["dislikeCount"])))*100, 2))
            get_data.append(item["statistics"]["commentCount"])
            # print(get_data)
            data_csv = open("./db/data.csv", "a", encoding="utf-8")
            writer = csv.writer(data_csv, lineterminator='\n')
            writer.writerow(get_data)
            data_csv.close()
            p = open("./html_view/index.html", "r", encoding="utf-8")
            data = p.read()
            row = data.split("\n")
            p.close()
            row.pop()
            row.pop()
            row.pop()
            row.pop()
            row.pop()
            row.pop()
            # row.append('<p><a href="./html/'+youtube_id+'.html">'+youtube_id+'</p>\n')
            row.append("<tr>\n<td>"+str(line_count)+"</td>\n")
            row.append("<td><img src='"+str(file_name) +
                       "' width='128' height='72'></td>\n")
            row.append(
                "<td>"+str(dt_now.strftime("%Y-%m-%d %H:%M:%S"))+"</td>\n")
            row.append("<td>"+str(item["snippet"]["title"])+"</td>\n")
            row.append("<td><a href='https://www.youtube.com/watch?v=" +
                       str(youtube_id)+"'>"+str(youtube_id)+"</a></td>\n")
            row.append(
                "<td>"+str(item["snippet"]["publishedAt"].replace('T', ' ').replace('Z', ''))+"</td>\n")
            row.append("<td><a href='https://www.youtube.com/channel/"+str(
                item["snippet"]["channelId"])+"'>"+str(item["snippet"]["channelTitle"])+"</a></td>\n")
            row.append("<td>"+str(item["statistics"]["viewCount"])+"</td>\n")
            row.append("<td>"+str(count_row)+"</td>\n")
            row.append("<td><a href='./html/"+youtube_id +
                       ".html'>"+str(count_w)+"</a></td>\n")
            row.append("<td><a href='./html/"+youtube_id +
                       ".html'>" + str(count_ij)+"</a></td>\n")
            try:
                item["statistics"]["likeCount"]
            except:
                row.append("<td>0</td>")
            else:
                row.append(
                    "<td>"+str(item["statistics"]["likeCount"])+"</td>\n")

            try:
                item["statistics"]["dislikeCount"]
            except:
                row.append("<td>0</td>")
            else:
                row.append(
                    "<td>"+str(item["statistics"]["dislikeCount"])+"</td>\n")
            try:
                round((int(item["statistics"]["likeCount"])/(int(item["statistics"]
                                                                 ["likeCount"])+int(item["statistics"]["dislikeCount"])))*100, 2)
            except:
                row.append("<td>0</td>")
            else:
                row.append("<td>"+str(round((int(item["statistics"]["likeCount"])/(int(
                    item["statistics"]["likeCount"])+int(item["statistics"]["dislikeCount"])))*100, 2))+"</td>\n")

            try:
                item["statistics"]["commentCount"]
            except:
                row.append("<td>0</td>")
            else:
                row.append(
                    "<td>"+str(item["statistics"]["commentCount"])+"</td>\n</tr>\n")
            row.append("</tbody>\n")
            row.append("</table>\n")
            row.append("</div>\n")
            row.append("</body>\n")
            row.append("</html>\n")
            p = open("./html_view/index.html", "w", encoding="utf-8")
            addlist = '<p><a href="./html/'+youtube_id+'.html">'+youtube_id+"</p>"
            p.writelines(row)
            p.close()
else:
    for youtube_id in VIDEO_ID_LIST:
        response = youtube.videos().list(
            part='snippet,statistics',
            id=youtube_id
        ).execute()

        for item in response.get("items", []):
            if item["kind"] != "youtube#video":
                continue
            # print('*' * 10)
            # print(json.dumps(item, indent=2, ensure_ascii=False))
            # print('*' * 10)
            # print(item["snippet"]["channelId"])
            print('*' * 30)
            print(json.dumps(item, indent=2, ensure_ascii=False))
            print('*' * 30)

            # url = item["snippet"]["thumbnails"]["maxres"]["url"]
            url = "https://img.youtube.com/vi/"+youtube_id+"/maxresdefault.jpg"
            file_name = "./thumbnail/"+youtube_id+"_maxresdefault.jpg"
            title = item["snippet"]["title"]

filename = youtube_id

row_no = 0

fileobj = open("./txt/all/"+filename+".txt", "r", encoding="utf-8")
text_a = []
time_a = []

while True:
    line = fileobj.readline()
    if line:
        row_no += 1
        moji = line.split(",")
        time = moji[0]
        text = moji[1]
        print(time)
        print(text)
        text_a.append(text)
        time_a.append(int(time))
    else:
        break

time_co = collections.Counter(time_a)
time_co = sorted(time_co.items())
x = [x for x, y in time_co]
y = [y for x, y in time_co]

xx_all = []
yy_all = []
gdic = dict()
c = 15
s = 0
count = 0
for line in time_co:
    t, tc = line
    if int(t) <= c:
        s += tc
        count += 1
    else:
        if c == 15:
            for i in range(15):
                yy_all.append(s)
                xx_all.append(i)

            gdic[str(0)+"-"+str(c)] = s
        else:
            for i in range(count):
                xx_all.append(c+i)
                yy_all.append(s)
            gdic[str(c)+"-"+str(c+20)] = s
        count = 0
        c += 15
        s = tc

plt.figure(figsize=(16, 10), dpi=60)
plt.xlabel('sec', fontsize=24)
plt.ylabel('count', fontsize=24)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.plot(xx_all, yy_all)
plt.title(youtube_id+"-w")
# plt.show()
plt.savefig('./html_view/plt/all/'+youtube_id+'.png')


row_no = 0

fileobj = open("./txt/w/"+filename+".txt", "r", encoding="utf-8")
text_l = []
time_l = []

while True:
    line = fileobj.readline()
    if line:
        row_no += 1
        moji = line.split(",")
        time = moji[0]
        text = moji[1]
        print(time)
        print(text)
        time_l.append(int(time))
        text_l.append(text)
    else:
        break

time_co = collections.Counter(time_l)
time_co = sorted(time_co.items())
x = [x for x, y in time_co]
y = [y for x, y in time_co]

xx = []
yy = []
gdic_w = dict()
c = 15
s = 0
count = 0
for line in time_co:
    t, tc = line
    if int(t) <= c:
        s += tc
        count += 1
    else:
        if c == 15:
            for i in range(15):
                xx.append(i)
                yy.append(s)

            gdic_w[str(0)+"-"+str(c)] = s
        else:
            for i in range(count):
                xx.append(c+i)
                yy.append(s)
            gdic_w[str(c)+"-"+str(c+20)] = s
        count = 0
        c += 15
        s = tc

plt.figure(figsize=(16, 10), dpi=60)
plt.xlabel('sec', fontsize=24)
plt.ylabel('count', fontsize=24)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.plot(xx, yy)
plt.title(youtube_id+"-w")
# plt.show()
plt.savefig('./html_view/plt/w/'+youtube_id+'.png')

row_no = 0

fileobj = open("./txt/interjection/"+filename+".txt", "r", encoding="utf-8")
text_l = []
time_l = []

while True:
    line = fileobj.readline()
    if line:
        row_no += 1
        moji = line.split(",")
        time = moji[0]
        text = moji[1]
        print(time)
        print(text)
        text_l.append(text)
        time_l.append(int(time))
    else:
        break

time_co = collections.Counter(time_l)
time_co = sorted(time_co.items())
x = [x for x, y in time_co]
y = [y for x, y in time_co]

# plt.figure(figsize=(16, 10), dpi=60)
# plt.xlabel('sec',fontsize = 24)
# plt.ylabel('count',fontsize = 24)
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# plt.plot(x,y)
# plt.show()


xx_interjection = []
yy_interjection = []
gdic_ij = dict()
c = 15
s = 0
count = 0
for line in time_co:
    t, tc = line
    if int(t) <= c:
        s += tc
        count += 1
    else:
        if c == 15:
            for i in range(15):
                xx_interjection.append(i)
                yy_interjection.append(s)

            gdic_ij[str(0)+"-"+str(c)] = s
        else:
            for i in range(count):
                xx_interjection.append(c+i)
                yy_interjection.append(s)
            gdic_ij[str(c)+"-"+str(c+20)] = s
        count = 0
        c += 15
        s = tc

plt.figure(figsize=(16, 10), dpi=60)
plt.xlabel('sec', fontsize=24)
plt.ylabel('count', fontsize=24)
plt.legend()
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.plot(xx, yy, label='Count of "w or W')
plt.plot(xx_interjection, yy_interjection, label='Count of interjections')
plt.plot(xx_all, yy_all, label='Count of all chats')
plt.legend()
plt.title(youtube_id+"-interjection")
# plt.show()
plt.savefig('./html_view/plt/interjection/'+youtube_id+'.png')

highlight_list_all = sorted(gdic.items(), key=lambda x: -x[1])
highlight_list_w = sorted(gdic_w.items(), key=lambda x: -x[1])
highlight_list_ij = sorted(gdic_ij.items(), key=lambda x: -x[1])
recommend_count = 0
base_url = "https://www.youtube.com/watch?v="+youtube_id
recommend_dic = dict()
# for highlight in highlight_list:
#     timerange , _ = highlight
#     time = timerange.split("-")
#     s = int(time[0])
#     e = int(time[1])
#     if s == 0:
#         continue
#     if recommend_count == 10:
#         break

#     recommend_dic[s] = dict()
#     recommend_dic[s]["t_range"] = timerange
#     recommend_dic[s]["s_t"] = s
#     recommend_dic[s]["e_t"] = e
#     recommend_dic[s]["count"] = _

#     recommend_count += 1

html = '<!DOCTYPE html>\n<html lang="ja">\n<head>\n    <meta charset="utf-8">\n    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <title>YouTube Chat Analyse</title>\n    <!-- BootstrapのCSS読み込み -->\n    <link href="../bootstrap/css/bootstrap.min.css" rel="stylesheet">\n    <!-- jQuery読み込み -->\n    <!-- <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script> -->\n    <!-- BootstrapのJS読み込み -->\n    <script src="../bootstrap/js/bootstrap.min.js"></script>\n    <script type="text/javascript" src="../jquery-3.5.1.min.js"></script>\n    <script type="text/javascript" src="../jquery.tablesorter.min.js"></script>\n    <link rel="stylesheet" href="../bootstrap_table_min.css">\n    <script>\n        $(document).ready(function () { $("#w_Table").tablesorter(); });\n        $(document).ready(function () { $("#IJ_Table").tablesorter(); });\n        $(document).ready(function () { $("#MACD_Table").tablesorter(); });\n        $(document).ready(function () { $("#Count_Table").tablesorter(); });\n    </script>\n</head>\n<body>\n    <div class="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow">\n        <h5 class="my-0 mr-md-auto font-weight-normal">YouTube Chat Analyse</h5>\n        <nav class="my-2 my-md-0 mr-md-3">\n            <a class="p-2 text-dark" href="../index.html">Index</a>\n            <a class="p-2 text-dark" href="#">Data</a>\n        </nav>\n    </div>\n'

kaku = ""

html += '<div class="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">\n        <h1 class="display-4">' + \
    title+'</h1>\n    </div>\n'

html += '<div class="container">\n'
html += '<img src="../thumbnail/'+youtube_id + \
    '_maxresdefault.jpg" class="img-fluid">\n'

html += '<h3 class=" text-center ">15秒あたりのコメント数</h3>\n'
html += '<img src="../plt/interjection/' + \
    youtube_id+'.png" class="img-fluid">\n'
# html += '<h3 class=" text-center ">MACDによるバースト検知</h3>\n'
# html += '<img src="../plt/macd/'+youtube_id+'.png"  class="img-fluid">\n'
html += '<h3 class=" text-center ">総チャット数ランキング</h3>\n'

# html += '<table class="tablesorter-bootstrap" id="w_Table">\n'
html += '<div class="mx-4">\n            <table class="tablesorter-bootstrap" id="all_Table">\n                <thead>\n                    <tr>\n                        <th>No.</th>\n                        <th>時間</th>\n                        <th>草、wチャット数</th>\n                    </tr>\n                </thead>\n                <tbody>\n<tr>\n'
ranking = 0

for highlight in highlight_list_all:
    timerange, _ = highlight
    time = timerange.split("-")
    s = int(time[0])
    e = int(time[1])
    if s == 0:
        continue
    if recommend_count == 10:
        break
    sm, ss = divmod(s, 60)
    em, ee = divmod(e, 60)
    print("recommend_point : ", str(sm)+":"+str(ss)+" ~ " +
          str(em)+":"+str(ee), " +-30s", " count : ", _)
    kaku += ("recommend_point : "+str(sm)+":"+str(ss) +
             " ~ "+str(em)+":"+str(ee)+" +-30s\n")
    print("\t", base_url+"&feature=youtu.be&t="+str(s-30)+"&end="+str(e+30))
    kaku += ("\t"+base_url+"&feature=youtu.be&t=" +
             str(s-30)+"&end="+str(e+30)+"\n")
    ranking += 1
    html += '<tr><td>'+str(ranking)+'</td>\n'
    html += '<td><a href="https://www.youtube.com/embed/'+youtube_id + \
        '?start='+str(s-30)+'" target="blank">'+str(sec_min(s-30))+"</a></td>\n"
    html += '<td>'+str(_)+'</td></tr>\n'
    # str(s-30)+' +-30s】</h4>\n'
    # html += "<p>コメント数 : "+str(_)+"</p>\n"
    # html += '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+youtube_id+'?start='+str(s-30)+'" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n'

    recommend_count += 1

html += '</tbody>\n</table>\n</div>\n'

recommend_count = 0
base_url = "https://www.youtube.com/watch?v="+youtube_id
recommend_dic = dict()

html += '<h3 class=" text-center ">草、wのチャット数ランキング</h3>\n'

# html += '<table class="tablesorter-bootstrap" id="w_Table">\n'
html += '<div class="mx-4">\n            <table class="tablesorter-bootstrap" id="w_Table">\n                <thead>\n                    <tr>\n                        <th>No.</th>\n                        <th>時間</th>\n                        <th>草、wチャット数</th>\n                    </tr>\n                </thead>\n                <tbody>\n<tr>\n'
ranking = 0

for highlight in highlight_list_w:
    timerange, _ = highlight
    time = timerange.split("-")
    s = int(time[0])
    e = int(time[1])
    if s == 0:
        continue
    if recommend_count == 10:
        break
    sm, ss = divmod(s, 60)
    em, ee = divmod(e, 60)
    print("recommend_point : ", str(sm)+":"+str(ss)+" ~ " +
          str(em)+":"+str(ee), " +-30s", " count : ", _)
    kaku += ("recommend_point : "+str(sm)+":"+str(ss) +
             " ~ "+str(em)+":"+str(ee)+" +-30s\n")
    print("\t", base_url+"&feature=youtu.be&t="+str(s-30)+"&end="+str(e+30))
    kaku += ("\t"+base_url+"&feature=youtu.be&t=" +
             str(s-30)+"&end="+str(e+30)+"\n")
    ranking += 1
    html += '<tr><td>'+str(ranking)+'</td>\n'
    html += '<td><a href="https://www.youtube.com/embed/'+youtube_id + \
        '?start='+str(s-30)+'" target="blank">'+str(sec_min(s-30))+"</a></td>\n"
    html += '<td>'+str(_)+'</td></tr>\n'
    # str(s-30)+' +-30s】</h4>\n'
    # html += "<p>コメント数 : "+str(_)+"</p>\n"
    # html += '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+youtube_id+'?start='+str(s-30)+'" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n'

    recommend_count += 1

html += '</tbody>\n</table>\n</div>\n'

recommend_count = 0
base_url = "https://www.youtube.com/watch?v="+youtube_id
recommend_dic = dict()

html += '<h3 class=" text-center ">感動詞のチャット数ランキング</h3>\n'

# html += '<table class="tablesorter-bootstrap" id="IJ_Table">\n'
html += '<div class="mx-4">\n            <table class="tablesorter-bootstrap" id="IJ_Table">\n                <thead>\n                    <tr>\n                        <th>No.</th>\n                        <th>時間</th>\n                        <th>感動詞チャット数</th>\n                    </tr>\n                </thead>\n                <tbody>\n'
ranking = 0

for highlight in highlight_list_ij:
    timerange, _ = highlight
    time = timerange.split("-")
    s = int(time[0])
    e = int(time[1])
    if s == 0:
        continue
    if recommend_count == 10:
        break
    sm, ss = divmod(s, 60)
    em, ee = divmod(e, 60)
    print("recommend_point : ", str(sm)+":"+str(ss)+" ~ " +
          str(em)+":"+str(ee), " +-30s", " count : ", _)
    kaku += ("recommend_point : "+str(sm)+":"+str(ss) +
             " ~ "+str(em)+":"+str(ee)+" +-30s\n")
    print("\t", base_url+"&feature=youtu.be&t="+str(s-30)+"&end="+str(e+30))
    kaku += ("\t"+base_url+"&feature=youtu.be&t=" +
             str(s-30)+"&end="+str(e+30)+"\n")
    ranking += 1
    html += '<tr>\n<td>'+str(ranking)+'</td>\n'
    html += '<td><a href="https://www.youtube.com/embed/'+youtube_id + \
        '?start='+str(s-30)+'" target="blank">'+str(sec_min(s-30))+"</a></td>\n"
    html += '<td>'+str(_)+'</td>\n</tr>\n'

    recommend_count += 1

html += '\n</tbody>\n</table>\n</div>\n'

# s_recom_l = sorted(recommend_dic.items())

# for recpoint in s_recom_l:
#     _ , rec_dic = recpoint
#     print("recommend_point : ",rec_dic["t_range"]," +-30s" , " count : ",rec_dic["count"])
#     kaku += ("recommend_point : "+str(rec_dic["t_range"])+" +-30s" + " count : "+str(rec_dic["count"])+"\n")
#     print("\t",base_url+"&feature=youtu.be&t="+str(rec_dic["s_t"]-30))
#     kaku += ("\t"+base_url+"&feature=youtu.be&t="+str(rec_dic["s_t"]-30)+"\n")
#     html += '<h3>【'+rec_dic["t_range"]+' +-30s】</h3>\n'
#     html += "<p>コメント数 : "+str(rec_dic["count"])+"</p>\n"
#     html += '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+youtube_id+'?start='+str(rec_dic["s_t"]-30)+'" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n'

# html += "<h3>MACDによるバースト検知</h3>"

# html += '<h3 class=" text-center ">MACDによる草コメントバースト検知</h3>\n'

# f = 4
# s = 8
# t = 5
# macd_data = MACDData(f, s, t)
# macd_data.calc_macd(yy)
# my = np.array(macd_data.histgram_list)

# macd_interjection_data = MACDData(f, s, t)
# macd_interjection_data.calc_macd(yy_interjection)
# my_interjection = np.array(macd_interjection_data.histgram_list)

# plt.figure(figsize=(16, 10), dpi=60)
# plt.xlabel('sec', fontsize=24)
# plt.ylabel('MACD', fontsize=24)
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# plt.plot(xx, my, label="Count of w or W")
# plt.plot(xx_interjection, my_interjection, label="Count of interjections")
# plt.legend()
# plt.title(youtube_id)
# # plt.show()
# plt.savefig('./html_view/plt/macd/'+youtube_id+'.png')


# ly = list(macd_data.histgram_list)

# xx = []
# yy = []
# gdic = dict()
# c = 15
# s = 0
# count = 0
# lyz = 0
# for line in time_co:
#     t, tc = line
#     if int(t) <= c:
#         s += tc
#         count += 1
#     else:
#         if c == 15:
#             for i in range(15):
#                 xx.append(i)
#                 yy.append(s)

#             gdic[str(0)+"-"+str(c)] = ly[lyz]
#             lyz += 1
#         else:
#             for i in range(count):
#                 xx.append(c+i)
#                 yy.append(s)
#             gdic[str(c)+"-"+str(c+20)] = ly[lyz]
#             lyz += 1
#         count = 0
#         c += 15
#         s = tc

# highlight_list = sorted(gdic.items(), key=lambda x: -x[1])

# recommend_count = 0
# base_url = "https://www.youtube.com/watch?v="+youtube_id

# # html += '<table class="tablesorter-bootstrap" id="MACD_Table">\n'
# # html += '<thead>\n            <tr>\n                <th>No.</th>\n                <th>時間</th>\n                <th>感動詞チャット数</th>\n             </tr>\n        </thead>\n        <tbody>\n'
# html += '<div class="mx-4">      \n<table class="tablesorter-bootstrap" id="MACD_Table">\n                <thead>\n                    <tr>\n                        <th>No.</th>\n                        <th>時間</th>\n                        <th>感動詞チャット数</th>\n                    </tr>\n                </thead>\n                <tbody>\n'
# ranking = 0

# for highlight in highlight_list:
#     timerange, _ = highlight
#     time = timerange.split("-")
#     s = int(time[0])
#     e = int(time[1])
#     if s == 0:
#         continue
#     if recommend_count == 10:
#         break
#     sm, ss = divmod(s, 60)
#     em, ee = divmod(e, 60)
#     ranking += 1
#     print("recommend_point : ", str(sm)+":"+str(ss)+" ~ " +
#           str(em)+":"+str(ee), " +-30s", " macd_histgram : ", _)
#     print("\t", base_url+"&feature=youtu.be&t="+str(s-30)+"&end="+str(e+30))
#     html += '<tr>\n<td>'+str(ranking)+'</td>\n'
#     html += '<td><a href="https://www.youtube.com/embed/'+youtube_id + \
#         '?start='+str(s-30)+'" target="blank">'+str(sec_min(s-30))+"</a></td>\n"
#     html += '<td>'+str(round(_, 2))+'</td>\n</tr>\n'

#     recommend_count += 1

# html += '</tbody>\n</table>\n</div>\n'

# html += '<h3 class=" text-center ">MACDによる感動詞チャットのバースト検知</h3>\n'

# # f = 4
# # s = 8
# # t = 5
# # macd_data = MACDData(f, s, t)
# # macd_data.calc_macd(yy)
# # my = np.array(macd_data.histgram_list)

# # macd_interjection_data = MACDData(f, s, t)
# # macd_interjection_data.calc_macd(yy_interjection)
# # my_interjection = np.array(macd_interjection_data.histgram_list)

# # plt.figure(figsize=(16, 10), dpi=60)
# # plt.xlabel('sec', fontsize=24)
# # plt.ylabel('MACD', fontsize=24)
# # plt.xticks(fontsize=20)
# # plt.yticks(fontsize=20)
# # plt.plot(xx, my, label="Count of w or W")
# # plt.plot(xx_interjection, my_interjection, label="Count of interjections")
# # plt.legend()
# # plt.title(youtube_id)
# # plt.show()
# # plt.savefig('./html_view/plt/macd/'+youtube_id+'.png')


# ly = list(macd_interjection_data.histgram_list)

# xx = []
# yy = []
# gdic = dict()
# c = 15
# s = 0
# count = 0
# lyz = 0
# for line in time_co:
#     t, tc = line
#     if int(t) <= c:
#         s += tc
#         count += 1
#     else:
#         if c == 15:
#             for i in range(15):
#                 xx.append(i)
#                 yy.append(s)

#             gdic[str(0)+"-"+str(c)] = ly[lyz]
#             lyz += 1
#         else:
#             for i in range(count):
#                 xx.append(c+i)
#                 yy.append(s)
#             gdic[str(c)+"-"+str(c+20)] = ly[lyz]
#             lyz += 1
#         count = 0
#         c += 15
#         s = tc

# highlight_list = sorted(gdic.items(), key=lambda x: -x[1])

# recommend_count = 0
# base_url = "https://www.youtube.com/watch?v="+youtube_id

# # html += '<table class="tablesorter-bootstrap" id="MACD_Table">\n'
# # html += '<thead>\n            <tr>\n                <th>No.</th>\n                <th>時間</th>\n                <th>感動詞チャット数</th>\n             </tr>\n        </thead>\n        <tbody>\n'
# html += '<div class="mx-4">      \n<table class="tablesorter-bootstrap" id="MACD_Table">\n                <thead>\n                    <tr>\n                        <th>No.</th>\n                        <th>時間</th>\n                        <th>感動詞チャット数</th>\n                    </tr>\n                </thead>\n                <tbody>\n'
# ranking = 0

# for highlight in highlight_list:
#     timerange, _ = highlight
#     time = timerange.split("-")
#     s = int(time[0])
#     e = int(time[1])
#     if s == 0:
#         continue
#     if recommend_count == 10:
#         break
#     sm, ss = divmod(s, 60)
#     em, ee = divmod(e, 60)
#     ranking += 1
#     print("recommend_point : ", str(sm)+":"+str(ss)+" ~ " +
#           str(em)+":"+str(ee), " +-30s", " macd_histgram : ", _)
#     print("\t", base_url+"&feature=youtu.be&t="+str(s-30)+"&end="+str(e+30))
#     html += '<tr>\n<td>'+str(ranking)+'</td>\n'
#     html += '<td><a href="https://www.youtube.com/embed/'+youtube_id + \
#         '?start='+str(s-30)+'" target="blank">'+str(sec_min(s-30))+"</a></td>\n"
#     html += '<td>'+str(round(_, 2))+'</td>\n</tr>\n'

#     recommend_count += 1
# html += '</tbody>\n</table>\n</div>\n'

# html += "<h3>チャット内単語出現ランキングTop50</h3>"
# html += '<h3 class=" text-center ">チャット内単語出現ランキングTop50</h3>\n'

# html += '<table class="tablesorter-bootstrap" id="MACD_Table">\n'
count_words = collections.Counter(text_a)

html += '<div class="mx-4">\n            <h3 class=" text-center ">チャット内単語出現ランキングTop20</h3>\n            <table class="tablesorter-bootstrap" id="Count_Table">\n                <thead>\n                    <tr>\n                        <th>No.</th>\n                        <th>原型</th>\n                        <th>チャット数</th>\n                    </tr>\n                </thead>\n<tbody>\n'
count_number = count_words.most_common()
for i in range(0, 50):
    html += '<tr><td>'+str(i+1)+'</td>\n'
    html += '<td>'+str(count_number[i][0])+'</td>\n'
    html += '<td>'+str(count_number[i][1])+'</td>\n</tr>\n'

html += '</tbody>\n</table>\n</div>\n'

html += '<img src="../plt/wordcloud/'+youtube_id+'.png" class="img-fluid">'

html += '\n<div>\n</body>\n</html>'

f = open("./data/"+youtube_id+".txt", "w", encoding="utf-8")
f.write(kaku)
f.close()

h = open("./html_view/html/"+youtube_id+".html", "w", encoding="utf-8")
h.write(html)
h.close()

# p=open("index.html","r",encoding="utf-8")
# data = p.read()
# row = data.split("\n")
# p.close()

# print(len(row))
# print(row[(len(row)-1)]+"\n")
# print(row[(len(row)-2)]+"\n")
# print(row[(len(row)-3)]+"\n")
# row[(len(row)-1)] = row[(len(row)-1)]
# row[(len(row)-1)] = row[(len(row)-3)]
# row[(len(row)-3)] = ('<p><a href="./html/'+youtube_id+'.html">'+title+"</p>")
# row.pop()
# row.pop()
# row.pop()
# row.append('<p><a href="./html/'+youtube_id+'.html">'+title+'</p>\n')
# row.append("</body>\n")
# row.append("</html>\n")
# print(len(row))
# print(row[(len(row)-1)]+"\n")
# print(row[(len(row)-2)]+"\n")
# print(row[(len(row)-3)]+"\n")

print(count_words.most_common(20))

if(os.path.isfile('json/'+youtube_id+'.json')):
    os.remove('json/'+youtube_id+'.json')
    
print("complete")