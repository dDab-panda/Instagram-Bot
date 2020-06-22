import asyncio
import logging
import aiohttp
import json
import urllib.parse
import urllib.request
from instabot import Bot
from decouple import config

posturl = "https://www.instagram.com/p/B_IbIDAlaco/"


def downloadimages(list):
    logging.info('Starting Downloading....')
    for url in range(len(list)):
        dirlink = 'downloaded_images/instapic_'+str(url)+'.jpg'
        urllib.request.urlretrieve(list[url], dirlink)
    logging.info('Finished Downloading....')    

async def getimages(postlink):
    
    logging.info('Enter into the getpost function and now await')
    url = "https://instagram-grabber.p.rapidapi.com/grab/"
    querystring = {"url":postlink}
    headers = {
    'x-rapidapi-host': config('x-rapidapi-host'),
    'x-rapidapi-key': config('x-rapidapi-key')
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=querystring) as resp:
            data = await resp.text()
            jsondata = json.loads(data)
            mediadata = jsondata['media']
            for medielm in mediadata:
                imageurls.append(medielm['source'])
    logging.info('ImageUrls Found') 
    downloadimages(imageurls)           
   
def uploadpost():
    bot = Bot()
    bot.login(username = config('username'),password = config('password'))
    logging.info('Uploading starts ...')
    for i in range(len(imageurls)):
        filelink = 'downloaded_images/instapic_'+str(i)+'.jpg'
        bot.upload_photo(filelink,caption = "Credit @ei_thoughts")
    logging.info('Uploading finished....')



if __name__ == "__main__":
    imageurls=[]
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getimages(posturl))    
    uploadpost()