import requests 
import bs4
import os
import time

version = "1.1.5"
# update note
'''
ver 1.0 First varsion
ver 1.1 新增挑出當日更新文章功能
'''

def today_article(soup):
    """
    rtype: list
    """
    today = str(time.strftime("%Y-%m-%d", time.localtime()))
    tbody = soup.find_all('tbody')
    today_list = [] # 存放文章代碼之 list

    # 提取文章代碼
    for x in tbody:
        date = x.find('span', attrs={'title':today})
        if date != None:
            if date.get('title') != today:
                continue
            id = x.get('id')
            if "normalthread" in str(id):
                today_list.append(id[-6:])
            continue          
    return today_list

def main(url):
    """
    type url: str
    rtype: None
    """    
    # 發送get 請求 到 sht
    response_of_home = requests.get(url)

    # 把HTML 丟入 bs4模組分析
    bs_home = bs4.BeautifulSoup(response_of_home.text,"html.parser")
    
    # 建立今日的新文章清單
    today_list = today_article(bs_home)
    pageNum = 0

    for url_of_pages in today_list:
        pageNum += 1
        response_of_pages = requests.get("https://www.sehuatang.org/thread-" + url_of_pages + "-1-1.html")
        bs_pages = bs4.BeautifulSoup(response_of_pages.text,"html.parser")
        magnet = bs_pages.find('div','blockcode').get_text()
        # magnet_List.append(magnet.removesuffix('复制代码'))
        print(str(pageNum) + ". " + magnet.removesuffix('复制代码'))
    print("Magnet 已提取完畢" + "一共抓取了" + str(pageNum) + "個 magnet")
    print('[*]===============================================')
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
        print("[*]                    v" + version)
        print('[*]===============================================')
        print("[*]                 1. 無碼")
        print("[*]                 2. 有碼")
        print("[*]                 3. 國產")
        print("[*]                 4. 歐美")
        print("[*]                 5. 中文")
        print("[*]                 6. 結束程式")
        print('[*]===============================================')
        typeList = ["無碼", "有碼", "國產", "歐美", "中文"]
        typeChoose = int(input("選擇要抓取 Magnet 的版(1~6):"))

        # 處理輸入之 Exception
        if typeChoose < 1 or typeChoose > 6:
            print('[*]===============================================')
            print("請重新輸入功能選單中之數字(1~6)...")
            os.system("pause")
            continue

        # 結束程式
        if typeChoose == 6:
            break

        url_home = URL_List[typeChoose-1]
        print('[*]===============================================')
        print("以下為 " + str(time.strftime("%Y-%m-%d", time.localtime())) + " " + str(typeList[typeChoose-1]) + " 區的 magnet 提取:")
        
        # 開始抓取
        main(url_home)
