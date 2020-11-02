from selenium.webdriver import Chrome
#크롬드라이버 연결
delay=0.1
browser = Chrome()
browser.implicitly_wait(delay)


start_url = 'https://music.naver.com/'
browser.get(start_url) 