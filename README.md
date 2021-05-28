# PWS_PageCrawler
臉書粉專爬蟲

=========================================. 

請先下載好Chrome driver並解壓縮
網址：https://sites.google.com/a/chromium.org/chromedriver/downloads
* mac可能遇到安全性設定問題，解決方式：
* 在終端機到driver所在資料夾執行以下指令： xattr -d com.apple.quarantine chromedriver.  

=========================================. 

要修改的路徑都在PageCrawler.py中有註解.  
請先按照以下步驟修改路徑或網址:.  

1.（步驟1）修改要爬的粉專網址.  
2.（步驟2）修改driver_location為driver位置.  
3.（步驟3）輸入臉書帳密  
4.（步驟6）修改要讓頁面滾動的次數，以蔡英文臉書為例，一年的貼文量大約要滾動220~250次，可以先實驗個幾次試試.  
5.（步驟7）修改輸出的檔案路徑，記得路徑最後檔名一定要改！檔名一定要改！檔名一定要改！不然先前爬資料會被蓋掉....  
  
=========================================. 

  
輸出檔案範例如Tsaiingwen_test.csv 與 Tsaiingwen_test.xls

2021.05.28 修正：  
20210528PostInformation函式新增Post連結、改Content抓取方式、留言分享數單位
