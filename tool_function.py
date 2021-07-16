import sys
import time
import os
import datetime

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


def make_html(input_list, fileName, titleList, magnetList):
    '''
    Read the url in the input_list, and make the HTML file

    type input_list: list
    '''
    path = "./" + fileName

    print(f"[/]{fileName} 產生中...")
    f = open(path, 'w', encoding="utf-8")
    f.write(f"""
    <!doctype html>
    <html>
        <head>
            <title>Auto SHT Picture Viewer</title>
        </head>
        <body>
            <div style="text-align:center;">
    """)

    pageNum = 0
    for url in input_list:
        title = titleList[pageNum]
        if url == "None":
            continue
        elif url == "end of page":
            f.write(f"<br><h3>{magnetList[pageNum]}</h3>")
            f.write("<hr />")
            pageNum += 1
        elif url == "Head of Page":
            f.write("<h2>" + title + "</h2>")
        else:
            f.write("<img src = " + str(url) + """ width="1200" height="807">""")

    f.write("""
                <a>Copyright © 2021.</a><a href = "https://github.com/dec880126" target="_blank">Cyuan</a><a>&nbsp&nbspAll rights reserved. </a>
            </div>
        </body>
    </html>""")
    f.close()
    path = f"{os.getcwd()}\{path[2:]}"
    
    print(f"[*]{fileName} 產生成功! -> 檔案路徑: {path}")
    return path, fileName


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


def choose_type():
    typeList_Chinese = ["無碼", "有碼", "國產", "歐美", "中文"]
    print('[*]===============================================') 
    print("[*]                 1. 無碼")
    print("[*]                 2. 有碼")
    print("[*]                 3. 國產")
    print("[*]                 4. 歐美")
    print("[*]                 5. 中文")
    print('[*]===============================================') 
    while True:     
        typeChoose = int(input(f"[?]請選擇分區(1~5):"))
        if typeChoose >= 1 and typeChoose <= 5:
            print(f'[*]選擇的是 {typeChoose}. {typeList_Chinese[typeChoose-1]} 分區')
            print('[*]===============================================') 
            return typeChoose


def changeDate():
    print('[*]===============================================')
    today = str(time.strftime("%Y-%m-%d", time.localtime()))
    print(f"[*]今天是 {today}")
    print(f"[*](昨天: -1, 前天: -2...)")
    print('[*]===============================================')
    date = input("[?]請問日期要更改為?:")
    if int(date) < 0 and int(date) > -4:
        return getYesterday(abs(int(date)))
