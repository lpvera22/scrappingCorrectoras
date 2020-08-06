import requests
import urllib.parse
import whois


def urlInfo(url):
    hostname = urllib.parse.urlparse(url).netloc
    return whois.whois(hostname)


def isUp(url):
    try:
        code = urllib.request.urlopen(url).getcode()
        if code == 200:
            return True
    except:
        return False
