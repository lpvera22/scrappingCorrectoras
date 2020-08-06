import requests
import urllib.parse
import whois
import requests


def urlInfo(url):
    hostname = urllib.parse.urlparse(url).netloc
    print(whois.whois(hostname))


def isUp(url):
    try:
        site_ping = requests.head(url)
        if site_ping.status_code < 400:

            return True
        else:

            return False
    except Exception:

        return False
