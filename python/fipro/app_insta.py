import json
import csv
import re
import sys
import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import Counter

# sys.path.append('./libraries')
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
driver = webdriver.Chrome('/project/02_Software/webdrivers/chromedriver', chrome_options=options)
driver.implicitly_wait(5)

#해시태그 키워드 지정
keyword = '인천역맛집'

def get_search_keyword(keyword):
    url = "https://www.instagram.com/explore/tags/" + keyword + "/" 
    return driver.get(url)

def randomtime_set():
    random.seed(datetime.datetime.now())
    Ran_Time = random.random()
    if Ran_Time <= 1:
        time.sleep(Ran_Time)
        # print(Ran_Time)
        # print('-' * 20)
    else:
        Ran_Time2 = Ran_Time + 0.4
        time.sleep(Ran_Time2)
        # print(Ran_Time2)
        # print('-' * 20)

def normalize(s):
    if s == None:
        return 0
    elif s != None:
        return s.replace(',', '').strip()

UserIds = []
HashTags = []

def get_hashtag():
    totalcount = driver.find_element_by_class_name('g47SY').text
    print("인스타그램에서 " + keyword + "에 대한 크롤링을 시작합니다.")
    print("총 게시물:", totalcount) # 검색tag의 총 게시물 수 출력 ('g47SY') 
    tcnt = normalize(totalcount)
    
    
    elem = driver.find_element_by_tag_name("body") 
    n = 0
    alt_list = []
    while n < 2: #int(tcnt) -> 전수조사  
        a_tag = driver.find_elements_by_tag_name('a')
        for i in range(len(a_tag)):
            addr = a_tag[i].get_attribute('href')
            pattern = re.compile(r'./p/.')
            match = pattern.search(addr)
            
            if match is not None:
                alt_list.append(addr)
                print("addr : "+ addr)
            else:
                pass
                
        elem.send_keys(Keys.PAGE_DOWN)
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        n += 1

    alt_list = list(set(alt_list))
    for j in alt_list:
        driver.get(j)
        hash_url = driver.find_elements_by_tag_name('a')
        # user_id = hash_url[1].get_attribute('text')
        # UserIds.append(user_id)
        user_tag = driver.find_elements_by_class_name('C4VMK')            
        for k in range(len(user_tag)):
            contents = hash_url[k].get_attribute('text')
            pattern = re.compile(r'^#+')
            match = pattern.search(contents)
            if match is not None:
                HashTags.append(contents)
                print("contents : "+ contents)
            else:
                continue
        driver.back()
        randomtime_set() #페이지 되돌아가기 후 일정시간 기다림

    driver.close()

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

#인스타 해당 키워드 접속
start_search = get_search_keyword(keyword)

#크롤링 시작
get_hashtag()        
