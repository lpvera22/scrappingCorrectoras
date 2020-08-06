import requests
import urllib.parse
import whois


def urlInfo(url):
    hostname = urllib.parse.urlparse(url).netloc
    print(whois.whois(hostname))



