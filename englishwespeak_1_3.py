# Script for downloading materials for english podcasts from BBC's English We Speak
# @author     Cristian Gómez Alvarez <cristianpark@gmail.com>
#  
# http://www.bbc.co.uk/programmes/p02pc9zn/episodes/downloads?page=1
#
# Based on: https://www.dataquest.io/blog/web-scraping-tutorial-python/

from selenium import webdriver
import os.path
import urllib.request

## Rutas
FILE_PATH="/home/direktio/EnglishPodcasts/EnglishWeSpeak/"

if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)

os.chdir(FILE_PATH)

## There are 11 pages but the first three have another way to handle the mp3 link
for page in range(1, 4):
    print('--- Downloading audios from English We Speak page '+str(page))
    
    driver = webdriver.Firefox()
    driver.get("http://www.bbc.co.uk/programmes/p02pc9zn/episodes/downloads?page="+str(page))
    
    #Get items to download
    downloads=[]
    #From page 3 to 1, download style has changed
    #<a class="link-complex  br-subtle-bg-ontext br-subtle-bg-onbg--hover br-subtle-link-ontext--hover" href="http://open.live.bbc.co.uk/mediaselector/5/redir/version/2.0/mediaset/audio-nondrm-download/proto/http/vpid/p052dkgz.mp3" download="The English We Speak, It comes with the territory - p052dky0.mp3"> Higher quality (128kbps) </a>
    downloads=driver.find_elements_by_class_name("popup__list__item")
    assert "No results found." not in driver.page_source
    
    print("There are "+str(len(downloads))+" audio files on page "+str(page))
    
    for elem in downloads:
        if elem.text=="Higher quality (128kbps)":
            mp3link=elem.get_attribute("href")
         
            if mp3link!="None":        
                print("-- Downloading "+mp3link)
                #Save MP3 if it doesn't exists
                u = urllib.request.urlopen(mp3link)
                meta=u.info()
                meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
                meta_content = meta_func("Content-Disposition")
                filename=meta_content[0].split("filename=")[1].replace('"', '')
                 
                mp3file=FILE_PATH+filename
                 
                #Download the file        
                urllib.request.urlretrieve(mp3link, mp3file)
                print("-- Downloaded MP3 file "+mp3file)
    
    #Close connection
    driver.close()