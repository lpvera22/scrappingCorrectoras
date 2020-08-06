from src.processing.seleniumBingSearch import getUrlCleansMultiprocessing, getUrlCleans
import pandas as pd
import time

cep = pd.read_csv('data/ceps.csv')
ceplist = cep['cep'].to_list()


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def main(search):
    aux = ceplist[:100]
    getUrlCleansMultiprocessing(search, aux, 1)
    # getUrlCleans(search, ceplist)


if __name__ == '__main__':
    start_time = time.time()
    keywords = ['SulAmerica', 'sulamerica']
    main(keywords)
    print('---%s seconds---' % (convert(time.time() - start_time)))
