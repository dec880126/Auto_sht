import os
import time
import webbrowser

from getData import get_title, get_magnet, get_pic_urlList, get_today_article, get_ALL
from tool_function import clearConsole, getYesterday, choose_type

version = "3.4.0"

class Fourm():
    def __init__(self):
        self.type = ""
        self.title = []
        self.magnet = []
        self.title_magnet = {}
        self.picture_path = "" # path of HTML files
        self.fileName = "請先運行圖片抓取模式"
        self.searchIndex = -1


if __name__ == '__main__':
    # Param
    fourmList_Chinese = ["無碼", "有碼", "國產", "歐美", "中文"]
    fourmList_Eng = [["WM"], ["YM"], ["GC"], ["OM"], ["JW"]]
    fourmList = []
    URL_List = [36, 37, 2, 38, 103]
    '''
    URL_List
    0. 無碼: https://www.sehuatang.org/forum-36-1.html
    1. 有碼: https://www.sehuatang.org/forum-37-1.html
    2. 國產: https://www.sehuatang.org/forum-2-1.html
    3. 歐美: https://www.sehuatang.org/forum-38-1.html
    4. 中文: https://www.sehuatang.org/forum-103-1.html
    '''
    today_list = [[], [], [], [], []]
    fourmChoose_last = 0

    # Default Setting
    today = str(time.strftime("%Y-%m-%d", time.localtime()))

    # Publish class
    fourmList_index = 0
    for fourm in fourmList_Eng:
        fourmList.append(Fourm())
        fourmList[fourmList_index].type = fourmList_Chinese[fourmList_index]
        fourmList_index += 1

    # Main Loop
    while True:
        clearConsole()
        
        print('[*]================== Auto_sht ===================')
        print("[*]                    v" + version)
        print("[*]")
        print("[*]    ↓ Follow the updates and Guides Here ↓")
        print("[*]https://github.com/dec880126/Auto_sht/releases")
        print('[*]===============================================')
        print("[*]                 1. 開始抓取")
        print("[*]                 2. 修改日期")
        print("[*]                 3. 資料查詢")
        print("[*]                 4. 結束程式")
        print('[*]===============================================')        
        typeChoose = int(input("[?]請選擇功能(1~4):"))

        # Finish
        if typeChoose == 4:
            break 
        
        # To ensure typeChoose in the list
        if typeChoose < 1 or typeChoose > 4:
            print('[*]===============================================')
            print("[?]請重新輸入功能選單中之數字(1~4)...")
            os.system("pause")
            continue

        # Change date
        if typeChoose == 2:
            print('[*]===============================================')
            print(f"[*](昨天: -1, 前天: -2...)")
            print('[*]===============================================')
            today = input("[?]請問日期要更改為?:")
            if int(today) < 0 and int(today) > -4:
                today = getYesterday(abs(int(today)))
            continue
        
        # Data Search
        """
        fourmList = [WM, YM, GC, OM, JW] <- every element is object Fourm
        """
        temp = 0
        if typeChoose == 3:   
            print('[*]===============================================')         
            try:                
                for fourm in fourmList:
                    if fourm.title_magnet:
                        temp += 1
                        print(f"[*]{temp}. {fourm.type}")
                        fourm.searchIndex = temp
                print('[*]===============================================')
                fourm_search = choose_type()

                if len(fourmList[fourm_search-1].title_magnet) == 0:
                    raise BaseException()
                for title, magnet in fourmList[fourm_search-1].title_magnet.items():
                    if magnet != "None":
                        print(f'[*] {title} : {magnet}')                    
            except:
                print(f"[*]資料庫中目前無資料")
                print('[*]===============================================')
            os.system("pause")
            continue
        
        if temp == 0:
            fourmChoose = choose_type()
        
        # while True:     
        #     extractChoose = input("[?]選擇要抓取的種類(標題:t, 磁力:m, 圖片:p, 挑選:c):")
        #     if extractChoose == 't' or extractChoose == 'T':
        #         extractChoose_mean = 'title'
        #         break
        #     elif extractChoose == 'm' or extractChoose == 'M':
        #         extractChoose_mean = 'magnet'
        #         break
        #     elif extractChoose == 'p' or extractChoose == 'P':
        #         extractChoose_mean = 'picture'
        #         break
        #     elif extractChoose == 'c' or extractChoose == 'C':
        #         extractChoose_mean = 'choose'
        #         break
        #     else:
        #         print(f"請輸入正確的字符")

        # Fourm Choose        

        home_code = URL_List[fourmChoose-1]
        extractChoose_mean = 'choose'
        print('[*]===============================================')
        print("[*]以下為 " + str(today) + " " + str(fourmList_Chinese[fourmChoose-1]) + " 區的 " + extractChoose_mean + " :")
        
        # Check if today_List for each fourm exist or not
        # make the list of article that published today
        if len(today_list[fourmChoose-1]) == 0:
            print("[*]本日文章清單不存在!")
            today_list[fourmChoose-1] = get_today_article(home_code, today)
        else:
            print("[*]本日文章清單已存在!")
        
        workSpace = fourmList[fourmChoose-1]
        # start to extract
        if extractChoose_mean == 'choose':
            # Ensure Data exist
            if len(workSpace.title_magnet) == 0:
                workSpace.title_magnet, workSpace.picture_path, workSpace.fileName = get_ALL(today_list[fourmChoose-1])
       
            print('[*]===============================================')

            # Open HTML files with default browser
            webbrowser.open_new_tab(workSpace.picture_path)

            temp = workSpace.title_magnet.copy()

            # Start working for choose movie
            print("[*]以下為挑選作業的規則說明:")
            print("[*]如果要保留請隨意輸入(不要空白即可)，並按下 Enter 送出")
            print("[*]如果要捨棄，直接按下 Enter 送出即可捨棄")
            print('[*]===============================================')
            Num = 0
            for title in workSpace.title_magnet:
                Num += 1
                if_save = input(f"[?]{Num}. {title}:   ")
                if if_save == "":
                    workSpace.title_magnet[title] = "None"
                elif if_save == "exit":
                    break
            else:
                temp = workSpace.title_magnet
            if if_save == "exit":
                workSpace.title_magnet = temp
                continue
            workSpace.title_magnet = temp
            print('[*]===============================================')
            print(f"[*]以下為 magnet 輸出:")
            for title in workSpace.title_magnet:                
                if workSpace.title_magnet[title] != "None":
                    print(workSpace.title_magnet[title])
            print('[*]===============================================')
        elif extractChoose_mean == 'title':
            if len(workSpace.title) == 0:
                for title in get_title(today_list[fourmChoose-1]):
                    workSpace.title_magnet[title] = ""

            for text in workSpace.title:
                print("[*]" + text)                
        elif extractChoose_mean == 'magnet':
            if len(workSpace.magnet) == 0:
                workSpace.magnet = get_magnet(today_list[fourmChoose-1])
                for title, magnet in zip(workSpace.title, workSpace.magnet):
                    workSpace.title_magnet[title] = magnet
            
            for title in workSpace.title_magnet:
                print("[*]" + workSpace.title_magnet[title])            
        elif extractChoose_mean == 'picture':
            if workSpace.picture_path == "":
                workSpace.picture_path, workSpace.fileName = get_pic_urlList(today_list[fourmChoose-1])
            
            print('[*]===============================================')
        else:
            print("[*]請重新輸入功能...")
        
        os.system("pause")
    
    try:
        # Remove the HTML files when program finished
        os.remove(workSpace.picture_path)
    except:
        pass
    clearConsole()
