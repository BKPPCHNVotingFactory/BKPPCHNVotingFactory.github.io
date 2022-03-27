import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
import os

# coding:utf-8
respostGet = requests.get("https://awards.komchadluek.net/")
# print(respostGet.text)

# 解析当前的html
soup = BeautifulSoup(respostGet.text, 'html.parser')

# 获取当前页面的script
json_obj = json.loads(soup.find("script", {"id": "__NEXT_DATA__"}).get_text())

pageProps = json_obj['props']['pageProps']
votes = pageProps['votes']

# with open('b.json', 'w') as fp:
#     json.dump(json_obj, fp, ensure_ascii=False)

# 数组集合
groupArr = [
    {
        "category_id": "group_4",
        "sumScore": 0,
        "item_id": ["item_10"],
        "item_score": 0,
        "category_name": "人气歌手"
    },
    {
        "category_id": "group_6",
        "sumScore": 0,
        "item_id": ["item_33"],
        "item_score": 0,
        "category_name": "人气情侣"
    },
    {
        "category_id": "group_7",
        "sumScore": 0,
        "item_id": ["item_229", "item_293"],
        "item_score": 0,
        "category_name": "人气演员"
    },
    {
        "category_id": "group_9",
        "sumScore": 0,
        "item_id": ["item_58"],
        "item_score": 0,
        "category_name": "热门剧集"
    },
]

# 组装之后的数组
resultArr = []
for groupItem in groupArr:
    groupObj = {
        # "sumScore": 0,
        "sumScore": '/',
        "list": [],
        "category_id": '',
        "category_name": ''
    }
    for voteItem in votes:
        active_item = 2
        if groupItem['category_id'] == voteItem['category_id']:
            groupObj['category_id'] = groupItem['category_id']
            groupObj['category_name'] = groupItem['category_name']
            # groupObj['sumScore'] += voteItem['raw_score']
            for item_vote_id in groupItem['item_id']:
                if voteItem['item_id'] == item_vote_id:
                    active_item = 1
            groupObj['list'].append({
                "item_name": voteItem['item_name'],
                # "score": voteItem['raw_score'],
                "score": "/",
                "active_item": active_item,
                # "weight": voteItem['score']
                "weight": "/"
            })
    # for item in groupObj['list']:
    #     item['weight'] = ("%.2f" %
    #                       ((item['score'] / groupObj['sumScore']) * 100)) + '%'

    # # 排序
    # groupObj['list'] = sorted(groupObj['list'],
    #                           key=lambda i: i['score'],
    #                           reverse=True)
    resultArr.append(groupObj)


# 转换北京时间 （UTC）
def format_time(bj_format="%Y-%m-%d %H:%M:%S"):
    uct_time = datetime.datetime.utcnow()
    bj_dt = uct_time + datetime.timedelta(hours=8)
    time_str = bj_dt.strftime(bj_format)
    return time_str


# 获取当前的时间
currentTime = format_time()
resultObj = {"date": currentTime, "data": resultArr}
# print(resultObj)

# 读取 json 文件
if not os.path.exists("vote.json"):
    with open('vote.json', 'w') as one:
        json_base = {"res": []}
        json.dump(json_base, one, ensure_ascii=False)

with open('vote.json', 'r') as fp:
    json_data = json.load(fp)

# print(json_data)

# 写入 json 文件
if not json_data["res"]:
    tempList = []
    tempList.append(resultObj)
    json_data["res"] = tempList
else:
    json_data["res"].append(resultObj)

sort_data = sorted(json_data["res"], key=lambda i: i['date'], reverse=True)
json_data["res"] = sort_data

with open('vote.json', 'w') as oldDate:
    json.dump(json_data, oldDate, ensure_ascii=False)
