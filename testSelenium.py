from selenium import webdriver
from bs4 import BeautifulSoup
RANK = 50 
driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get('https://www.melon.com/genre/song_list.htm?gnrCode=GN2100&steadyYn=Y')

html = driver.page_source
parse = BeautifulSoup(html, 'html.parser')
titles = parse.find_all("div", {"class": "ellipsis rank01"}) 
singers = parse.find_all("div", {"class": "ellipsis rank02"}) 
albums = parse.find_all("div",{"class": "ellipsis rank03"})
 
title = []
singer = []
album = []
 
for t in titles:
    title.append(t.find('a').text)
 
for s in singers:
    singer.append(s.find('span', {"class": "checkEllipsis"}).text)

for a in albums:
    album.append(a.find('a').text)

for i in range(RANK):
        print('%3d위: %s [ %s ] - %s'%(i+1, title[i], album[i], singer[i]))



url = "https://www.melon.com/search/song/index.htm?q={singer}&section=&searchGnbYn=Y&kkoSpl=N&kkoDpType=&ipath=srch_form"
for r in range(0, 51):
    lyric = []
    searchURL = url.replace('{singer}', singer[r])
    driver.get(searchURL)
    detail = driver.find_element_by_class_name('btn btn_icon_detail')
    detail.find_element_by_class_name('odd span').click()

    ##세부 정보 클릭하고 가사 크롤링
    #lyrics = parse.select('div.lyric on')
    
    #for i in lyrics:
    #    lyrics.append(i)

    #s = ""
    #s = s + str(lyrics[0])
    #s = s.replace('<br/>', '\n')
    #print(s)


    #title = []
    #titles = parse.find_all("div", {"class": "fc_gray"})
    #for t in titles:
        #title.append(t.find('a').text)

        #btn btn_icon_detail

