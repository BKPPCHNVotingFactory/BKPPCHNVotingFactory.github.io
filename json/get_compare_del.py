import os, sys

# # 删除图片
# print("目录为: %s" %os.listdir(os.getcwd()))
if (os.path.exists("compareVote.png")):
    os.remove("compareVote.png")
else:
    print("要删除的文件不存在！")