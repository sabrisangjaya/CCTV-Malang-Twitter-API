# import the module
import tweepy
import requests
import schedule
import time
import urllib.request
import ssl
import os
from datetime import datetime
from PIL import Image,ImageChops,ImageDraw 
import pandas as pd
import random

ssl._create_default_https_context = ssl._create_unverified_context
    
# assign the values accordingly
consumer_key = "CENSORED"
consumer_secret = "CENSORED"
access_token = "CENSORED"
access_token_secret = "CENSORED"
 
# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  
# set access to user's access key and access secret 
auth.set_access_token(access_token, access_token_secret)
  
# calling the api 
api = tweepy.API(auth)

df = pd.read_excel('data.xlsx',index_col="ID")



def cctvcuaca():
    datatweet=df.loc[df['group']==random.randrange(1,101)]
    print(datatweet)
    url_cuaca="https://api.openweathermap.org/data/2.5/weather?lat="+str(datatweet.loc[datatweet.index[0],'latitude'])+"&lon="+str(datatweet.loc[datatweet.index[0],'longitude'])+"&lang=en&units=metric&appid=10cd7d5b04f5c284fd91d440a416172c"
    print(url_cuaca)    
    resp = requests.get(url=url_cuaca)
    data_cuaca = resp.json()
    isi_tweet="infomalang Suhu "+str(data_cuaca["main"]["temp"])+u'\N{DEGREE SIGN}'+"C. Cuaca "+str(data_cuaca["weather"][0]["main"])+" "+str(data_cuaca["weather"][0]["description"])

    if(len(datatweet)==1):
        imgcoordinate=[[0,0]]
        base_image = Image.new("RGBA", (1920, 1080), (255, 255, 255))
    elif(len(datatweet)==2):
        imgcoordinate=[[0,0],[0,1080]]
        base_image = Image.new("RGBA", (1920, 2160), (255, 255, 255))
    elif(len(datatweet)==3):
        imgcoordinate=[[0,0],[1920,0],[960,1080]]
        base_image = Image.new("RGBA", (3840, 2160), (255, 255, 255))
    elif(len(datatweet)==4):
        imgcoordinate=[[0,0],[1920,0],[0,1080],[1920,1080]]
        base_image = Image.new("RGBA", (3840, 2160), (255, 255, 255))
    elif(len(datatweet)==5):
        imgcoordinate=[[0,0],[1920,0],[960,1080],[0,2160],[1920,2160]]
        base_image = Image.new("RGBA", (3840, 3240), (255, 255, 255))
    for i in range(0,len(datatweet)):
        filename="img"+str(i)+".jpg"
        try:
            urlrequest="http://proxy.cctv.malangkota.go.id/image?host="+datatweet.loc[datatweet.index[i],"host"]
            print(urlrequest)
            urllib.request.urlretrieve(urlrequest, filename)
            foreground_image=Image.open(filename).convert("RGBA")
        except:
            error_img=Image.new("RGB", (1920, 1080), (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)))
            foreground_image=error_img.convert("RGBA")
        base_image.paste(foreground_image,(imgcoordinate[i]),foreground_image)
    width, height = base_image.size
    new_height = 1080
    new_width  = int(new_height * width / height)
    base_image=base_image.resize((new_width, new_height), Image.ANTIALIAS)
    base_image.save("mediacctv.png")
    media = api.media_upload(filename="mediacctv.png")
    updatetweet=api.update_status(status=isi_tweet, media_ids=[media.media_id])
    print("Update status at : "+datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
      
schedule.every(15).minutes.do(cctvcuaca)

while 1:
    schedule.run_pending()
    time.sleep(1)