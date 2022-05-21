# Transmission-LiteRSS

Transmission-LiteRSS is a tiny Python script that helps you fetching public Torrent RSS feeds and add tasks to Transmission.

## Support

The scripts is tested to supports RSS links from the following ACG sites; Other RSS links might also be supported. You are welcomed to push issues if the script doesn’t work with other sites.

```
Nyaa
DMHY
acg.rip
acgnx.se
bangumi.moe
```

As the scripts is added into crontab, all RSS feed updates in `feeds.json` will be checked. The download records for each feed are stored in `feeds/[RSS Name][RSS hash].json` automatically.

## Requirement

The scripts requires Python 3 and is designed to run in Linux.

Following packages should be installed in your system:

```
transmission-daemon
transmission-remote
```

Following Python modules are required (use `pip` to install):

```
feedparser
json
hashlib
re
datetime
arrow
subprocess
urllib
```

## Setup

You may follow the steps below to run this script.

### 1. config

**Open `config.json` and fill in the required values.**

`username`: Transmission RPC username

`password`: Transmission RPC password

`timeZone`: The time zone you want to use for article fetching records. Time zones should be in the format of `ZZZ`, as `Asia/Baku, Europe/Warsaw, GMT...` Check [Time Zone Database](https://www.iana.org/time-zones) for more information.

`maxRatio`: Maximum upload ratio for the tasks created.

### 2. path

**Open `main.py` and fill in the following lines**

- Line 22&31, replace `/usr/bin/transmission-remote` with your `transmission-remote` path (use `whereis transmission-remote` in shell).
- Line 51, fill in the current path of the script.
- Line 133, 136&145 will deliver message to `logger` and save message in system log (for Openwrt). Just delete the lines if you don’t need them.

### 3. Add feeds

Use `writeFeeds.py ` and add feeds that you need. For details please turn to next section.

### 4. Crontab

Add the following crontab to make sure the scripts automatically runs.

```c
*/5 * * * * python /pyscripts/Transmission-LiteRSS/main.py
```

Replace with your own script directory.

`*/5` means the script run once every 5 minutes, meaning that the RSS updates are checked every 5 minutes. Change to the value you prefer.

## WriteFeeds

`feeds.json` should be filled in the structure like:

```json
{
    "RSS 1":{
        "title":"RSS 1 Title",
        "path":"/opt/RSS1",
        "url":"https://rss/1/url",
        "md5":"c51c90c2d18c38c398da2c5191ff8932"
    },
    "RSS 2":{
        "title":"RSS 2 Title",
        "path":"/tmp/RSS2/path",
        "url":"https://rss/2/url",
        "md5":"1ba71deb5923a64ae12ab798b026855f"
    }
}
```

The `md5` value is calculated from `url`, however, this only works as an ID for each RSS subscript, and will not be verified during the daily tasks.

#### Feeds Manager

A `Feeds Manager` is provided for you to manage feeds easily. Run the command below in shell.

```shell
python writeFeeds.py
```

The `Feeds Manager` will help you manage your feeds, as an example showing below. You can `Add`, `Delete`, `Edite` your feeds using this script. Remember to `save` after any edit. The script will calculate `md5` value of each `RSS Url` automatially.

![](https://s2.loli.net/2022/05/21/yKBmCNpg8WGk7oF.png)

## Article record

A download record for each feed will be generated in `feeds/[RSS Name][RSS hash].json`. 

The record file follows the structure like:

```json
{
    "torrentUrl md5":{
        "title":"[XX字幕组][Anime Title][EP01][1080P]",
        "pubTime":"2022-04-01 00:00:00",
        "addTime":"2022-05-16 14:34:29",
        "urlType":"magnet",
        "torrentUrl":"magnet:?xt=urn:btih:XXXXXXXXXXXXXXXXx"
    },
    "torrentUrl md5":{
        "title":"[XX字幕组][Anime Title][EP02][1080P]",
        "pubTime":"2022-05-10 09:35:07",
        "addTime":"2022-05-16 14:34:29",
        "urlType":"torrent",
        "torrentUrl":"https://rss/file.torrent"
    }
}
```

The file will be generated automatically.

If you want to add any of the existed tasks again, you may delete the corresponding part in json file.