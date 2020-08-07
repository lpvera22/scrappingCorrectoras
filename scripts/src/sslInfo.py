import requests


def checkSSL(url):
    ssl = True
    try:
        requests.get(url, verify=True)

    except:
        ssl = False

    return ssl
