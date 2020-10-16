import os 
import pandas as pd
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='3dd519d40f6e473ead0986152e2b8edf')


def trainData(imgUrls):

    imageList=[ClImage(url) for url in imgUrls['imgSrc'].to_list()]

    n=128
    chunks = [imageList[i * n:(i + 1) * n] for i in range((len(imageList) + n - 1) // n )]  

    for c in chunks:
        app.inputs.bulk_create_images(c)
def search(imgUrls):

    search= app.inputs.search_by_image(url='https://logodownload.org/wp-content/uploads/2017/10/sulamerica-logo.png')
    L={}

    for search_result in search:
        L[search_result.url]=search_result.score
        print('Score:',search_result.score,"| URL:",search_result.url)

    f={}
    for u in imgUrls['imgSrc'].to_list():
        print(u)
        if u not in L.keys():
            f[u] = -1

        else:
            print(L[u])
            f[u] = L[u]



    
    d=pd.DataFrame(f.items(), columns=['imgSrc', 'score'])
    
    return d
