from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import csv
import time
import re
from multiprocessing import Process


startTime = time.time() 
# 코드 실행 시간 측정(시작시간)


filename = '연남동결과.csv'
csvfile = open('./datalist/' + filename, 'w')
reader = csv.writer(csvfile)
reader.writerow(['작성자', '작성날짜', '게시글내용', '좋아요갯수', '댓글수', '해시태그'])




options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'cookies'                   : 2, 'images': 2,
                                                    'plugins'                   : 2, 'popups': 2, 'geolocation': 2,
                                                    'notifications'             : 2, 'auto_select_certificate': 2,
                                                    'fullscreen'                : 2,
                                                    'mouselock'                 : 2, 'mixed_script': 2,
                                                    'media_stream'              : 2,
                                                    'media_stream_mic'          : 2, 'media_stream_camera': 2,
                                                    'protocol_handlers'         : 2,
                                                    'ppapi_broker'              : 2, 'automatic_downloads': 2,
                                                    'midi_sysex'                : 2,
                                                    'push_messaging'            : 2, 'ssl_cert_decisions': 2,
                                                    'metro_switch_to_desktop'   : 2,
                                                    'protected_media_identifier': 2, 'app_banner': 2,
                                                    'site_engagement'           : 2,
                                                    'durable_storage'           : 2}}
options.add_experimental_option('prefs', prefs)
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions") 


drvdir = "/project/02_Software/webdrivers/chromedriver" 
# 크롬드라이버 위치

driver1 = webdriver.Chrome(drvdir, chrome_options=options)
driver2 = webdriver.Chrome(drvdir, chrome_options=options)
driver3 = webdriver.Chrome(drvdir, chrome_options=options)
driver4 = webdriver.Chrome(drvdir, chrome_options=options)

time.sleep(5) 

url_list1 = []
url_list2 = []
url_list3 = []
url_list4 = []

def list_slice():
    urlfile = open('./datalist/연남동.csv', 'r')
    url_list_csv = csv.reader(urlfile)
    global url_list1
    global url_list2
    global url_list3
    global url_list4

    url_list_csv = list(url_list_csv)
    length = len(url_list_csv)

    length = int(length/4)

    for line in url_list_csv[0:length]:
        for i in line:
            url_list1.append(i)
    for line in url_list_csv[length:length*2]:
        for i in line:
            url_list2.append(i)
    for line in url_list_csv[length*2:length*3]:
        for i in line:
            url_list3.append(i)
    for line in url_list_csv[length*3:]:
        for i in line:
            url_list4.append(i)
    



def datacrawl1():
    startcount1 = 0

    for url1 in url_list1:
        startcount1 += 1 
        print('driver1 진행상황 :', startcount1, '개')
        driver1.get(url1)
        
        #time.sleep(1)
        driver1.implicitly_wait(1)

        
    
        crwsrc1_1 = driver1.page_source 
        # 접속한 페이지 소스 load
        soup1_1 = BeautifulSoup(crwsrc1_1, 'html.parser') 
        # 파싱
    
        hashtag1 = ""
        for i in soup1_1.select('.C4VMK span a'): 
            #해시태그 찾기
            if i.text.startswith("@"): 
                #사용자 태그 제거
                continue
            else:
                hashtag1 += i.text
        try:
            UserId1 = driver1.find_element_by_class_name('BrX75').text
        except:
            continue
        #작성자 찾기
        #print('작성자 : ',UserId)
        #작성자 출력
    
        ### 작성 날짜 찾기 ###
        try:
            writedate1 = str(soup1_1.find('a', class_='c-Yi7'))
            writedate1 = re.search(r'\d{4}-\d{2}-\d{2}', writedate1)
            writedate1 = writedate1.group(0)
        except:
            continue
        #print(writedate)
    
        #동영상의 경우 조회수를 클릭해야 좋아요수가 나오기 때문에 try문 사용
        try: 
            like1 = driver1.find_element_by_class_name('Nm9Fw').find_element_by_tag_name('span').text
            like1 = int(like1.replace(',', '').strip())
            #print('좋아요 : ',like) 
            #좋아요 출력
        except NoSuchElementException:
            like1 = 0
        #print("좋아요 : ", like)
        except:
            driver1.find_element_by_class_name('vcOH2').click()
            driver1.implicitly_wait(1)
            like1 = driver1.find_element_by_class_name('vJRqr').find_element_by_tag_name('span').text
            like1 = int(like1.replace(',', '').strip())
        #print("좋아요 : ",like) 
        #좋아요 출력 


    ### 게시글 내용 추출 ###
        try:
            content1 = str(soup1_1.find('div', class_='C4VMK').find('span'))
            content1 = re.sub('<a.*?>.*?</a>', '', content1, 0)
            content1 = re.sub('<br/>', '\n', content1, 0)
            content1 = re.sub('<.+?>', '', content1, 0)
        except:
            content1 = ""
    #print(content)
    
    ### 댓글 수 가져오기 ###
    
        while True:
            try:
                driver1.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/div[2]/div[1]/ul/li[2]/button").click()
                element1 = driver1.find_element_by_css_selector("#react-root > section > main > div > div > article > div.eo2As")
                driver1.execute_script("arguments[0].scrollIntoView(true);", element1)
                driver1.implicitly_wait(1)
            except:
                crwsrc1_2 = driver1.page_source 
                # 접속한 페이지 소스 load
                soup2 = BeautifulSoup(crwsrc1_2, 'html.parser') 
                # 파싱
                cocount1 = soup2.findAll("li", class_="gElp9")
                break
        cocount1 = int(len(cocount1)) -1
            #print("댓글 수 : ", cocount)
    
        try:
            reader.writerow([UserId1, writedate1, content1, like1, cocount1, hashtag1])
        except:
            continue
        


def datacrawl2(): 
    startcount2 = 0 
    for url2 in url_list2:
        startcount2 += 1 
        print('driver2 진행상황 :', startcount2, '개')
        driver2.get(url2)
        
        #time.sleep(1)
        driver2.implicitly_wait(1)
        # 다음 게시글 이동 버튼 클릭

        
    
        crwsrc2_1 = driver2.page_source 
        # 접속한 페이지 소스 load
        soup2_1 = BeautifulSoup(crwsrc2_1, 'html.parser') 
        # 파싱
    
        hashtag2 = ""
        for i in soup2_1.select('.C4VMK span a'): 
            #해시태그 찾기
            if i.text.startswith("@"): 
                #사용자 태그 제거
                continue
            else:
                hashtag2 += i.text
        
        try:
            UserId2 = driver2.find_element_by_class_name('BrX75').text
        except:
            continue
        #작성자 찾기
        #print('작성자 : ',UserId)
        #작성자 출력
    
        ### 작성 날짜 찾기 ###
        try:
            writedate2 = str(soup2_1.find('a', class_='c-Yi7'))
            writedate2 = re.search(r'\d{4}-\d{2}-\d{2}', writedate2)
            writedate2 = writedate2.group(0)
        except:
            continue
        #print(writedate)
    
        #동영상의 경우 조회수를 클릭해야 좋아요수가 나오기 때문에 try문 사용
        try: 
            like2 = driver2.find_element_by_class_name('Nm9Fw').find_element_by_tag_name('span').text
            like2 = int(like2.replace(',', '').strip())
            #print('좋아요 : ',like) 
            #좋아요 출력
        except NoSuchElementException:
            like2 = 0
        #print("좋아요 : ", like)
        except:
            driver2.find_element_by_class_name('vcOH2').click()
            driver2.implicitly_wait(1)
            like2 = driver2.find_element_by_class_name('vJRqr').find_element_by_tag_name('span').text
            like2 = int(like2.replace(',', '').strip())
        #print("좋아요 : ",like) 
        #좋아요 출력 


    ### 게시글 내용 추출 ###
        try:
            content2 = str(soup2_1.find('div', class_='C4VMK').find('span'))
            content2 = re.sub('<a.*?>.*?</a>', '', content2, 0)
            content2 = re.sub('<br/>', '\n', content2, 0)
            content2 = re.sub('<.+?>', '', content2, 0)
        except:
            content2 = ""
    #print(content)
    
    ### 댓글 수 가져오기 ###
    
        while True:
            try:
                driver2.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/div[2]/div[1]/ul/li[2]/button").click()
                element2 = driver2.find_element_by_css_selector("#react-root > section > main > div > div > article > div.eo2As")
                driver2.execute_script("arguments[0].scrollIntoView(true);", element2)
                driver2.implicitly_wait(1)
            except:
                crwsrc2_2 = driver2.page_source 
                # 접속한 페이지 소스 load
                soup2_2 = BeautifulSoup(crwsrc2_2, 'html.parser') 
                # 파싱
                cocount2 = soup2_2.findAll("li", class_="gElp9")
                break
        cocount2 = int(len(cocount2)) -1
            #print("댓글 수 : ", cocount)
    
        try:
            reader.writerow([UserId2, writedate2, content2, like2, cocount2, hashtag2])
        except:
            continue
        
        
def datacrawl3(): 
    startcount3 = 0 
    for url3 in url_list3:
        startcount3 += 1 
        print('driver3 진행상황 :', startcount3, '개')
        driver3.get(url3)
        
        #time.sleep(1)
        driver3.implicitly_wait(1)
        # 다음 게시글 이동 버튼 클릭

        
    
        crwsrc3_1 = driver3.page_source 
        # 접속한 페이지 소스 load
        soup3_1 = BeautifulSoup(crwsrc3_1, 'html.parser') 
            # 파싱
    
        hashtag3 = ""
        for i in soup3_1.select('.C4VMK span a'): 
            #해시태그 찾기
            if i.text.startswith("@"): 
                #사용자 태그 제거
                continue
            else:
                hashtag3 += i.text
        try:
            UserId3 = driver3.find_element_by_class_name('BrX75').text
        except:
            continue
        #작성자 찾기
        #print('작성자 : ',UserId)
        #작성자 출력
    
        ### 작성 날짜 찾기 ###
        try:
            writedate3 = str(soup3_1.find('a', class_='c-Yi7'))
            writedate3 = re.search(r'\d{4}-\d{2}-\d{2}', writedate3)
            writedate3 = writedate3.group(0)
        except:
            continue
        #print(writedate)
    
        #동영상의 경우 조회수를 클릭해야 좋아요수가 나오기 때문에 try문 사용
        try: 
            like3 = driver3.find_element_by_class_name('Nm9Fw').find_element_by_tag_name('span').text
            like3 = int(like3.replace(',', '').strip())
            #print('좋아요 : ',like) 
            #좋아요 출력
        except NoSuchElementException:
            like3 = 0
        #print("좋아요 : ", like)
        except:
            driver3.find_element_by_class_name('vcOH2').click()
            driver3.implicitly_wait(1)
            like3 = driver3.find_element_by_class_name('vJRqr').find_element_by_tag_name('span').text
            like3 = int(like3.replace(',', '').strip())
        #print("좋아요 : ",like) 
        #좋아요 출력 


    ### 게시글 내용 추출 ###
        try:
            content3 = str(soup3_1.find('div', class_='C4VMK').find('span'))
            content3 = re.sub('<a.*?>.*?</a>', '', content3, 0)
            content3 = re.sub('<br/>', '\n', content3, 0)
            content3 = re.sub('<.+?>', '', content3, 0)
        except:
            content3 = ""
    #print(content)
    
    ### 댓글 수 가져오기 ###
    
        while True:
            try:
                driver3.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/div[2]/div[1]/ul/li[2]/button").click()
                element3 = driver3.find_element_by_css_selector("#react-root > section > main > div > div > article > div.eo2As")
                driver3.execute_script("arguments[0].scrollIntoView(true);", element3)
                driver3.implicitly_wait(1)
            except:
                crwsrc3_2 = driver3.page_source 
                # 접속한 페이지 소스 load
                soup3_2 = BeautifulSoup(crwsrc3_2, 'html.parser') 
                # 파싱
                cocount3 = soup3_2.findAll("li", class_="gElp9")
                break
        cocount3 = int(len(cocount3)) -1
            #print("댓글 수 : ", cocount)
    
        try:
            reader.writerow([UserId3, writedate3, content3, like3, cocount3, hashtag3])
        except:
            continue


def datacrawl4():   
    startcount4 = 0 
    for url4 in url_list4:
        startcount4 += 1 
        print('driver4 진행상황 :', startcount4, '개')
        driver4.get(url4)
        
        #time.sleep(1)
        driver4.implicitly_wait(1)
        # 다음 게시글 이동 버튼 클릭

        
    
        crwsrc4_1 = driver4.page_source 
        # 접속한 페이지 소스 load
        soup4_1 = BeautifulSoup(crwsrc4_1, 'html.parser') 
        # 파싱
    
        hashtag4 = ""
        for i in soup4_1.select('.C4VMK span a'): 
            #해시태그 찾기
            if i.text.startswith("@"): 
                #사용자 태그 제거
                continue
            else:
                hashtag4 += i.text
                
        try:
            UserId4 = driver4.find_element_by_class_name('BrX75').text
        except:
            continue
        #작성자 찾기
        #print('작성자 : ',UserId)
        #작성자 출력
    
        ### 작성 날짜 찾기 ###
        try:
            writedate4 = str(soup4_1.find('a', class_='c-Yi7'))
            writedate4 = re.search(r'\d{4}-\d{2}-\d{2}', writedate4)
            writedate4 = writedate4.group(0)
        except:
            continue
        #print(writedate)
    
        #동영상의 경우 조회수를 클릭해야 좋아요수가 나오기 때문에 try문 사용
        try: 
            like4 = driver4.find_element_by_class_name('Nm9Fw').find_element_by_tag_name('span').text
            like4 = int(like4.replace(',', '').strip())
            #print('좋아요 : ',like) 
            #좋아요 출력
        except NoSuchElementException:
            like4 = 0
        #print("좋아요 : ", like)
        except:
            driver4.find_element_by_class_name('vcOH2').click()
            driver4.implicitly_wait(1)
            like4 = driver4.find_element_by_class_name('vJRqr').find_element_by_tag_name('span').text
            like4 = int(like4.replace(',', '').strip())
        #print("좋아요 : ",like) 
        #좋아요 출력 


    ### 게시글 내용 추출 ###
        try:
            content4 = str(soup4_1.find('div', class_='C4VMK').find('span'))
            content4 = re.sub('<a.*?>.*?</a>', '', content4, 0)
            content4 = re.sub('<br/>', '\n', content4, 0)
            content4 = re.sub('<.+?>', '', content4, 0)
        except:
            content4 = ""
    #print(content)
    
    ### 댓글 수 가져오기 ###
    
        while True:
            try:
                driver4.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/div[2]/div[1]/ul/li[2]/button").click()
                element4 = driver4.find_element_by_css_selector("#react-root > section > main > div > div > article > div.eo2As")
                driver4.execute_script("arguments[0].scrollIntoView(true);", element4)
                driver4.implicitly_wait(1)
            except:
                crwsrc4_2 = driver4.page_source 
                # 접속한 페이지 소스 load
                soup4_2 = BeautifulSoup(crwsrc4_2, 'html.parser') 
                # 파싱
                cocount4 = soup4_2.findAll("li", class_="gElp9")
                break
        cocount4 = int(len(cocount4)) -1
            #print("댓글 수 : ", cocount)
    
        try:
            reader.writerow([UserId4, writedate4, content4, like4, cocount4, hashtag4])
        except:
            continue
        

list_slice()
p1 = Process(target=datacrawl1)
p2 = Process(target=datacrawl2)
p3 = Process(target=datacrawl3)
p4 = Process(target=datacrawl4)
    
p1.start()
p2.start()
p3.start()
p4.start()

p1.join()
p2.join()
p3.join()
p4.join()

csvfile.close()
driver1.close() 
driver2.close()
driver3.close()
driver4.close()



endTime = time.time() - startTime
print('걸린 시간은 : ',endTime) 



        
        