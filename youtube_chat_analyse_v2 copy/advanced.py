#!/usr/bin/env python3

from bs4 import BeautifulSoup
import ast
import requests
import requests_html # <= 追加
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


class MACDData():
    def __init__(self,f,s,t):
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
            else :
                macd = sum(freq_list[i-self.f+1:i+1])/len(freq_list[i-self.f+1:i+1]) - sum(freq_list[max(0,i-self.s):i+1])/len(freq_list[max(0,i-self.s):i+1])
                self.macd_list.append(macd)
                signal = sum(self.macd_list[max(0,i-self.t+1):i+1])/len(self.macd_list[max(0,i-self.t+1):i+1])
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
target_url = "https://www.youtube.com/watch?v=" + sys.argv[1]
dict_str = ''
next_url = ''
comment_data = []
# session = requests.Session()
session = requests_html.HTMLSession()
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

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

if os.path.exists('./json/'+youtube_id+'.json'):
    print("That video has downloaded.")
    already = 1
else:
    # Regex match for emoji.
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

    # Find any live_chat_replay elements, get URL for next live chat message.
    # for iframe in soup.find_all("iframe"):
    #     if("live_chat_replay" in iframe["src"]):
    #         next_url = iframe["src"]
    for iframe in resp.html.find("iframe"):
        if "live_chat_replay" in iframe.attrs["src"]:
            next_url = "".join(["https://www.youtube.com", iframe.attrs["src"]])

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
            for script in soup.find_all('script'):
                script_text = str(script)
                if 'ytInitialData' in script_text:
                    dict_str = ''.join(script_text.split(" = ")[1:])

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
            continue_url = dics["continuationContents"]["liveChatContinuation"]["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
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
            # continue #TODO
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
count = 1
result = ""
with open("./json/"+filename+'.json', 'r', encoding='utf8') as f:
    lines = f.readlines()
    for line in lines:
        sys.stdout.write('\rProcessing line %d' % (count))
        if 'liveChatTickerPaidMessageItemRenderer' in line:
            continue
        if 'liveChatTextMessageRenderer' not in line and 'liveChatPaidMessageRenderer' not in line:
            continue
        ql = line
        frac = ("#Chat No.%05d " % count)
        info = ast.literal_eval(ql)

        # Case Normal Chat
        if 'liveChatTextMessageRenderer' in line:
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
            frac += "type: NORMALCHAT user: \"" + authorName + "\" time: " + time + "\n- " + content + "\n"

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
            frac += "type: SUPERCHAT user: \"" + authorName + "\" time: " + time + " amount: " + purchaseAmout + "\n- " + content + "\n"
        result += frac
        count += 1

target_id = filename.split('.')[0]
sys.stdout.write('\nDone!')
with open("./txt/all/"+target_id + ".txt", 'w', encoding='utf8') as f:
    f.write(result)


#!/usr/bin/env python3
#秒数表示とコメント表示のみ

filename = youtube_id
target_id = filename.split('.')[0]
count = 1
result = ""
with open("./json/"+filename+".json", 'r', encoding='utf8') as f:
    lines = f.readlines()
    for line in lines:
        sys.stdout.write('\rProcessing line %d' % (count))
        if 'liveChatTickerPaidMessageItemRenderer' in line:
            continue
        if 'liveChatTextMessageRenderer' not in line and 'liveChatPaidMessageRenderer' not in line:
            continue
        ql = line
        # frac = ("#Chat No.%05d " % count)
        frac = ""
        info = ast.literal_eval(ql)

        # Case Normal Chat
        if 'liveChatTextMessageRenderer' in line:
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
            if(len(time_sp)==2):
                print(time_sp)
                try:
                    min = int(time[0])
                except:
                    print("error")
                else:
                    t = datetime.time(0, int(time_sp[0]), int(time_sp[1]), 0)
            else:
                print(time_sp)
                t = datetime.time(int(time_sp[0]),int(time_sp[1]),int(time_sp[2]),0)
            time = t.hour * 3600 + t.minute * 60 + t.second
            if time != 0:
                if("草" in content or "w" in content or "W" in content or "笑" in content):
                    frac += (str(time)+","+content + "\n")

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
            if(len(time_sp)==2):
                print(time_sp)
                try:
                    min = int(time[0])
                except:
                    print("error")
                else:
                    t = datetime.time(0, int(time_sp[0]), int(time_sp[1]), 0)
            else:
                print(time_sp)
                t = datetime.time(int(time_sp[0]),int(time_sp[1]),int(time_sp[2]),0)
            time = t.hour * 3600 + t.minute * 60 + t.second
            if("草" in content or "w" in content or "W" in content or "笑" in content):
                frac += (str(time)+","+content + "\n")
        result += frac
        count += 1

target_id = filename.split('.')[0]
sys.stdout.write('\nDone!')
with open("./txt/w/"+target_id + ".txt", 'w', encoding='utf8') as f:
    f.write(result)

#!/usr/bin/env python3
#感動詞とタイム

filename = youtube_id
target_id = filename.split('.')[0]
count = 1
result = ""
with open("./json/"+filename+".json", 'r', encoding='utf8') as f:
    lines = f.readlines()
    for line in lines:
        sys.stdout.write('\rProcessing line %d' % (count))
        if 'liveChatTickerPaidMessageItemRenderer' in line:
            continue
        if 'liveChatTextMessageRenderer' not in line and 'liveChatPaidMessageRenderer' not in line:
            continue
        ql = line
        # frac = ("#Chat No.%05d " % count)
        frac = ""
        info = ast.literal_eval(ql)

        # Case Normal Chat
        if 'liveChatTextMessageRenderer' in line:
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
            if(len(time_sp)==2):
                print(time_sp)
                try:
                    min = int(time[0])
                except:
                    print("error")
                else:
                    t = datetime.time(0, int(time_sp[0]), int(time_sp[1]), 0)
            else:
                print(time_sp)
                t = datetime.time(int(time_sp[0]),int(time_sp[1]),int(time_sp[2]),0)
            time = t.hour * 3600 + t.minute * 60 + t.second
            if time != 0:
                tokenizer = MeCab.Tagger()
                tokenizer.parse("")
                node = tokenizer.parseToNode(content)
                keywords = []
                while node:
                    if node.feature.split(",")[0] == u"感動詞":
                        content = node.surface
                        frac += (str(time)+","+content + "\n")
                    node = node.next
                # if("草" in content or "w" in content or "W" in content or "笑" in content):

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
            if(len(time_sp)==2):
                print(time_sp)
                try:
                    min = int(time[0])
                except:
                    print("error")
                else:
                    t = datetime.time(0, int(time_sp[0]), int(time_sp[1]), 0)
            else:
                print(time_sp)
                t = datetime.time(int(time_sp[0]),int(time_sp[1]),int(time_sp[2]),0)
            time = t.hour * 3600 + t.minute * 60 + t.second
            if time != 0:
                tokenizer = MeCab.Tagger()
                tokenizer.parse("")
                node = tokenizer.parseToNode(content)
                keywords = []
                while node:
                    if node.feature.split(",")[0] == u"感動詞":
                        content = node.surface
                        frac += (str(time)+","+content + "\n")
                    node = node.next
                # if("草" in content or "w" in content or "W" in content or "笑" in content):
        
        result += frac
        count += 1

target_id = filename.split('.')[0]
sys.stdout.write('\nDone!')
with open("./txt/positive/"+target_id + ".txt", 'w', encoding='utf8') as f:
    f.write(result)


filename = youtube_id
row_no=0

fileobj = open("./txt/w/"+filename+".txt","r",encoding="utf-8")
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
x = [x for x,y in time_co]
y = [y for x,y in time_co]

# plt.figure(figsize=(16, 10), dpi=60)
# plt.xlabel('sec',fontsize = 24)
# plt.ylabel('count',fontsize = 24)
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# plt.plot(x,y)
# plt.show()


xx =[]
yy =[]
gdic = dict()
c=15
s=0
count = 0
for line in time_co:
    t,tc = line
    if int(t) <= c:
        s += tc
        count += 1
    else:
        if c ==15:
            for i in range(15):
                xx.append(i)
                yy.append(s)
        
            gdic[str(0)+"-"+str(c)] = s
        else:
            for i in range(count):
                xx.append(c+i)
                yy.append(s)
            gdic[str(c)+"-"+str(c+20)] = s
        count = 0
        c += 15
        s = tc
        
plt.figure(figsize=(16, 10), dpi=60)
plt.xlabel('sec',fontsize = 24)
plt.ylabel('count',fontsize = 24)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.plot(xx,yy)
plt.title(youtube_id+"-w")
# plt.show()
plt.savefig('./plt/normal/'+youtube_id+'.png')

row_no=0

fileobj = open("./txt/positive/"+filename+".txt","r",encoding="utf-8")
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
x = [x for x,y in time_co]
y = [y for x,y in time_co]

# plt.figure(figsize=(16, 10), dpi=60)
# plt.xlabel('sec',fontsize = 24)
# plt.ylabel('count',fontsize = 24)
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# plt.plot(x,y)
# plt.show()


xx2 =[]
yy2 =[]
gdic = dict()
c=15
s=0
count = 0
for line in time_co:
    t,tc = line
    if int(t) <= c:
        s += tc
        count += 1
    else:
        if c ==15:
            for i in range(15):
                xx2.append(i)
                yy2.append(s)
        
            gdic[str(0)+"-"+str(c)] = s
        else:
            for i in range(count):
                xx2.append(c+i)
                yy2.append(s)
            gdic[str(c)+"-"+str(c+20)] = s
        count = 0
        c += 15
        s = tc
        
plt.figure(figsize=(16, 10), dpi=60)
plt.xlabel('sec',fontsize = 24)
plt.ylabel('count',fontsize = 24)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.plot(xx,yy)
plt.plot(xx2,yy2)
plt.title(youtube_id+"-positive")
# plt.show()
plt.savefig('./plt/positive/'+youtube_id+'.png')

highlight_list = sorted(gdic.items(), key=lambda x: -x[1])
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

html = '<!DOCTYPE html>\n<html lang="jp">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>'+title+'</title>\n</head>\n<body>\n'

kaku = ""

html += '<h2>'+title+'</h2>\n'

# html += '<p>15秒あたりの草等コメント数 </p>'
# html += '<img src="../plt/normal/'+youtube_id+'.png">'
html += '<p>15秒あたりの草とポジティブコメント数 </p>'
html += '<img src="../plt/positive/'+youtube_id+'.png">'
html += '<p>MACDによるバースト検知 </p>'
html += '<img src="../plt/macd/'+youtube_id+'.png">'

html += '<h3>コメント数によるバースト検知</h3>'

for highlight in highlight_list:
    timerange , _ = highlight
    time = timerange.split("-")
    s = int(time[0])
    e = int(time[1])
    if s == 0:
        continue
    if recommend_count == 10:
        break
    sm,ss = divmod(s,60)
    em,ee = divmod(e,60)
    print("recommend_point : ",str(sm)+":"+str(ss)+" ~ "+str(em)+":"+str(ee)," +-30s" , " count : ",_)
    kaku += ("recommend_point : "+str(sm)+":"+str(ss)+" ~ "+str(em)+":"+str(ee)+" +-30s\n")
    print("\t",base_url+"&feature=youtu.be&t="+str(s-30)+"&end="+str(e+30))
    kaku += ("\t"+base_url+"&feature=youtu.be&t="+str(s-30)+"&end="+str(e+30)+"\n")
    html += '<h4>【'+str(s-30)+' +-30s】</h4>\n'
    html += "<p>コメント数 : "+str(_)+"</p>\n"
    html += '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+youtube_id+'?start='+str(s-30)+'" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n'
        
    recommend_count += 1

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

html += "<h3>MACDによるバースト検知</h3>"

f = 4
s = 8
t = 5
macd_data = MACDData(f,s,t)
macd_data.calc_macd(yy)
my = np.array(macd_data.histgram_list)

plt.figure(figsize=(16, 10), dpi=60)
plt.xlabel('sec',fontsize = 24)
plt.ylabel('MACD',fontsize = 24)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.plot(xx,my)
plt.title(youtube_id)
# plt.show()
plt.savefig('./plt/macd/'+youtube_id+'.png')


ly = list(macd_data.histgram_list)

xx =[]
yy =[]
gdic = dict()
c=15
s=0
count = 0
lyz = 0
for line in time_co:
    t,tc = line
    if int(t) <= c:
        s += tc
        count += 1
    else:
        if c ==15:
            for i in range(15):
                xx.append(i)
                yy.append(s)
        
            gdic[str(0)+"-"+str(c)] = ly[lyz]
            lyz+=1
        else:
            for i in range(count):
                xx.append(c+i)
                yy.append(s)
            gdic[str(c)+"-"+str(c+20)] = ly[lyz]
            lyz+=1
        count = 0
        c += 15
        s = tc

highlight_list = sorted(gdic.items(), key=lambda x: -x[1])

recommend_count = 0
base_url = "https://www.youtube.com/watch?v="+youtube_id

for highlight in highlight_list:
    timerange , _ = highlight
    time = timerange.split("-")
    s = int(time[0])
    e = int(time[1])
    if s == 0:
        continue
    if recommend_count == 5:
        break
    sm,ss = divmod(s,60)
    em,ee = divmod(e,60)
    print("recommend_point : ",str(sm)+":"+str(ss)+" ~ "+str(em)+":"+str(ee)," +-30s" , " macd_histgram : ",_)
    print("\t",base_url+"&feature=youtu.be&t="+str(s-30)+"&end="+str(e+30))
    html += '<h4>【'+str(s-30)+' +-30s】</h4>\n'
    html += "<p>macd_histgram : "+str(_)+"</p>\n"
    html += '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+youtube_id+'?start='+str(s-30)+'" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n'
        
    recommend_count += 1


html += '\n</body>\n</html>'

f = open("./data/"+youtube_id+".txt","w",encoding="utf-8")
f.write(kaku)
f.close()

h = open("./html/"+youtube_id+".html","w",encoding="utf-8")
h.write(html)
h.close()

p=open("index.html","r",encoding="utf-8")
data = p.read()
row = data.split("\n")
p.close()

# print(len(row))
# print(row[(len(row)-1)]+"\n")
# print(row[(len(row)-2)]+"\n")
# print(row[(len(row)-3)]+"\n")
# row[(len(row)-1)] = row[(len(row)-1)]
# row[(len(row)-1)] = row[(len(row)-3)]
# row[(len(row)-3)] = ('<p><a href="./html/'+youtube_id+'.html">'+title+"</p>")
row.pop()
row.pop()
row.pop()
row.append('<p><a href="./html/'+youtube_id+'.html">'+title+'</p>\n')
row.append("</body>\n")
row.append("</html>\n")
# print(len(row))
# print(row[(len(row)-1)]+"\n")
# print(row[(len(row)-2)]+"\n")
# print(row[(len(row)-3)]+"\n")
if already == 0:
    p = open("index.html","w",encoding="utf-8")
    addlist = '<p><a href="./html/'+youtube_id+'.html">'+title+"</p>"
    p.writelines(row)
    p.close()