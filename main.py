from src.seleniumBingSearch import getUrlCleansMultiprocessing
from src.cleaningUrls import cleaningUrls
from src.addingFeatures import addingFeatures
from src.googleDetectLogo import findLogoOnUrl
from src.getFontImg import getAllFonts
from src.googleImgProp import getAllColors
import pandas as pd
import time

cep = pd.read_csv('data/CEP-dados-2018-UTF8/ceps.csv')
ceplist = cep['cep'].to_list()


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def main(search):

    # getUrlCleansMultiprocessing(search)
    # cleaningUrls(8)
    # findLogoOnUrl()
    # getAllFonts()
    getAllColors()
    # addingFeatures()







if __name__ == '__main__':
    start_time = time.time()
    keywords = ['SulAmerica', 'sulamerica']
    main(keywords)
    print('---%s seconds---' % (convert(time.time() - start_time)))
