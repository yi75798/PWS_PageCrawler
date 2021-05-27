#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#### Name:PageCrawler
#### Author:Liang-Yi, Hsu
#### Date:2021/05/27

### 0.載入套件
from selenium import webdriver
import time
import datetime
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import  re

### 1.設定要爬的粉專網址
url = "https://www.facebook.com/dpptw" # 粉專網址
ID = url.split(".com/")[1]

### 2.設定瀏覽器driver
# driver設定
my_options = Options()
my_options.add_argument("--headless") # 不顯示實體瀏覽器（想看瀏覽器自己動可以不設這項ＸＤ）

# location為存放driver的路徑
driver_location = u"/Volumes/GoogleDrive/我的雲端硬碟/台大政研/2021程式設計/final_project/chromedriver" # 路徑有中文所以前面加u
driver = webdriver.Chrome(driver_location, options=my_options)

### 3.登入臉書，避免跳出一些視窗且降低ip被ban機會
start_time = time.time() # 計時用
# 輸入臉書帳密
account = 'xxx@xxxx' # 帳號
password = 'xxxxxxxx' # 密碼

# 登入函式
def login(account, password, driver):
    driver.get('https://www.facebook.com/')
    input_1 = driver.find_element_by_css_selector('#email')
    input_2 = driver.find_element_by_css_selector("input[type='password']")

    input_1.send_keys(account)
    input_2.send_keys(password)
    driver.find_element_by_css_selector("button[name='login']").click()
    time.sleep(1)
    
    driver.get(url)
    time.sleep(1)

# 登入
login(account, password, driver)

### 4.抓取貼文連結函式
# 因為是瀑布式網頁，要讓頁面往下滾動才會顯示貼文
def FindLinks(n:int) -> list:
    """
    n為要讓頁面往下滾幾次，自行斟酌一年的貼文大該要幾次...
    輸出為list形式，存放所有貼文連結
    """
    Links = []
    for i in range(n):
        time.sleep(2)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3) # 停留時間視網速而定，不夠久會抓不到東西（頁面來不及顯示）
    time.sleep(1)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    posts = soup.find_all('div', {'class':'du4w35lb l9j0dhe7'})
    for i in posts:
        Links.append(i.find('a',{'class':'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl m9osqain gpro0wi8 knj5qynh'}).attrs['href'].split('?',2)[0])
    return Links

### 5.抓取Ｐost內容、互動數、留言數、分享數函式
def PostInformation(soup) -> pd.DataFrame:
    """
    soup:parser完的網頁（就是個別貼文）
    輸出為DataFrame形式
    """
    # Post時間
    try:
        Time = soup.find("b", {"class":"b6zbclly myohyog2 l9j0dhe7 aenfhxwr l94mrbxd ihxqhq3m nc684nl6 t5a262vz sdhka5h4"}).text.strip("=")
    except:
        Time = ""
    # Post內容
    try:
        Content = soup.find("div", {"class":"ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a"}).text
    except:
        Content = ""
    # 互動數（我抓不到個別心情數QQ）
    try:
        Reaction = soup.find("span", {"class":"pcp91wgn"}).text
        if Reaction[-1] == "萬":
            Reaction = int(re.sub(r"\D", "", Reaction)) * 1000 # 用re留下數字部分並還原單位
        else:
            Reaction = int(re.sub(r"\D", "", Reaction))
    except:
        Reaction = ""
    ## 留言分享數
    Comment_Share = soup.find_all("span", {"class":"d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v knj5qynh m9osqain"})
    # 留言數
    try:
        Comment = Comment_Share[0].text
        Comment = int(re.sub(r"\D","", Comment))
    except:
        Comment = ""
    # 分享數
    try:
        Share = Comment_Share[1].text
        Share = int(re.sub(r"\D","", Share))
    except:
        Share = ""
    # 輸出
    return pd.DataFrame(
        data = [{'ID':ID,
                 'Time':Time,
                 'Content':Content,
                 'Reaction':Reaction,
                 'Comment':Comment,
                 'Share':Share}],
        columns = ['ID', 'Time', 'Content', 'Reaction', 'Comment', 'Share'])

### 6.正式開始爬蟲
## 先抓取所有貼文連結
# FindLinks輸入要滾動頁面的次數
Links = FindLinks(2)
print("Find Links Finished")

## 抓取Post資訊
# 先設一個空的DataFrame以存放輸出的東西
Post_Output = pd.DataFrame()

# 點開每一個Post連結，用PostInformation函式抓資料
for i in Links:
    print('Dealing with: ' + i)
    try:
        driver.get(i)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        Post_Output = Post_Output.append(PostInformation(soup),ignore_index=True)
        Post_Output["Link"] = i
    except:
        print('Load Failed: ' + i) # 出現任何問題就顯示Failed

driver.close() # 關閉瀏覽器

end_time = time.time()
print("耗費時間:"+ str(datetime.timedelta(seconds=end_time - start_time)))

### 7.輸出為csv及xls檔
# 路徑最後檔案名記得改!!!!!!
Post_Output.to_csv(path_or_buf=u"/Volumes/GoogleDrive/我的雲端硬碟/台大政研/2021程式設計/final_project/dpp.csv", index=False, encoding="utf-8")
Post_Output.to_excel(u"/Volumes/GoogleDrive/我的雲端硬碟/台大政研/2021程式設計/final_project/dpp.xls", index=False, encoding="utf-8")





