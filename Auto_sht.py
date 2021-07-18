from os import system, remove, path
from time import strftime, localtime
from sys import exit
from webbrowser import open_new
from requests import get
from bs4 import BeautifulSoup

from getData import get_title, get_magnet, get_pic_urlList, get_today_article, get_ALL
from tool_function import clearConsole, choose_type, changeDate, make_html, Write_into_Clipboard

info = {
    'author': 'CyuanHunag',
    'version': '3.8.5',
    'email': 'dec880126@icloud.com',
    'official site': 'https://github.com/dec880126/Auto_sht',
    'Copyright': 'Copyright © 2021. Cyuan All rights reserved.',
    'license': 'GPL-3.0 License'
}

class Fourm():
    def __init__(self):
        self.type = ""
        self.title = []
        self.magnet = []
        self.title_magnet = {}
        self.picture_path = "" # path of HTML files
        self.fileName = "請先運行圖片抓取模式"


def remove_html_if_exist(fourmList):
    for fourm in fourmList:
        if path.isfile(fourm.picture_path):        
            remove(fourm.picture_path)
            print("[*]" + fourm.picture_path + "HTML files 已刪除")        

def check_update(current_version):
    print("[/]" + "檢查是否為最新版本中......".center(41))
    url = 'https://github.com/dec880126/Auto_sht/releases/'
    html = get(url)
    soup = BeautifulSoup(html.text,"html.parser")
    latest_version = soup.find("div", "f1 flex-auto min-width-0 text-normal").get_text().strip()
    if current_version != latest_version:
        print("[*]" + f"最新版本: {latest_version} 已經發布".center(41))
        return False
    else:
        print("[*]" + "已經是最新版本".center(41))
        return True

if __name__ == '__main__':    
    # Param
    fourmList_Chinese = ["無碼", "有碼", "國產", "歐美", "中文"]
    fourmList_Eng = [["WM"], ["YM"], ["GC"], ["OM"], ["JW"]]
    fourmList = []
    URL_List = [36, 37, 2, 38, 103]
    pic_link_List = [[], [], [], [], []]

    '''
    URL_List
    0. 無碼: https://www.sehuatang.org/forum-36-1.html
    1. 有碼: https://www.sehuatang.org/forum-37-1.html
    2. 國產: https://www.sehuatang.org/forum-2-1.html
    3. 歐美: https://www.sehuatang.org/forum-38-1.html
    4. 中文: https://www.sehuatang.org/forum-103-1.html
    '''
    today_list = [[], [], [], [], []]

    # Default Setting
    today = str(strftime("%Y-%m-%d", localtime()))

    # Publish class
    fourmList_index = 0
    for fourm in fourmList_Eng:
        fourmList.append(Fourm())
        fourmList[fourmList_index].type = fourmList_Chinese[fourmList_index]
        fourmList_index += 1    
    # Check Version
    if check_update(info['version']):
        pass
    else:
        while True:
            to_update = input(f"[?]是否要下載最新版本?(y/n):")
            if to_update == 'y' or to_update == 'Y':
                webbrowser.open_new('https://github.com/dec880126/Auto_sht/releases/')
                exit()
            elif to_update == 'n' or to_update == 'N':
                break
            else:
                continue
    try:
        # Main Loop        
        while True:
            try:
                print('[*]================== Auto_sht ===================')
                print("[*]" + info['version'].center(46))
                print("[*]")
                print("[*]" + "↓ Follow the updates and Guides Here ↓".center(41))
                print("[*]" + "https://github.com/dec880126/Auto_sht/releases".center(41))
                print('[*]===============================================')
                print("[*]" + "1. 開始抓取".center(41))
                print("[*]" + "2. 修改日期".center(41))
                print("[*]" + "3. 資料查詢".center(41))
                print("[*]" + "4. 重製資料".center(41))
                print("[*]" + "5. 結束程式".center(41))
                print("[*]" + "隨時可按 Ctrl + C 回到此頁面".center(41))
                print('[*]===============================================')        
                typeChoose = int(input("[?]請選擇功能(1~5):"))

                # Finish
                if typeChoose == 5:
                    break

                # Reset Data
                if typeChoose == 4:
                    reset_index = choose_type()
                    fourmList[reset_index-1].__init__()
                    continue
                
                # To ensure typeChoose in the list
                if typeChoose < 1 or typeChoose > 5:
                    print('[*]===============================================')
                    print("[?]請重新輸入功能選單中之數字(1~5)...")
                    system("pause")
                    continue

                # Change date
                if typeChoose == 2:
                    today = changeDate()
                    continue
                
                # Data Search
                """
                fourmList = [WM, YM, GC, OM, JW] <- every element is object Fourm
                """
                if typeChoose == 3:      
                    try:                
                        fourm_search = choose_type()

                        if len(fourmList[fourm_search-1].title_magnet) == 0:
                            raise BaseException()
                        for title, magnet in fourmList[fourm_search-1].title_magnet.items():
                            if magnet != "None":
                                print(f'[*] {title} : {magnet}')                    
                    except:
                        print(f"[*]資料庫中目前無資料")
                        print('[*]===============================================')
                    system("pause")
                    continue
                
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
                while not today_list[fourmChoose-1]:
                    print(f"[*]{today} 的 {str(fourmList_Chinese[fourmChoose-1])} 區 的文章清單不存在!")
                    today_list[fourmChoose-1] = get_today_article(str(fourmList_Chinese[fourmChoose-1]), home_code, today)

                    if not today_list[fourmChoose-1]:
                        print(f"[*]{today} 目前尚未有文章更新")
                        today = changeDate()
                        today_list[fourmChoose-1] = get_today_article(home_code, today)

                workSpace = fourmList[fourmChoose-1]
                # start to extract
                if extractChoose_mean == 'choose':
                    # Ensure Data exist
                    if len(workSpace.title_magnet) == 0:
                        workSpace.title_magnet, pic_link_List[fourmChoose-1] = get_ALL(today_list[fourmChoose-1])

                    # Make HTML files
                    workSpace.picture_path, workSpace.fileName = make_html(input_list=pic_link_List[fourmChoose-1], fileName="Auto_SHT_Pic_" + fourmList_Chinese[fourmChoose-1] + ".html", \
                        titleList=[title for title in workSpace.title_magnet.keys()], \
                        magnetList=[magnet for magnet in workSpace.title_magnet.values()], \
                        article_Code_List=today_list[fourmChoose-1])
                        
                    print('[*]===============================================')

                    # Open HTML files with default browser
                    open_new(workSpace.picture_path)

                    temp = workSpace.title_magnet.copy()

                    # Start working for choose movie
                    print("[*]以下為挑選作業的規則說明:")
                    print("[*]如果要保留請隨意輸入(不要空白即可)，並按下 Enter 送出")
                    print("[*]如果要捨棄，直接按下 Enter 送出即可捨棄")
                    print("[*]如果誤刪了，可以輸入: -1，來返回操作")
                    print('[*]===============================================')
                    Num = 0
                    title_List = [str(x) for x in workSpace.title_magnet.keys()]            
                    title_List_history = ["尚未放棄任何選擇"]
                    title_List_history.extend(title_List)

                    for title in title_List:
                        # """
                        # Save: Type any word
                        # Do not save: Just enter it
                        # Exit the progress: Enter "exit"
                        # """
                        Num += 1
                        print('[*]現在選擇的是:')
                        if_save = input(f"[?]{Num}. {title}:   ", )

                        if if_save == "":
                            # """
                            # Case: Do not save
                            # """
                            workSpace.title_magnet[title] += "DO_NOT_SAVE"  # magnet .. ... .DO_NOT_SAVE
                        elif if_save == "-1":
                            # """
                            # Case: Recovery
                            # """
                            print('[*]現在選擇的是:')
                            if_save = input(f"[?]{Num-1}. {title_List_history[Num-1]}:   ")
                            if if_save == "":
                                # """
                                # Case: Do not save
                                # """
                                workSpace.title_magnet[title_List_history[Num-1]] += "DO_NOT_SAVE"  # magnet .. ... .DO_NOT_SAVE
                            elif if_save == "exit":
                                # """
                                # Case: Exit - Stage I
                                # """
                                break
                            
                            # """
                            # Case: Save
                            # """
                            check_if_save = str(workSpace.title_magnet[title_List_history[Num-1]])
                            if check_if_save[-11:] == "DO_NOT_SAVE":
                                mag_temp = workSpace.title_magnet[title_List_history[Num-1]]
                                workSpace.title_magnet[title_List_history[Num-1]] = mag_temp.replace("DO_NOT_SAVE", "")

                            # Recover last data
                            Num -= 1
                            title_List.insert(title_List.index(title)+1, title)
                        elif if_save == "exit":
                            # """
                            # Case: Exit - Stage I
                            # """
                            break
                    else:
                        # """
                        # Case: Save
                        # """
                        if workSpace.title_magnet[title][-11:] == "DO_NOT_SAVE":
                            workSpace.title_magnet[title].replace("DO_NOT_SAVE", "")
                    if if_save == "exit":
                        # """
                        # Case: Exit - Stage II
                        # """
                        workSpace.title_magnet = temp
                        continue

                    # workSpace.title_magnet = temp
                    print('[*]===============================================')
                    print(f"[*]以下為 magnet 輸出:")
                    magnet_choosen = [x for x in workSpace.title_magnet.values() if x[-11:] != "DO_NOT_SAVE"]

                    for magnet in magnet_choosen:
                        print(magnet)
                    Write_into_Clipboard(magnet_choosen)
                    print('[*]magnet 已複製至剪貼簿')
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
            except:
                system("pause")
                continue
            finally:
                clearConsole()
                if typeChoose != 5:
                    continue
        remove_html_if_exist(fourmList)
        system("pause")
        clearConsole()
    except:
        print(f"\n\n-*-*-*-*-[!]Error has happened, contact me with email: {info['email']}[!]-*-*-*-*-\n")
