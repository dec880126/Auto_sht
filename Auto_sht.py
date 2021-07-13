import requests 
import bs4
import os
import time

version = "1.3.1"

class movie():
    def __init__(self) -> None:
        pass
    

def today_article(soup):
    """
    You can change the date to whenever you want
    rtype: list
    """
    # change the date to extract the data if you want
    # today = yyyy-mm-dd
    today = str(time.strftime("%Y-%m-%d", time.localtime()))
    tbody = soup.find_all('tbody')
    today_list = [] # list of "article code"

    # extract article code
    for x in tbody:
        date = x.find('span', attrs={'title':today})
        if date != None:
            if date.get('title') != today:
                continue
            id = x.get('id')
            if "normalthread" in str(id):
                today_list.append(id[-6:])      # extract article_Code
            continue          
    return today_list   # List of article_Code


def get_title(today_list):
    """
    Read the article_Code and print all title that correspond to the parameter "today"
    type today_list: list (article_Code)
    """
    titleNum = 0
    for article_Code in today_list:
        titleNum += 1
        response_of_article = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
        bs_article = bs4.BeautifulSoup(response_of_article.text,"html.parser")
        title = bs_article.find('span', attrs={'id' : 'thread_subject'}).get_text()
        print("[*]" + title)
    print("[*]Title 已提取完畢" + "一共抓取了" + str(titleNum) + "個 title")
    print('[*]===============================================')
    os.system("pause")


def get_magnet(today_list):
    """
    Read the article_Code and print all magnet that correspond to the parameter "today"
    type today_list: list
    rtype: None
    """            
    pageNum = 0

    for article_Code in today_list:
        pageNum += 1
        response_of_pages = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
        bs_pages = bs4.BeautifulSoup(response_of_pages.text,"html.parser")
        magnet = bs_pages.find('div','blockcode').get_text()
        # magnet_List.append(magnet.removesuffix('复制代码'))
        print("[*]" + str(pageNum) + ". " + magnet.removesuffix('复制代码'))
    print("[*]Magnet 已提取完畢" + "一共抓取了" + str(pageNum) + "個 magnet")
    print('[*]===============================================')
    os.system("pause")


def get_pic_urlList(today_list):
    """
    Read the article_Code and print all URL of picture that correspond to the parameter "today"
    type today_list: list
    rtype: None
    """            
    pageNum = 0

    for article_Code in today_list:
        pageNum += 1
        response_of_pages = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
        soup = bs4.BeautifulSoup(response_of_pages.text,"html.parser")
        img_block = soup.find_all('ignore_js_op')
        for block in img_block[:-1]:
            pic_link = block.find('img').get('file')
            print(pic_link)
    print("[*]Pic URL 已提取完畢" + "一共抓取了" + str(pageNum) + "個 Pic URL")
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
        typeChoose = int(input("請選擇功能(1~6):"))
        # Exception
        if typeChoose < 1 or typeChoose > 6:
            print('[*]===============================================')
            print("[*]請重新輸入功能選單中之數字(1~6)...")
            os.system("pause")
            continue

        # Finish
        if typeChoose == 6:
            break        

        extractChoose = input("選擇要抓取的種類(標題:t, 磁力:m, 圖片:p):")        
        if extractChoose == 't':
            extractChoose_mean = 'title'
        elif extractChoose == 'm':
            extractChoose_mean = 'magnet'
        elif extractChoose == 'p':
            extractChoose_mean = 'picture'
        else:
            print("Error of extractChoose")        

        # choose url_home
        url_home = URL_List[typeChoose-1]
        print('[*]===============================================')
        print("[*]以下為 " + str(time.strftime("%Y-%m-%d", time.localtime())) + " " + str(typeList[typeChoose-1]) + " 區的 " + extractChoose_mean + " 提取:")
        
        # request to sehuatang
        response_of_home = requests.get(url_home)

        # bs4 analysis
        bs_home = bs4.BeautifulSoup(response_of_home.text,"html.parser")
        
        # make the list of article that published today
        today_list = today_article(bs_home)

        # start to extract
        if extractChoose == 't':
            get_title(today_list)
        elif extractChoose == 'm':
            get_magnet(today_list)
        elif extractChoose == 'p':
            get_pic_urlList(today_list)
        else:
            print("[*]請重新輸入功能...")
            os.system("pause")
            continue
        continue
