import os
import time
import sys

# Necessary Modules
import requests 
import bs4
import datetime

version = "1.6.4"

class movie():
    def __init__(self):
        self.type = None
        self.date = None
        self.title = []
        self.magnet = []
        self.picture = []

def today_article(home_code):
    """
    To get the article published today

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

    type today_list: List (article_Code)
    rtype: List
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

    print("[*]Title 已提取完畢" + "一共抓取了" + str(titleNum) + "個 title")
    print('[*]===============================================')    
    return title_list


def get_magnet(today_list):
    """
    Read the article_Code and print all magnet that correspond to the parameter "today"

    type today_list: List
    rtype: List
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
    
    print("[*]Magnet 已提取完畢" + "一共抓取了" + str(magNum) + "個 magnet")
    print('[*]===============================================')
    return magnet_List


def get_pic_urlList(today_list):
    """
    Read the article_Code and print all URL of picture that correspond to the parameter "today"
    
    type today_list: list
    rtype: List
    """            
    picNum = 0
    pic_link_List = []
    
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
    path = make_html(pic_link_List, "Auto_SHT_Pic.html")    
    print('[*]===============================================')
    return path


def make_html(input_list, fileName):
    '''
    Read the url in the input_list, and make the HTML file

    type input_list: list
    '''
    path = "./" + fileName

    print(f"[/]{fileName} 產生中...")
    f = open(path, 'w')
    f.write("<!doctype html><html><head><title>Auto SHT !</title></head><body>")

    for url in input_list:
        if url == "None":
            continue
        f.write("<img src = " + url + """ width="1200" height="807">""")

    f.write("</body></html>")
    f.close()
    path = f"{os.getcwd()}\{path[2:]}"
    print(f"[*]{fileName} 產生成功! -> 檔案路徑: {path}")
    return path


def progress_bar(progress_Now, over = False):# 1~101
    '''
    Make progress bar by 0% ~ 100%

    type progress_Now: int
    '''
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


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def getYesterday(how_many_day_pre): 
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=how_many_day_pre) 
    yesterday=today-oneday  
    return yesterday


if __name__ == '__main__':
    # Param
    typeList = ["無碼", "有碼", "國產", "歐美", "中文"]
    type_List2 = [["WM"], ["YM"], ["GC"], ["OM"], ["JW"]]
    today_set = False
    today_list = []
    typeChoose_last = 0

    # Main Loop
    while True:
        clearConsole()
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
        print("[*]")
        print("[*]    ↓ Follow the updates and Guides Here ↓")
        print("[*]https://github.com/dec880126/Auto_sht/releases")
        print('[*]===============================================')
        print("[*]                 1. 無碼")
        print("[*]                 2. 有碼")
        print("[*]                 3. 國產")
        print("[*]                 4. 歐美")
        print("[*]                 5. 中文")
        print("[*]                 6. 結束程式")
        print("[*]                 7. 修改日期")
        print('[*]===============================================')        
        typeChoose = int(input("[?]請選擇功能(1~6):"))        
        # Exception
        if typeChoose < 1 or typeChoose > 7:
            print('[*]===============================================')
            print("[?]請重新輸入功能選單中之數字(1~6)...")
            os.system("pause")
            continue

        # Finish
        if typeChoose == 6:
            break        

        # Change date
        if typeChoose == 7:
            print("[*]請問日期要更改為?")
            print(f"[*](昨天: -1, 前天: -2...)")
            print("""[*]  !!注意!!  :  "-"號是必要的""")
            today = input("[?](YYYY-MM-DD):")
            if int(today) < 0 and int(today) > -4:
                today = getYesterday(abs(int(today)))
            continue        
        
        extractChoose = input("[?]選擇要抓取的種類(標題:t, 磁力:m, 圖片:p):")        
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
            today_or_not = input("[?]要抓取的是今天的資料嗎? (y/n):")
            if today_or_not == "y" or today_or_not == "Y":
                today = str(time.strftime("%Y-%m-%d", time.localtime()))
                today_set = True
            elif today_or_not == "n" or today_or_not == "N":
                print("[?]請問要抓取的日期是?")
                print(f"[*](昨天: -1, 前天: -2...)")
                print("""[*]  !!注意!!  :  "-"號是必要的""")
                today = input("(YYYY-MM-DD):")
                if int(today) < 0 and int(today) > -4:
                    today = getYesterday(abs(int(today)))
                today_set = True

        home_code = URL_List[typeChoose-1]       
        print('[*]===============================================')
        print("[*]以下為 " + str(today) + " " + str(typeList[typeChoose-1]) + " 區的 " + extractChoose_mean + " 提取:")
        
        # Check if today_List exist
        # make the list of article that published today
        if len(today_list) == 0 or typeChoose != typeChoose_last:
            print("[*]本日文章清單不存在!")
            today_list = today_article(home_code)
        else:
            print("[*]本日文章清單已存在!")
        
        # start to extract
        """
        CONTENT OF type_List2
        INDEX = typeChoose-1

        WM: 無碼
        YM: 有碼
        GC: 國產
        OM: 歐美
        JW: 中文
        """
        if extractChoose_mean == 'title':
            try:
                for text in type_List2[typeChoose-1].title:
                    print("[*]" + text)
            except:
                type_List2[typeChoose-1] = movie()
                type_List2[typeChoose-1].title = get_title(today_list)
                for text in type_List2[typeChoose-1].title:
                    print("[*]" + text)
        elif extractChoose_mean == 'magnet':
            try:
                for text in type_List2[typeChoose-1].magnet:
                    print("[*]" + text)
            except:
                type_List2[typeChoose-1] = movie()
                type_List2[typeChoose-1].magnet = get_magnet(today_list)
                for text in type_List2[typeChoose-1].magnet:
                    print("[*]" + text)            
        elif extractChoose_mean == 'picture':
            try:
                print(f"[*]檔案路徑: {type_List2[typeChoose-1].picture}")                
            except:
                type_List2[typeChoose-1] = movie()
                type_List2[typeChoose-1].picture = get_pic_urlList(today_list)
        else:
            print("[*]請重新輸入功能...")
            os.system("pause")
            continue

        # Record latest typeChoose
        typeChoose_last = typeChoose

        os.system("pause")
