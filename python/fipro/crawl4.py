from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import csv
import datetime

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
tag = '주안역맛집' 
# 검색하고 싶은 태그 (추후 입력받게끔 해야함)
 
# 크롤링 횟수 (추후 입력받게끔 해야함)

driver.get(starturl+tag) 
# 검색하고 싶은 태그 검색
time.sleep(3) # 브라우저 실행 후 기다려줘야하는 최소 시간
driver.find_element_by_class_name('_9AhH0').click() # 첫 게시글 클릭

#time.sleep(1)

# 총 게시글 수 구하는 함수
def normalize(s):
    if s == None:
        return 0
    elif s != None:
        return s.replace(',', '').strip()

totalcount = driver.find_element_by_class_name('g47SY').text
tcnt = normalize(totalcount)

endcount = 50

startcount=0 # 크롤링 횟수 측정 위한 변수

# 리스트 선언
UserIds = []
HashTags = []


def crawl(crwalurl): #크롤링 함수
    driver2.get(crwalurl) # 크롤링 한 url로 접속
    
    crwsrc = driver2.page_source # 접속한 페이지 소스 load
    soup = BeautifulSoup(crwsrc, 'html.parser') # 파싱
    
    for i in soup.select('.C4VMK span a'): #해시태그 찾기
        if i.text.startswith("@"): #사용자 태그 제거
            continue
        else:
            print(i.text) # 해시태그 출력
            HashTags.append(i.text)
        
    #name = soup.find('h2', class_='_6lAjh').text #작성자 찾기
    #print('작성자 : ',name) #작성자 출력
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

while True: # startcount가 endcount와 같아질때까지 반복
    
    crwalurl = driver.current_url # 현재 페이지의 url load
    crawl(crwalurl) # 현재 페이지의 url로 크롤링 시작
    #time.sleep(1)
    driver.find_element_by_xpath("//a[@class='HBoOv coreSpriteRightPaginationArrow']").click() # 다음 게시글 이동 버튼 클릭
    if startcount == endcount: # startcount와 endcount 비교해서 break
        break
    
    startcount += 1 # 버튼 한번 클릭당 카운트 1 증가
    print('진행상황 ', startcount, '개') # 현재 진행상황 체크
    

driver.close() # 드라이버 닫아주기
driver2.close()


now = datetime.datetime.now()
filename = keyword+'_%s.csv' % now.strftime('%Y-%m-%d %H:%M:%S')

with open('./datalist/' + filename, 'w') as csvfile:
    reader = csv.writer(csvfile)
    #해시태그, 빈도 출력
    reader.writerow(['HashTag', 'Frequency'])
    result = Counter(HashTags) #해시태그별 빈도출력
    rank_list = sorted(result.items(), key = lambda x:x[1], reverse = True) #빈도별 내림차순 정렬
    for key in rank_list:
        reader.writerow([key[0], key[1]])

        #유저아이디, 해시태그 출력
        # reader.writerow(['UserID', 'HashTag'])
        # for UserId in UserIds:
        #     for HashTag in HashTags:
        #         reader.writerow([UserId, HashTag])
    print('파일을 저장했습니다. 파일명 : %s' % filename)
    # os.system('say "작업이 끝났습니다."')
print("작업이 끝났습니다. 다음 작업을 실행해주세요!") 



endTime = time.time() - startTime
print('걸린 시간은 : ',endTime) 



        
        