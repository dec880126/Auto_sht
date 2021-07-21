import os
import time
import sys
import webbrowser
import requests
import bs4
import getpass
import concurrent.futures

import getData
import tool_function
import Synology_Web_API
import config

info = {
    'author': 'CyuanHunag',
    'version': '5.0.0',
    'email': 'dec880126@icloud.com',
    'official site': 'https://github.com/dec880126/Auto_sht'
}


# Parameters
# '''
# URL_List
# 0. 無碼: https://www.sehuatang.org/forum-36-1.html
# 1. 有碼: https://www.sehuatang.org/forum-37-1.html
# 2. 國產: https://www.sehuatang.org/forum-2-1.html
# 3. 歐美: https://www.sehuatang.org/forum-38-1.html
# 4. 中文: https://www.sehuatang.org/forum-103-1.html
# '''
fourmList_Chinese = ["無碼", "有碼", "國產", "歐美", "中文"]
fourmList_Eng = [["WM"], ["YM"], ["GC"], ["OM"], ["JW"]]
URL_List = [36, 37, 2, 38, 103]      
pic_link_List = [[], [], [], [], []]
today_list = [[], [], [], [], []]
fourmList = []
today = str(time.strftime("%Y-%m-%d", time.localtime()))


class Fourm():
    def __init__(self):
        self.type = ""
        self.title = []
        self.magnet = []
        self.title_magnet = {}
        self.picture_path = "" # path of HTML files
        self.fileName = "請先運行圖片抓取模式"


class Endding(Exception):
    def __init__(self):
        sys.exit()


def Auto_sht_function(functionChoose):
    """
    功能清單
    type functionChoose: str
    """    
    method = functionDefined.get(functionChoose, default)
    
    return method()


def default():
    print('請重新選擇功能')


def remove_html_if_exist(fourmList):
    for fourm in fourmList:
        if os.path.isfile(fourm.picture_path):        
            os.remove(fourm.picture_path)
            print("[*]" + fourm.picture_path + "HTML files 已刪除")        


def check_update(current_version):
    print("[/]" + "檢查是否為最新版本中......".center(41))
    url = 'https://github.com/dec880126/Auto_sht/releases/'
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text,"html.parser")
    latest_version = soup.find("div", "f1 flex-auto min-width-0 text-normal").get_text().strip()
    if current_version != latest_version:
        print("[*]" + f"最新版本: {latest_version} 已經發布".center(41))
        return False
    else:
        print("[*]" + "已經是最新版本".center(41))
        return True


def Synology_setting():
    """
    IP = '192.168.0.183'
    PORT = 5000
    SECURE = False
    USER = ''
    PASSWORD = ''
    """    
    global syno_info

    while True:
        print("[*]               1. 開啟或修改設定")
        print("[*]               2. 關閉")
        print('[*]===============================================')
        SETTING_SYNOLOGY = int(input("[?]選擇要執行的動作:"))
        try:
            if SETTING_SYNOLOGY == 1:
                syno_info['upload'] = True
                syno_info['IP'] = input("[?]Synology NAS　IP:(ex:192.168.1.100)\n")
                syno_info['PORT'] = input('[?]Port:(預設5000)')
                syno_info['SECURE'] = False
                syno_info['USER'] = input('[?]Synology NAS 帳號:')
                syno_info['PASSWORD'] =  getpass.getpass('[?]Synology NAS 密碼:')
                break
            elif SETTING_SYNOLOGY == 2:
                syno_info['upload'] = False
                os.system('pause')
                break
        except ValueError:
            pass


def reset_data():
    reset_index = tool_function.choose_type()
    fourmList[reset_index-1].__init__()


def edit_date():
    '''
    rtype: str <- today's info
    '''
    global today
    today = tool_function.changeDate()


def history_search():
    try:                
        fourm_search = tool_function.choose_type()

        if len(fourmList[fourm_search-1].title_magnet) == 0:
            raise BaseException()
        search_result_Number = 0
        for title, magnet in fourmList[fourm_search-1].title_magnet.items():
            if magnet[-11:] != "DO_NOT_SAVE":
                search_result_Number += 1
                print(f'[*]{search_result_Number}. {title} :\n[*]{magnet}')                    
    except:
        print(f"[*]資料庫中目前無資料")
        print('[*]===============================================')
    os.system("pause")


def extract():
    global today
    # Fourm Choose
    fourmChoose = tool_function.choose_type()        
    home_code = URL_List[fourmChoose-1]
    print('[*]===============================================')
    print("[*]以下為 " + str(today) + " " + str(fourmList_Chinese[fourmChoose-1]) + " 區的挑選作業:")

    # Check if today_List for each fourm exist or not
    # make the list of article that published today

    pages = [pageNum for pageNum in range(1, 10)]
    fourmtype = str(fourmList_Chinese[fourmChoose-1])
    fourms = [fourmtype]*len(pages)
    homeCodes = [home_code]*len(pages)
    todays = [today]*len(pages)    

    while not today_list[fourmChoose-1]:
        getData.initial_param()
        print(f"[*]{today} 的 {fourmtype} 區 的文章清單不存在!")
        print(f"[/]{today} 的 {fourmtype} 區 的文章清單獲取中...")
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(getData.get_today_article, fourms, homeCodes, todays, pages)
        end_time = time.time()        
        today_list[fourmChoose-1] = getData.get_todays()

        if not today_list[fourmChoose-1]:
            print(f"[*]{today} 目前尚未有文章更新")
            today = tool_function.changeDate()       
            start_time = time.time()     
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(getData.get_today_article, fourms, homeCodes, todays, pages)
            end_time = time.time()
            today_list[fourmChoose-1] = getData.get_todays()
    
    print("[!]抓取完成")
    print(f"[*]一共花了 {end_time - start_time:2.2f} 秒來抓取 {today} 的 {fourmtype} 區 的文章清單")
    workSpace = fourmList[fourmChoose-1]

    # start to extract
    # Ensure Data exist
    if len(workSpace.title_magnet) == 0:
        print(f'[*]開始抓取 {today} 的 {fourmtype} 區 的文章')
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(getData.get_ALL, today_list[fourmChoose-1], [fourmtype for i in range(len(today_list[fourmChoose-1]))])
        end_time = time.time()
        print("[!]抓取完成")
        print(f"[*]一共花了 {end_time - start_time:2.2f} 秒爬取 {len(today_list[fourmChoose-1])} 篇文章")
        
        workSpace.title_magnet = getData.get_titles_magnets()
        pic_link_List[fourmChoose-1] = getData.get_picLinkList()

    title_List = [str(x) for x in workSpace.title_magnet.keys()] 
    if fourmtype == '有碼':
            print(f'[*]一共排除了 {len(today_list[fourmChoose-1]) - len(title_List)} 篇素人文章，並保留了 {len(title_List)} 篇文章')

    # Make HTML files
    workSpace.picture_path, workSpace.fileName = tool_function.make_html(input_list=pic_link_List[fourmChoose-1], fileName="Auto_SHT_Pic_" + fourmList_Chinese[fourmChoose-1] + ".html", \
        titleList=[title for title in workSpace.title_magnet.keys()], \
        magnetList=[magnet for magnet in workSpace.title_magnet.values()], \
        article_Code_List=today_list[fourmChoose-1])

    # Open HTML files with default browser
    webbrowser.open_new(workSpace.picture_path)

    temp = workSpace.title_magnet.copy()
    
    Num = 0
    # title_List = [str(x) for x in workSpace.title_magnet.keys()]            
    title_List_history = ["尚未放棄任何選擇"]
    title_List_history.extend(title_List)

    # Start working for choose movie
    print('[*]===============================================')
    print("[*]以下為挑選作業的規則說明:")
    print("[*]如果要保留請隨意輸入(不要空白即可)，並按下 Enter 送出")
    print("[*]如果要捨棄，直接按下 Enter 送出即可捨棄")
    print("[*]如果誤刪了，可以輸入: -1，來返回操作")
    print('[*]===============================================')

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

    # workSpace.title_magnet = temp

    magnet_choosen = [x for x in workSpace.title_magnet.values() if x[-11:] != "DO_NOT_SAVE"]

    # 有選取magnet才會執行輸出
    if magnet_choosen:
        print('[*]===============================================')
        print(f"[*]以下為 magnet 輸出:")    

        # Synology Web API
        if syno_info['upload']:
            ds = Synology_Web_API.SynologyDownloadStation(ip=syno_info['IP'], port=syno_info['PORT'], secure=syno_info['SECURE'])
            ds.login(syno_info['USER'], syno_info['PASSWORD'])
            for magnet_to_download in magnet_choosen:
                ds.uploadTorrent(magnet_to_download, syno_info['PATH'])

        for magnet in magnet_choosen:
            print(magnet)
        tool_function.Write_into_Clipboard(magnet_choosen)
        print('[*]magnet 已複製至剪貼簿')
        print('[*]===============================================')
    else:
        print('[!]無選取任何 magnet')


def exit_Auto_sht():
    """
    刪除 HTML files 並關閉程式
    """
    remove_html_if_exist(fourmList)
    raise Endding 


# ================== Dictionary ==================

functionDefined = {
    '1': extract,
    '2': edit_date,
    '3': history_search,
    '4': reset_data,
    # '5': Synology_setting,
    'EXIT': exit_Auto_sht
}

# ============== End of Dictionary ==============


if __name__ == '__main__':
    # Publish class
    fourmList_index = 0
    for fourm in fourmList_Eng:
        fourmList.append(Fourm())
        fourmList[fourmList_index].type = fourmList_Chinese[fourmList_index]
        fourmList_index += 1

    # Check Version
    current_version_show = "目前版本:" + info['version']
    print('[*]============== Auto_sht 版本確認 ===============')
    print("[*]" + current_version_show.center(41))
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
    
    #  Load config    
    if config.check_config_if_exist(file_name = "config.ini"):
        syno_info = config.load_config()
    else:
        print("[!]若為初次運行 Auto_sht ，請先至檔案目錄下配置 config.ini")
        config.make_config("./config.ini")
        os.system('pause')
        sys.exit()

    # Main Loop        
    while True:
        print('[*]================== Auto_sht ===================')
        print("[*]" + info['version'].center(46))
        print("[*]")
        print("[*]" + "↓ Official Site ↓".center(46))
        print("[*]" + "https://github.com/dec880126/Auto_sht".center(46))   
        print('[*]===============================================')         
        print("[*]               1. 開始抓取")
        print("[*]               2. 修改日期")
        print("[*]               3. 資料查詢")
        print("[*]               4. 重製資料")
        print("[*]               EXIT. 結束程式")
        print("[*]          隨時可按 Ctrl + C 回到此頁面")
        print('[*]===============================================')        
        functionChoose = input(f"[?]請選擇功能(1~{len(functionDefined)-1}):")

        if functionChoose == 'exit':
            functionChoose = 'EXIT'

        # 檢查 functionChoose 是否在功能清單中 否則重複選擇直到成功
        if functionChoose not in functionDefined:
            print('[*]===============================================')
            print("[?]請重新輸入功能選單中之數字(1~5)...")
            os.system("pause")
            continue

        try:
            # 根據所選擇之功能開始作業
            Auto_sht_function(functionChoose)
        except Endding:
            print("系統發生錯誤 將回到主選單...")            
            continue
        finally:
            os.system('pause')
            
            # 結束每階段任務後清除 Console
            tool_function.clearConsole()
