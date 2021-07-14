import requests 
import bs4
import os
import time
import sys

version = "1.6.0"

def today_article(home_code):
    """
    You can change the date to whenever you want
    rtype: list
    """
    print("[/]正在獲取本日文章清單...")

    # list of "article code"
    today_list = []

    for url_pageNum_of_home in range(1, 6):
        # choose home_code
        url_home = "https://www.sehuatang.org/forum-" + str(home_code) + "-" + str(url_pageNum_of_home) + ".html"        
        
        # request to sehuatang
        response_of_home = requests.get(url_home)

        # bs4 analysis
        bs_home = bs4.BeautifulSoup(response_of_home.text,"html.parser")

        # change the date to extract the data if you want    
        tbody = bs_home.find_all('tbody')

        # extract article code
        for x in tbody:
            date = x.find('span', attrs={'title':today})
            if date == None:
                continue
            id = x.get('id')
            if "normalthread" in str(id):
                today_list.append(id[-6:])      # extract article_Code
            continue     
        url_pageNum_of_home += 1
    print("[*]本日文章清單獲取完成!")
    return today_list   # List of article_Code


def get_title(today_list):
    """
    Read the article_Code and print all title that correspond to the parameter "today"
    type today_list: list (article_Code)
    """
    titleNum = 0
    title_list = []

    print("[/]Title 提取中...")
    for article_Code in today_list:        
        titleNum += 1
        progress_bar(int(titleNum/30*99))
        response_of_article = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
        bs_article = bs4.BeautifulSoup(response_of_article.text,"html.parser")
        title = bs_article.find('span', attrs={'id' : 'thread_subject'}).get_text()
        title_list.append(title)
    progress_bar(100, over = True)

    for t in title_list:
        print("[*]" + t)

    print("[*]Title 已提取完畢" + "一共抓取了" + str(titleNum) + "個 title")
    print('[*]===============================================')
    os.system("pause")


def get_magnet(today_list):
    """
    Read the article_Code and print all magnet that correspond to the parameter "today"
    type today_list: list
    rtype: None
    """            
    magNum = 0
    magnet_List = []

    print("[/]Magnet 提取中...")
    for article_Code in today_list:
        magNum += 1
        progress_bar(int(magNum/30*99))
        response_of_pages = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
        bs_pages = bs4.BeautifulSoup(response_of_pages.text,"html.parser")
        magnet = bs_pages.find('div','blockcode').get_text()
        magnet_List.append(magnet.removesuffix('复制代码'))
    progress_bar(100, over = True)

    for mag in magnet_List:
        print(mag)
    print("[*]Magnet 已提取完畢" + "一共抓取了" + str(magNum) + "個 magnet")
    print('[*]===============================================')
    os.system("pause")


def get_pic_urlList(today_list):
    """
    Read the article_Code and print all URL of picture that correspond to the parameter "today"
    
    type today_list: list
    rtype: None
    """            
    picNum = 0
    pic_link_List = []

    print("[/]Pic_URL.html 產生中...")
    for article_Code in today_list:        
        progress_bar(int(picNum/60*99))
        response_of_pages = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
        soup = bs4.BeautifulSoup(response_of_pages.text,"html.parser")
        img_block = soup.find_all('ignore_js_op')
        for block in img_block[:-1]:
            picNum += 1            
            pic_link = block.find('img').get('file')
            if pic_link != None:
                pic_link_List.append(pic_link)        
    progress_bar(100, over = True)

    print("[*]Pic URL 已提取完畢" + "一共抓取了" + str(picNum) + "個 Pic URL")    
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


def progress_bar(progress_Now, over = False):# 1~101
    if progress_Now > 99:
        if progress_Now == 100:
            print("\r",end="")
            print("[/]Download progress: {}%: ".format(progress_Now),"▋" * (progress_Now // 2),end="")
        else:
            progress_Now = 99
    if over:
        print("")
    else:
        print("\r",end="")
        print("[/]Download progress: {}%: ".format(progress_Now),"▋" * (progress_Now // 2),end="")
        sys.stdout.flush()
        time.sleep(0.05)
    


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
        if extractChoose == 't' or extractChoose == 'T':
            extractChoose_mean = 'title'
        elif extractChoose == 'm' or extractChoose == 'M':
            extractChoose_mean = 'magnet'
        elif extractChoose == 'p' or extractChoose == 'P':
            extractChoose_mean = 'picture'
        else:
            print("Error of extractChoose")

        # Choose Date        
        while not(today_set):
            today_or_not = input("[*]要抓取的是今天的資料嗎?(y/n):")
            if today_or_not == "y" or today_or_not == "Y":
                today = str(time.strftime("%Y-%m-%d", time.localtime()))
                today_set = True
            elif today_or_not == "n" or today_or_not == "N":
                print("[*]請問要抓取的日期是?")
                print("""[*]  !!注意!!  :  "-"號是必要的""")
                today = input("(YYYY-MM-DD):")
                today_set = True

        home_code = URL_List[typeChoose-1]       
        print('[*]===============================================')
        print("[*]以下為 " + str(today) + " " + str(typeList[typeChoose-1]) + " 區的 " + extractChoose_mean + " 提取:")
        
        # make the list of article that published today
        today_list = today_article(home_code)

        # start to extract
        if extractChoose_mean == 'title':
            get_title(today_list)
        elif extractChoose_mean == 'magnet':
            get_magnet(today_list)
        elif extractChoose_mean == 'picture':
            get_pic_urlList(today_list)
        else:
            print("[*]請重新輸入功能...")
            os.system("pause")
            continue
        continue
