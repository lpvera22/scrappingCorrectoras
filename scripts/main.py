import sys
import os
import pathlib
# print(sys.path)
# sys.path.append('/media/laura/dados/Projects/Work/searchKeyword/database')
# sys.path.append('/home/lvera/projects/scrappingCorrectoras/database')
sys.path.append('/root/projects/scrappingCorrectoras/database')
from src.seleniumBingSearch import getUrlCleansMultiprocessing,getUrlCleansNoMult,getUrlCleans
from src.cleaningUrls import cleaningUrls
from src.addingFeatures import addingFeatures, addingColorsAndFontInfo,addingFeaturesByImgUrl
from src.googleDetectLogo import findLogoOnUrl,getallImgUrlwithLogo
from src.getFontImg import getAllFonts,getFontsByUrlImg
from src.googleImgProp import getAllColors,getColorsByImgUrl
from src.ScrapingToDb import getScrapingtoDb
from src.getallImg import seleniumGetImg

import pandas as pd
import time
import re
# /home/lvera/projects/scrappingCorrectoras/scripts/credentials.json

os.environ['KEY'] = 'AIzaSyAMgJ9UV5-81zIDTy0kMXYK2ILsfFYWh20'


def convert(seconds):
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def main(search):
    # getUrlCleansNoMult(search,2)
    getUrlCleansMultiprocessing(search,2)
    cleaningUrls(2)
    dfCleaned = pd.read_csv('scripts/out/urlCleaned.csv')
    
    f = open('scripts/out/imgUrls.csv', 'w')
    f.write('url;cep;imgSrc')
    f.write('\n')
    urlsCeps=list(zip(dfCleaned.url, dfCleaned.cep))
    for url,cep in urlsCeps :
        
        print(url,cep)
        m = re.search('https?://([A-Za-z_0-9.-]+).*', url)
        seleniumGetImg(url, cep,str(m.group(1)),f)
    getallImgUrlwithLogo()
    
    
    
    getFontsByUrlImg()
    
    
    getColorsByImgUrl()
    
    addingFeaturesByImgUrl()
    
    # #to delete
    # # addingColorsAndFontInfo()
    
    getScrapingtoDb()
    
    


if __name__ == '__main__':
    start_time = time.time()
    keywords = ['SulAmerica']
    main(keywords)
    print('---%s seconds---' % (convert(time.time() - start_time)))
