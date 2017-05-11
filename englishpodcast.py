# Script for downloading materials for english podcasts from brittish council
# @author     Cristian Gómez Alvarez <cristianpark@gmail.com>
#  
# https://learnenglish.britishcouncil.org/en/elementary-podcasts
#
# Based on: https://www.dataquest.io/blog/web-scraping-tutorial-python/

import requests
import wget
import os.path
from bs4 import BeautifulSoup
import re

## Rutas
RUTA_ARCHIVOS="/home/direktio/EnglishPodcasts/"

## There are 4 series divided into some episodes (max 20 episodes)
for serie in range(1, 5):
    for episode in range(1, 21):
        page=requests.get("https://learnenglish.britishcouncil.org/en/elementary-podcasts/series-"+str(serie).zfill(2)+"-episode-"+str(episode).zfill(2))
        
        print("--- Page status: "+str(page.status_code))
        
        if(page.status_code<=299):
            soup = BeautifulSoup(page.content, 'html.parser')
            
            #Check if there are any downloads to make
            if(len(soup.select("span.file a"))>0):
                print("--- All criteria meeted, grabbing files from serie "+str(serie)+" episode "+str(episode))
                
                #Determine position of transcript file
                pdfposition=1
                pattern=re.compile("^Download Support pack and Transcript[^\w]*$")
                 
                if len(soup.select("span.file a"))==4:  #Sometimes the last element is the transcript with support pack
                    pdfposition=3 if pattern.match(soup.select("span.file a")[3].get_text()) else 1
                    
                elif len(soup.select("span.file a"))==5:  #Transcript is the fourth link
                    pdfposition=3
            
                #Find the link for audio and transcript (there are four span with file class: the first one is audio, the last one transcript)
        #         print(soup.find_all('span', class_='file'))    ##With this we need to navigate children
                mp3link=soup.select("span.file a")[0]['href']
                pdflink=soup.select("span.file a")[pdfposition]['href'] 
                print("- Links adquired")
                     
                #Create the directory if it doesn't exists
                folder=RUTA_ARCHIVOS+"/Series"+str(serie).zfill(2)
                      
                if not os.path.exists(folder):
                    os.makedirs(folder)
                  
                #Check if file exists
                mp3file=folder+"/s"+str(serie).zfill(2)+"_e"+str(episode).zfill(2)+"_Audio.mp3"
                pdffile=folder+"/s"+str(serie).zfill(2)+"_e"+str(episode).zfill(2)+"_Transcript.pdf"
                 
                #Save MP3 if it doesn't exists
                if(not os.path.isfile(mp3file)):
                    out=wget.download(mp3link, out=mp3file)
                    print("Downloaded MP3 file "+out)
                        
                #Save PDF
                if(not os.path.isfile(pdffile)):
                    out=wget.download(pdflink, out=pdffile)
                    print("Downloaded PDF file "+out)