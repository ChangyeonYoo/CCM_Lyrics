import re
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from urllib3 import request
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

#CCM 곡 순위는 50위 까지만 존재
RANK = 50 
driver = webdriver.Chrome()
driver.implicitly_wait(3)

#CCM 차트 접근
driver.get('https://www.melon.com/genre/song_list.htm?gnrCode=GN2100&steadyYn=Y')

html = driver.page_source
parse = BeautifulSoup(html, 'html.parser')

#가수 크롤링
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


print(singer)
singer_set = set(singer) #집합set으로 변환
singer_list = list(singer_set) #list로 변환
print(singer_list)

#검색이 완료된 가수
serched_singer = []
#가수 ID
singer_id = []

#검색창 접근
url = "https://www.melon.com/search/total/index.htm?q={singer}&section=&searchGnbYn=Y&kkoSpl=N&kkoDpType=&ipath=srch_form"
driver.get(url)

for s in singer_list:
    time.sleep(3)
    #search = driver.find_element_by_xpath('//*[@id="top_search"]')
    #search.send_keys(Keys.CONTROL + "a")
    #search.clear()

    #가수 검색
    #search.send_keys(Keys.RETURN)

    #가수 검색2
    sURL = "https://www.melon.com/search/total/index.htm?q={singer}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&linkOrText=T&ipath=srch_form"
    sURL = sURL.replace('{singer}', s)
    print(sURL)
    driver.get(sURL)

    try:
        #검색된 가수 클릭
        driver.find_element_by_xpath('//*[@id="conts"]/div[3]/div[1]/div[1]/div/a/strong').click()
        url = driver.current_url
        #현재 URL에서 가수 ID부분을 크롤링
        id = url.replace('https://www.melon.com/artist/timeline.htm?artistId=', '')
        singer_id.append(id)

    except NoSuchElementException:
        print("검색된 가수 없음")

l1 = 'https://www.melon.com/artist/song.htm?artistId='
# idol_id
l2 = '#params%5BlistType%5D=A&params%5BorderBy%5D=ISSUE_DATE&params%5BartistId%5D='
# idol_id
l3 = '&po=pageObj&startIndex='


CCM_Lyrics = pd.DataFrame(
    {
    'artist':['testArtist'],
    'title':['testTitle'],
    'lyrics':['testLyrics']
})

i = 0
title_c = []
lyrics_c = []
for id in singer_id:
    n = 1
    while True:
        driver.get(l1+str(id)+l2+str(id)+l3+str(n))

        try:
            #곡 세부정보 검색
            driver.find_element_by_css_selector('tr:nth-child(1) > td:nth-child(3) > div > div > a.btn.btn_icon_detail > span').click()
            
            # 제목 크롤링(제목은 없지 않기 때문에 예외 없음)
            title_c.append(driver.find_element_by_xpath('//*[@id="downloadfrm"]/div/div/div[2]/div[1]/div[1]').text)
            
            try:
                #가사 크롤링
                lyrics_c.append(driver.find_element_by_xpath('//*[@id="d_video_summary"]').text)
            except NoSuchElementException as e:
                print('NULL')

            n+=1
        
        except NoSuchElementException as e:
            dataList = [(singer_list[i], title_c[-1], lyrics_c[-1])]
            CCM_Lyrics = CCM_Lyrics.append(dataList, colums = ['artist', 'title', 'lyrics'])
            i += 1
            break

CCM_Lyrics.to_csv('CCMLyrics_test01.csv')

    #if singer[r] not in serched_singer:
    #    searchURL = url.replace('{singer}', singer[r])
    #    driver.get(searchURL)
    #    time.sleep(5)
    #    serched_singer.append(singer[r])
    #    print(serched_singer)

    #   html = driver.page_source
    #    parse = BeautifulSoup(html, 'html.parser')

    #    for tag in parse.select('#tb_list.d_song_list.songTypeOne a[href*=goSongDetail]'):
    #        print("for tag문 실행")
    #        title = tag.text
    #        print(title)
    #        js = tag['href']
    #        matched = re.search(r",'(\d+)'\);", js)
    #        if matched:
    #            song_id = matched.group(1)
    #            song_url = 'https://www.melon.com/song/detail.htm?songId=' + song_id
    #            print(song_url)
               
    #else :
    #    continue
    
    #html = request.get
    #serched_singer.append(singer[r])
    #for tag in 
    #for i in details:
    #    print(i)
    #    i.onclick()
    #    time.sleep(5)
    #for details in driver.find_elements_by_link_text('곡정보 보기'):
    #    time.sleep(5)
    #    lyric=[]
    #    details.onclick()
    #    content = driver.find_element_by_class_name('lyric on')

    #    for i in content:
    #        lyric.append(content.text)
    #        print(lyric)
    #    time.sleep(5)
    #    driver.back()


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

        #btn btn_icon_detai