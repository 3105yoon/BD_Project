# BD_Project
Instagram Project _빅데이터2조

Instagram Hashtag crawling

#코드 수정시 확인하고 업데이트

### 수정해야될 부분 ###  
1. url 크롤러 자동화  
2. data 크롤러 자동화  
3. csv 저장시 헤더 여러번 써지는 문제  
4. 아스날  
  
  
### 데이터 관련 ###
#### 소요시간 ####  
url 10000개 수집 : 약 1600초  
data 10000개 수집 : 약 5000초  
#### 데이터크기 ####  
약 10000개 : 4MB  


### 변수명 ###  
**userid** : 작성자 id  
**HashTags** : 게시글의 해시태그들(댓글 포함)리스트  
**like** : 게시글의 좋아요 갯수  
**content** : 게시글의 내용(광고글 제거 위해 수집 필요)  
**writedata** : 게시글의 작성 날짜  
**tcnt** : 검색 tag의 총 게시물 수  
**keyword** : 검색하고 싶은 태그명  
**driver, driver2** : 크롬 웹드라이버 load 변수  
**startcount** : 크롤링 횟수 측정을 위한 변수 (시작)  
**endcount** : 크롤링 횟수 측정을 위한 변수 (종료)  
**startTime** : 크롤링 실행 시간 측정(시작시간)  
**endTime** : 크롤링 실행 시간 측정(종료시간)  
**options** : 크롬웹드라이버 사용시 브라우저를 숨기기 위한 옵션 지정 변수  



### 사용하는 selenium 함수 ###

**driver.find_element_by_class_name('g47SY').text** : 총 게시물 수 수집  
**driver.find_element_by_class_name('_9AhH0').click()** : 첫 게시글 클릭  

#### 좋아요 수집 방법 (try 문 사용) ####  
```python
try:    
    like = driver2.find_element_by_class_name('Nm9Fw').find_element_by_tag_name('span').text
    #-> 일반 게시물의 좋아요 수집방법
except NoSuchElementException:
    like = "0"  
    #-> 좋아요 수가 0개인 게시글의 수집방법
    #-> 사용 시 코드 상단에 from selenium.common.exceptions import NoSuchElementException 필요  
except:  
    driver2.find_element_by_class_name('vcOH2').click()
    like = driver2.find_element_by_class_name('vJRqr').find_element_by_tag_name('span').text
    #-> 동영상의 경우 조회수를 클릭해야 좋아요수가 노출되기때문에 클릭후 수집하여야함.
```

**driver.current_url** : 현재 페이지의 url load  
**driver.find_element_by_xpath("//a[@class='HBoOv coreSpriteRightPaginationArrow']").click()** : 다음 게시글 이동 버튼 클릭  

