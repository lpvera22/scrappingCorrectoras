import pandas as pd
from src.processing.urlInfo import isUp


def concatUrls(n):
    frames = []
    for i in range(n):
        print(i)
        aux = pd.read_csv('out/' + str(i) + '.csv', header=0, index_col=False, sep=',')

        print(aux)
        frames.append(aux)
    # allUrls = pd.concat(frames, ignore_index=True)
    # return allUrls


def cleaningUrls(n):
    urls = concatUrls(n)
    # nurls = urls[urls.duplicated(['url'], keep='last')]
    # nurls['on'] = nurls['ur'].apply(isUp)
    # return nurls[nurls == 'on']
