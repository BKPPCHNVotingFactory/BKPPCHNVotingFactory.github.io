# 引入 pandas 数据
import os,sys
import pandas as pd
import json
import time
import dataframe_image as dfi

pd.set_option('display.unicode.ambiguous_as_wide', True)  #处理数据的列标题与数据无法对齐的情况
pd.set_option('display.unicode.east_asian_width', True)  #无法对齐主要是因为列标题是中文

# 打开 json
with open('vote.json', 'r', encoding='utf8') as fp:
    json_data = json.load(fp)

# 整理数据
headList = []
obj = {
    'บิวกิ้น พุฒิพงศ์ - BK': [],
    'พีพี กฤษฎ์ - PP': [],
    'นุนิว ชวรินทร์ - Duo': [],
    'BK 日增长值': [],
    'PP 日增长值': [],
    'Duo 日增长值': []
}
for item in json_data['res']:
    tempTime = time.strptime(item['date'], "%Y-%m-%d %H:%M:%S")
    resultTime = time.strftime("%Y-%m-%d", tempTime)
    headList.insert(0, resultTime)
    for i in item['data'][0]['list']:
        for name in obj.keys():
            if i['item_name'] in name:
                obj[name].insert(0, i['score'])

# 计算日增长值
for i in range(0, len(headList)):
    if i == 0:
        obj['BK 日增长值'].append(obj['บิวกิ้น พุฒิพงศ์ - BK'][i])
        obj['PP 日增长值'].append(obj['พีพี กฤษฎ์ - PP'][i])
        obj['Duo 日增长值'].append(obj['นุนิว ชวรินทร์ - Duo'][i])
    else:
        obj['BK 日增长值'].append(
            abs(obj['บิวกิ้น พุฒิพงศ์ - BK'][i] -
                obj['บิวกิ้น พุฒิพงศ์ - BK'][i - 1]))
        obj['PP 日增长值'].append(
            abs(obj['พีพี กฤษฎ์ - PP'][i] - obj['พีพี กฤษฎ์ - PP'][i - 1]))
        obj['Duo 日增长值'].append(
            abs(obj['นุนิว ชวรินทร์ - Duo'][i] -
                obj['นุนิว ชวรินทร์ - Duo'][i - 1]))

resultPd = {'date': headList}
resultPd.update(obj)
# pd.DataFrame(resultPd)
df = pd.DataFrame(resultPd)

df.drop(labels = [
    'บิวกิ้น พุฒิพงศ์ - BK', 'พีพี กฤษฎ์ - PP', 'นุนิว ชวรินทร์ - Duo'
], axis=1)

# # 删除图片
# print("目录为: %s" %os.listdir(os.getcwd()))
if (os.path.exists("compareVote.png")):
    os.remove("compareVote.png")
else:
    print("要删除的文件不存在！")

# 数据基础统计
df_style = df.style.background_gradient()
dfi.export(obj = df_style,filename = "compareVote.png",fontsize = 30)

# 完成
# finish
