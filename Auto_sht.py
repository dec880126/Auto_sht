import requests 
import bs4
import os
import time

version = "1.5.0"

def today_article(soup):
    """
    You can change the date to whenever you want

    rtype: list
    """
    # change the date to extract the data if you want    
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
    pic_link_List = []
    print("[*]Pic_URL.html 產生中...")
    for article_Code in today_list:
        pageNum += 1
        response_of_pages = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
        soup = bs4.BeautifulSoup(response_of_pages.text,"html.parser")
        img_block = soup.find_all('ignore_js_op')
        for block in img_block[:-1]:
            pic_link = block.find('img').get('file')
            print(pic_link)
            pic_link_List.append(pic_link)
    print("[*]Pic URL 已提取完畢" + "一共抓取了" + str(pageNum) + "個 Pic URL")    
    make_html(pic_link_List, "Pic_URL.html")
    print("[*]Pic_URL.html 產生成功!")
    print('[*]===============================================')
    os.system("pause")

def make_html(input_list, fileName):
    '''
    Read the url in the input_list, and make the HTML file
    type input_list: list
    '''
    path = "./" + fileName
    f = open(path, 'w')
    f.write("<!doctype html><html>    <head>        <title>Auto SHT ! </title>    </head>    <body>")

    for url in input_list:
        if url != "None":
            f.write("<img src = " + url + """ width="1200" height="807">""")

    f.write("    </body></html>")
    f.close()
    

if __name__ == '__main__':
    today_set = False
    while True:        
        URL_List = [36, 37, 2, 38, 103]
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
        print("[*]                 7. 修改日期")
        print('[*]===============================================')
        typeList = ["無碼", "有碼", "國產", "歐美", "中文"]
        typeChoose = int(input("請選擇功能(1~6):"))
        # Exception
        if typeChoose < 1 or typeChoose > 7:
            print('[*]===============================================')
            print("[*]請重新輸入功能選單中之數字(1~6)...")
            os.system("pause")
            continue

        # Finish
        if typeChoose == 6:
            break        

        # Change date
        if typeChoose == 7:
            print("[*]請問日期要更改為?")
            print("""[*]  !!注意!!  :  "-"號是必要的""")
            today = input("(YYYY-MM-DD):")
            continue        
        
        extractChoose = input("選擇要抓取的種類(標題:t, 磁力:m, 圖片:p):")        
        if extractChoose == 't':
            extractChoose_mean = 'title'
        elif extractChoose == 'm':
            extractChoose_mean = 'magnet'
        elif extractChoose == 'p':
            extractChoose_mean = 'picture'
        else:
            print("Error of extractChoose")

        # Choose Date        
        while not(today_set):
            today_or_not = input("[*]要抓取的是今天的資料嗎?(y/n):")
            if today_or_not == "y":
                today = str(time.strftime("%Y-%m-%d", time.localtime()))
                today_set = True
            elif today_or_not == "n":
                print("[*]請問要抓取的日期是?")
                print("""[*]  !!注意!!  :  "-"號是必要的""")
                today = input("(YYYY-MM-DD):")
                today_set = True


        # choose url_home
        url_pageNum_of_home = 1
        url_home = "https://www.sehuatang.org/forum-" + str(URL_List[typeChoose-1]) + "-" + str(url_pageNum_of_home) + ".html"        
        print('[*]===============================================')
        print("[*]以下為 " + str(today) + " " + str(typeList[typeChoose-1]) + " 區的 " + extractChoose_mean + " 提取:")
        
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
