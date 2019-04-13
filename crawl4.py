from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import csv
import time
import datetime
import re

startTime = time.time() 
# 코드 실행 시간 측정(시작시간)

options = webdriver.ChromeOptions() 
# 브라우저 숨기기
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu") 
# 브라우저 숨기기 끝 

drvdir = "/project/02_Software/webdrivers/chromedriver" 
# 크롬드라이버 위치

driver = webdriver.Chrome(drvdir, chrome_options=options) 
# url 크롤링 위한 load
driver2 = webdriver.Chrome(drvdir, chrome_options=options) 
# 게시글 크롤링 위한 load

starturl = 'https://www.instagram.com/explore/tags/' 
# 태그 검색 url
keyword = '주안역맛집' 
# 검색하고 싶은 태그 (추후 입력받게끔 해야함)
 
# 크롤링 횟수 (추후 입력받게끔 해야함)

driver.get(starturl+keyword) 
# 검색하고 싶은 태그 검색
time.sleep(3) # 브라우저 실행 후 기다려줘야하는 최소 시간

totalcount = driver.find_element_by_class_name('g47SY').text
driver.find_element_by_class_name('_9AhH0').click() # 첫 게시글 클릭

#time.sleep(1)

# 총 게시글 수 구하는 함수
def normalize(s):
    if s == None:
        return 0
    elif s != None:
        return s.replace(',', '').strip()


tcnt = normalize(totalcount)


startcount = 0 # 크롤링 횟수 측정 위한 변수
endcount = 10




now = datetime.datetime.now()
filename = keyword+'_%s.csv' % now.strftime('%Y-%m-%d %H:%M:%S')
csvfile = open('./datalist/' + filename, 'w')
reader = csv.writer(csvfile)
reader.writerow(['작성자', '작성날짜', '게시글내용', '좋아요갯수', '댓글수', '해시태그'])
    
for crwal in range(endcount):
    startcount += 1 # 버튼 한번 클릭당 카운트 1 증가
    print('진행상황 ', startcount, '개') # 현재 진행상황 체크
    crwalurl = driver.current_url # 현재 페이지의 url load
    #time.sleep(1)
    driver.find_element_by_xpath("//a[@class='HBoOv coreSpriteRightPaginationArrow']").click() # 다음 게시글 이동 버튼 클릭

    
    
    
    driver2.get(crwalurl) # 크롤링 한 url로 접속
    
    crwsrc = driver2.page_source # 접속한 페이지 소스 load
    soup = BeautifulSoup(crwsrc, 'html.parser') # 파싱
    
    hashtag = ""
    for i in soup.select('.C4VMK span a'): #해시태그 찾기
        if i.text.startswith("@"): #사용자 태그 제거
            continue
        else:
            hashtag += i.text
    print(hashtag) # 해시태그 출력
            #HashTags.append(i.text)
        
    UserId = soup.find('h2', class_='_6lAjh').text #작성자 찾기
    print('작성자 : ',UserId) #작성자 출력
    
    ### 작성 날짜 찾기 ###
    writedate = str(soup.find('a', class_='c-Yi7'))
    writedate = re.search(r'\d{4}-\d{2}-\d{2}', writedate)
    writedate = writedate.group(0)
    print(writedate)
    
    #동영상의 경우 조회수를 클릭해야 좋아요수가 나오기 때문에 try문 사용
    try: 
        like = driver2.find_element_by_class_name('Nm9Fw').find_element_by_tag_name('span').text
        print('좋아요 : ',like) #좋아요 출력
    except NoSuchElementException:
        like = "0"
        print("좋아요 : ", like)
    except:
        driver2.find_element_by_class_name('vcOH2').click()
        like = driver2.find_element_by_class_name('vJRqr').find_element_by_tag_name('span').text
        print("좋아요 : ",like) #좋아요 출력    


    ### 게시글 내용 추출 ###
    content = str(soup.find('div', class_='C4VMK').find('span'))
    content = re.sub('<a.*?>.*?</a>', '', content, 0)
    content = re.sub('<br/>', '\n', content, 0)
    content = re.sub('<.+?>', '', content, 0)
    print(content)
    
    ### 댓글 수 가져오기 ###
    
    while True:
        try:
            driver2.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/div[2]/div[1]/ul/li[2]/button").click()
            element = driver2.find_element_by_css_selector("#react-root > section > main > div > div > article > div.eo2As")
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
        except:
            crwsrc2 = driver2.page_source # 접속한 페이지 소스 load
            soup2 = BeautifulSoup(crwsrc2, 'html.parser') # 파싱
            cocount = soup2.findAll("li", class_="gElp9")
#        for i in soup.select('.gElp9'):
#            count+=1
            break
    cocount = int(len(cocount))
    print(cocount)
    
    
    reader.writerow([UserId, writedate, content, like, cocount, hashtag])
    




    
    
#if startcount == endcount: # startcount와 endcount 비교해서 break
csvfile.close()
driver.close() # 드라이버 닫아주기
driver2.close()
 #       break
    
    
    




endTime = time.time() - startTime
print('걸린 시간은 : ',endTime) 



        
        