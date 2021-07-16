import os
import time

from getData import get_title, get_magnet, get_pic_urlList, get_today_article
from tool_function import clearConsole, getYesterday, choose_type

version = "3.0.0"

class Fourm():
    def __init__(self):
        self.title = []
        self.magnet = []
        self.title_magnet = {}
        self.picture_path = "" # path of HTML files
        self.fileName = "請先運行圖片抓取模式"


if __name__ == '__main__':
    # Param
    fourmList_Chinese = ["無碼", "有碼", "國產", "歐美", "中文"]
    fourmList_Eng = [["WM"], ["YM"], ["GC"], ["OM"], ["JW"]]
    fourmList = []
    URL_List = [36, 37, 2, 38, 103]
    today_list = [[], [], [], [], []]
    fourmChoose_last = 0

    # Default Setting
    today = str(time.strftime("%Y-%m-%d", time.localtime()))

    # Publish class
    for fourm in fourmList_Eng:
        fourmList.append(Fourm())

    # Main Loop
    while True:
        clearConsole()
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
        print("[*]                 1. 選擇功能")
        print("[*]                 2. 修改日期")
        print("[*]                 3. 結束程式")
        print('[*]===============================================')        
        typeChoose = int(input("[?]請選擇功能(1~3):"))   

        # To ensure typeChoose in the list
        if typeChoose < 1 or typeChoose > 3:
            print('[*]===============================================')
            print("[?]請重新輸入功能選單中之數字(1~3)...")
            os.system("pause")
            continue

        # Finish
        if typeChoose == 3:
            break        

        # Change date
        if typeChoose == 2:
            print("[*]請問日期要更改為?")
            print(f"[*](昨天: -1, 前天: -2...)")
            print("""[*]  !!注意!!  :  "-"號是必要的""")
            today = input("[?](YYYY-MM-DD):")
            if int(today) < 0 and int(today) > -4:
                today = getYesterday(abs(int(today)))
            continue        
        
        while True:     
            extractChoose = input("[?]選擇要抓取的種類(標題:t, 磁力:m, 圖片:p, 選擇:c):")
            if extractChoose == 't' or extractChoose == 'T':
                extractChoose_mean = 'title'
                break
            elif extractChoose == 'm' or extractChoose == 'M':
                extractChoose_mean = 'magnet'
                break
            elif extractChoose == 'p' or extractChoose == 'P':
                extractChoose_mean = 'picture'
                break
            elif extractChoose == 'c' or extractChoose == 'C':
                extractChoose_mean = 'choose'
                break
            else:
                print(f"請輸入正確的字符")

        # Fourm Choose
        fourmChoose = choose_type()

        home_code = URL_List[fourmChoose-1]       
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
            if len(workSpace.title) == 0:
                workSpace.title =  get_title(today_list[fourmChoose-1])
            if len(workSpace.magnet) == 0:
                workSpace.magnet = get_magnet(today_list[fourmChoose-1])
            if len(workSpace.title_magnet) == 0:
                workSpace.title_magnet = dict(zip(workSpace.title, workSpace.magnet))
            if workSpace.picture_path == "":
                workSpace.picture_path, workSpace.fileName = get_pic_urlList(today_list[fourmChoose-1])

            print(f"選擇時搭配 {workSpace.fileName} 使用 -> 檔案路徑: {workSpace.picture_path}")
            print('[*]===============================================')

            # Start working for choose movie
            for title in workSpace.title_magnet:
                if_save = input(f"{title}: ")
                if if_save == "":
                    workSpace.title_magnet[title] = "None"
            
            print('[*]===============================================')
            print(f"以下為 magnet 輸出:")
            for title in workSpace.title_magnet:                
                if workSpace.title_magnet[title] != "None":
                    print(workSpace.title_magnet[title])
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

            print(f"[*]{workSpace.fileName} 產生成功! -> 檔案路徑: {workSpace.picture_path}")
            print('[*]===============================================')
        else:
            print("[*]請重新輸入功能...")
        
        os.system("pause")
    
    # Remove the HTML files when program finished
    os.remove(workSpace.picture_path)
