import requests 
import bs4
import os

def main(url):    
    # 發送get 請求 到 sht
    response_of_home = requests.get(url)

    # 把HTML 丟入 bs4模組分析
    bs_home = bs4.BeautifulSoup(response_of_home.text,"html.parser")

    '''
    <div class="title"> 
        <a href="/bbs/Gossiping/M.1589705973.A.912.html">
        [問卦] 為什麼八卦的民意在社會上都體現不出來呢
        </a>	
    </div>
    '''
    # 2-2 查找所有html 元素 過濾出 標籤名稱為 'div' 同時class為 title 
    titles = bs_home.find_all('a','s xst')

    # 2-3 萃取文字出來。
    # 因為我們有多個Tags存放在 List titles中。
    # 所以需要使用for 迴圈將逐筆將List 
    href_List = []
    magnet_List = []

    for t in titles[7:]:
        href_List.append(t.get("href"))
    # print(href_List)

    url_of_pages = href_List[0]
    pageNum = 0
    for url_of_pages in href_List:
        response_of_pages = requests.get("https://www.sehuatang.org/" + url_of_pages)
        bs_pages = bs4.BeautifulSoup(response_of_pages.text,"html.parser")
        magnet = bs_pages.find('div','blockcode').get_text()
        # magnet_List.append(magnet.removesuffix('复制代码'))
        print(magnet.removesuffix('复制代码'))
    print("Magnet 已提取完畢")
    os.system("pause")

if __name__ == '__main__':
    while True:        
        URL_List = ["https://www.sehuatang.org/forum-36-1.html", "https://www.sehuatang.org/forum-37-1.html", "https://www.sehuatang.org/forum-2-1.html", "https://www.sehuatang.org/forum-38-1.html", "https://www.sehuatang.org/forum-103-1.html"]
        '''
        URL_List
        0. 無碼: https://www.sehuatang.org/forum-36-1.html
        1. 有碼: https://www.sehuatang.org/forum-37-1.html
        2. 國產: https://www.sehuatang.org/forum-2-1.html
        3. 歐美: https://www.sehuatang.org/forum-38-1.html
        4. 中文: https://www.sehuatang.org/forum-103-1.html
        '''
        print('[*]================== Auto_sht ===================')
        print("[*]                 1. 無碼")
        print("[*]                 2. 有碼")
        print("[*]                 3. 國產")
        print("[*]                 4. 歐美")
        print("[*]                 5. 中文")
        print("[*]                 6. 結束程式")
        print('[*]===============================================')
        typeChoose = int(input("選擇要抓取 Magnet 的版(1~5):"))
        if typeChoose == 6:
            break
        url_home = URL_List[typeChoose-1]
        main(url_home)