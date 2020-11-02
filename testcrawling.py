import requests
from bs4 import BeautifulSoup

lyrics = []
musicId = 39897488
url2 = "https://music.naver.com/lyric/index.nhn?trackId="+str(musicId)
response = requests.get(url2)

html = response.text
soup = BeautifulSoup(html, 'html.parser')
requst_lyrics = soup.select('div.show_lyrics')

for i in requst_lyrics:
    lyrics.append(i)

s = ""
s = s + str(lyrics[0])
s = s[40:]
s = s[:-6]
s = s.replace('<br/>', '\n')
print(s)