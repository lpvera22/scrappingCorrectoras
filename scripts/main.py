import sys
import os
import pathlib
import os
import glob

sys.path.append('/root/projects/scrappingCorrectoras/database')
from src.seleniumBingSearch import getUrlCleansMultiprocessing,getUrlCleansNoMult,getUrlCleans
from src.cleaningUrls import cleaningUrls
from src.addingFeatures import addingFeatures, addingColorsAndFontInfo,addingFeaturesByImgUrl
from src.googleDetectLogo import findLogoOnUrl,getallImgUrlwithLogo
from src.getFontImg import getAllFonts,getFontsByUrlImg
from src.googleImgProp import getAllColors,getColorsByImgUrl
from src.ScrapingToDb import getScrapingtoDb
from src.getallImg import seleniumGetImg
import os, shutil
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
    #Done correctly!!
    # getUrlCleansNoMult(search,0)
    getUrlCleansMultiprocessing(search,5)
    print('cleaning urls...')
    cleaningUrls(5)
    dfCleaned = pd.read_csv('scripts/out/urlCleaned.csv')    
    print(dfCleaned)
    f = open('scripts/out/imgUrlsWithSet.csv', 'w')
    f.write('url;imgSrc')
    f.write('\n')
    urlsCeps=set(dfCleaned.url)
    
    for url in urlsCeps :
        
        print(url)
        m = re.search('https?://([A-Za-z_0-9.-]+).*', url)
        seleniumGetImg(url,str(m.group(1)),f)
    getallImgUrlwithLogo()
    
    
    
    getFontsByUrlImg()
    
    
    getColorsByImgUrl()
    
    addingFeaturesByImgUrl()
    
    print('*************DONE=====>TO DB====>********')
    getScrapingtoDb()

    

    
    folder = 'scripts/out/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


    


if __name__ == '__main__':
    start_time = time.time()
    keywords = ['SulAmerica','Sulamerica seguros','Sulamerica saude','plano de saude sulamerica']
    # keywords = ['sulamerica']
    main(keywords)
    print('---%s seconds---' % (convert(time.time() - start_time)))
