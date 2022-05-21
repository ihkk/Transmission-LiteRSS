import feedparser # rss解析
import json
import hashlib
import os
import re
from datetime import datetime, timedelta 
import arrow
from urllib.parse import quote
import subprocess

# feedparser.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
# 生成md5
def genearteMD5(str):
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return(hl.hexdigest())

# 添加磁力链接
def addMagnet(url, path):
	# print(f"Added:{url} -- {path}")
	subprocess.run(['/usr/bin/transmission-remote', '--auth', auth, '-a', url, '-w', path, '--seedratio', ratio])
	print(f"Magnet Task added to Transmission {path}")

# 【未完成】添加种子
def addTorrent(url, path, md5):
	torrentPath = torrentDir + md5 + ".torrent"
	url = quote(url)
	url = url.replace('%3A//', '://')
	subprocess.run(['wget', url, '-O', torrentPath])
	subprocess.run(['/usr/bin/transmission-remote', '--auth', auth, '-a', torrentPath, '-w', path, '--seedratio', '2'])
	print(f"Torrent Task added to Transmission {path}")

# 获取种子/磁链
def obtainMagnet(entry):
	links = entry.links
	for link in links:
		# dmhy & bangumi.moe & acg.rip & acgnx
		if link['type'] == 'application/x-bittorrent':
			url = link['href']
		# nyaa
		elif re.findall(r"http?[^'\{\}]+\.torrent",link['href']):
			url = link['href']
	# 判断是torrent还是magnet
	if (url.find("http://")!= -1) or (url.find("https://") != -1):
		return "torrent", quote(url).replace("%3A", ":")
	if url.find("magnet:?xt=") != -1:
		return "magnet", url

# 获取路径
currentPath = "/pyscripts/Transmission-LiteRSS/"
configPath = currentPath + "config.json"
feedsPath = currentPath + "feeds.json"
feedDir = currentPath + "feeds/"
torrentDir = currentPath + "torrents/"

if not os.path.exists(feedDir):
    os.makedirs(feedDir)

print(f"Reading Configs {configPath}")
# 读取配置
f = open(configPath, 'r', encoding='utf-8')
jsonConfig = f.read()
config = json.loads(jsonConfig)
f.close

# 读取订阅列表
print(f"Reading Feeds {feedsPath}")
f = open(feedsPath, 'r', encoding='utf-8')
jsonFeeds = f.read()
feeds = json.loads(jsonFeeds)
f.close


# 获取Transmission 登陆的用户名和密码
authUser = config['username']
authPass = config['password']
auth = authUser + ":" + authPass

# 获取时区
userTimezone = config['timeZone']

# 获取做种率
ratio = config['maxRatio']

print("Checking Feeds Directory...")
for feed in feeds:
	feedTitle = feeds[feed]['title']
	feedUrl = feeds[feed]['url']
	feedPath = feeds[feed]['path']
	feedMd5 = feeds[feed]['md5']
	jsonPath = feedDir + "[" + feedTitle + "][" + feedMd5 + '].json'
	print(f"\nChecking {jsonPath}")
	if not os.path.exists(jsonPath):
		# 如果该订阅无json，则创建一个空文件用于存储
		newFile = open(jsonPath, 'w')
		newFile.close
		print(f"{jsonPath} not found, new one created.")
	
	# 解析当前订阅的json并存入currentRecord
	try:
		with open(jsonPath, 'r', encoding='utf-8') as f:
			currentRecord = json.load(f)
	except json.decoder.JSONDecodeError:
		currentRecord = {}
	print(f"Fetching \033[33m{feedTitle}\033[0m from {feedUrl}...")
	# 解析rss
	currentFeed = feedparser.parse(feedUrl)
	print(f"\033[34m{len(currentFeed['entries'])} article(s)\033[0m obtained.")
	# 检索当前feed的每一个article
	for article in currentFeed['entries']:
		# 获取每个种子的信息
		currentName = article['title']
		print(f"Checking {currentName}")
		currentPubDate = article['published']
		if currentPubDate.find('GMT') != -1:
			currentPubDate = currentPubDate.replace('GMT','+0000')
		currentPubDate = arrow.get(currentPubDate, 'ddd, DD MMM YYYY HH:mm:ss Z').to(userTimezone).format('YYYY-MM-DD HH:mm:ss')
		# 此处更新为用obTainTorrentUrl来解析
		currentUrlType, currentURL = obtainMagnet(article)
		currentHash = genearteMD5(currentURL)
		if not currentHash in currentRecord:
			print(f"\033[32mNew {currentUrlType} Article Obtained.\033[0m")
			currentTime = arrow.now().format("YYYY-MM-DD HH:mm:ss")
			currentRecord[currentHash] = {
				"title": currentName,
				"pubTime": currentPubDate,
				"addTime": currentTime,
				"urlType": currentUrlType,
				"torrentUrl": currentURL}
			if currentUrlType == "magnet":
				addMagnet(currentURL, feedPath)
				subprocess.run(['logger', f"LiteRSS Created: {currentName}"])
			if currentUrlType == "torrent":
				addTorrent(currentURL, feedPath, currentHash)
				subprocess.run(['logger', f"LiteRSS Created: {currentName}"])
		else:
			print(f"{currentUrlType.title()} Article \033[31mExisted\033[0m.")

	# print(currentRecord)
	# 将新的json覆盖currentRecord
	f = open(jsonPath, 'w', encoding='utf-8')
	f.write(json.dumps(currentRecord, ensure_ascii=False, indent=4, separators=(',', ':')))
	f.close
subprocess.run(['logger', f'LiteRSS {len(feeds)} feeds Checked'])
print(f"\n\033[32mDone. {len(feeds)} feeds checked.\033[0m")