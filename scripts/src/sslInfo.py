import requests


def checkSSL(url):
    # url='http://'+url
    ssl = True
    # print(url)
    try:
        requests.get(url, verify=True)

    except:
        ssl = False

    return ssl
