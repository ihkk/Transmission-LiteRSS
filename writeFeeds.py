import json
import os
from urllib.parse import unquote
from urllib.parse import quote
import hashlib
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
from textwrap import fill

feedsPath = "feeds.json"

# 生成md5
def genearteMD5(str):
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return(hl.hexdigest())


def listFeeds():
	global saveStatus
	print("\nCurrent Feeds:")
	i = 0
	tab = PrettyTable()
	tab.field_names = ['ID','Feed Title','Download Path','RSS Url']
	for feed in feeds:
		tab.add_row([i, feeds[feed]['title'], feeds[feed]['path'], fill(unquote(feeds[feed]['url']), width=50)])
		i += 1
	tab.set_style(MSWORD_FRIENDLY)
	tab.hrules = True
	print(tab)
	# 提示是否有修改
	if saveStatus == 0:
		print("\033[0;31mJSON NOT SAVED.\033[0m")

def deleteFeed():
	global saveStatus
	deleteVal = input("Delete feed ID:\n")
	confirm = input(f"\nConfirm Delete {feeds[list(feeds)[int(deleteVal)]]['title']}? (y/n)\n")
	if confirm == "y": 
		feeds.pop(list(feeds)[int(deleteVal)])
		print("\n\033[0;31mDeleted.\033[0m \n")
		saveStatus = 0
	# listFeeds()

def addFeed():
	title = input("\nFeed Title: ")
	path = input("\nDownload Path: ")
	url = input("\nRSS Url: ")
	md5 = genearteMD5(url)
	feeds[title] = {
		'title': title,
		'path': path,
		'url': url,
		'md5': md5
	}
	print("\033[0;31mAdded.\033[0m ")
	global saveStatus
	saveStatus = 0
	# listFeeds()

def editFeed():
	global saveStatus
	editVal = input("Select feed ID:\n")
	print(f"Selected: {feeds[list(feeds)[int(editVal)]]['title']}\n\nPlease enter new values, keep blank to ramain existing value.")
	newTitle = input(f"\nTitle: {feeds[list(feeds)[int(editVal)]]['title']}\nNew Title: ")
	newPath = input(f"\nPath: {feeds[list(feeds)[int(editVal)]]['path']}\nNew Path: ")
	newUrl = input(f"\nURL: {feeds[list(feeds)[int(editVal)]]['url']}\nNew URL: ")
	newmd5 = genearteMD5(newUrl)
	if newTitle != "":
		feeds[list(feeds)[int(editVal)]]['title'] = newTitle
		saveStatus = 0
	if newPath != "":
		feeds[list(feeds)[int(editVal)]]['path'] = newPath
		saveStatus = 0
	if newUrl != "":
		newmd5 = genearteMD5(newUrl)
		feeds[list(feeds)[int(editVal)]]['url'] = newUrl
		feeds[list(feeds)[int(editVal)]]['md5'] = newmd5
		saveStatus = 0


def save():
	global saveStatus
	f = open(feedsPath, 'w', encoding='utf-8')
	f.write(json.dumps(feeds, ensure_ascii=False, indent=4, separators=(',', ':')))
	f.close
	print(f"\033[0;32mJSON Saved to {feedsPath}.\033[0m ")
	saveStatus = 1

if not os.path.exists(feedsPath):
	# 如果没有feeds文件，则创建一个空文件用于存储
	newFile = open(feedsPath, 'w')
	newFile.close

# 读取数据
try:
	with open(feedsPath, 'r', encoding='utf-8') as f:
		feeds = json.load(f)
except json.decoder.JSONDecodeError:
	feeds = {}

print("\n-- Transmission-LiteRSS v1.0 --\n--       Feeds Manager       --")
saveStatus = 1
while True:
	listFeeds()
	print("\n1. Add Feed\t2. Delete Feed\t\t3. Edit Feed\n4. Save\t\t5. Save and Exit\t6. Exit (without saving)\n")
	selection = input()
	if selection == "1":
		addFeed()
	elif selection == "2":
		deleteFeed()
	elif selection == "3":
		editFeed()
	elif selection == "4":
		save()
	elif selection == "5":
		save()
		exit()
	elif selection == "6":
		exit()
	# 导出feeds.json



