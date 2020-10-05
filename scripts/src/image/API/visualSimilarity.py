import os 
import pandas as pd
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='f8aa7a6441db4878869c9604a8c27ac3')


def visualSim():
    
    imgUrls=pd.read_csv('scripts/src/image/API/test.csv')

    imageList=[ ClImage(url) for url in imgUrls['url'].to_list()]

    n=128
    chunks = [imageList[i * n:(i + 1) * n] for i in range((len(imageList) + n - 1) // n )]  

    for c in chunks:
        app.inputs.bulk_create_images(c)

    search= app.inputs.search_by_image(url='https://images-gmi-pmc.edge-generalmills.com/cbc3bd78-8797-4ac9-ae98-feafbd36aab7.jpg')

    for search_result in search:
        print('Score:',search_result.score,"| URL:",search_result.url)